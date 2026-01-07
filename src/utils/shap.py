import os
import json
import base64
import hashlib
from io import BytesIO
from datetime import datetime

import shap
import matplotlib.pyplot as plt


def generate_shap_waterfall(
    model,
    input_df,
    feature_cols,
    feature_display_names,
    hidden_features,
    model_type="lgbm",
    input_data=None,
    texts = None
):
    texts = texts or {
        "title": "Contract Rejection or Confirmation Graph",
        "header": "Why was this decision made?",
        "positive": "🔴 {feature} = `{value}` → increased the probability of rejection by +{impact}",
        "negative": "🟢 {feature} = `{value}` → reduced the probability of rejection by {impact}",
        "neutral": "All feature impacts are very small or evenly distributed."
    }

    hidden_features = hidden_features or [] 

    explainer = shap.TreeExplainer(model) if model_type == "lgbm" else shap.Explainer(model)
    shap_values = explainer(input_df[feature_cols])

    if isinstance(shap_values, list):
        shap_val = shap_values[1][0]
        expected_value = explainer.expected_value[1]
    else:
        shap_val = shap_values.values[0]
        expected_value = explainer.expected_value

    row = input_df[feature_cols].iloc[0]

    display_names = [feature_display_names.get(col, col) for col in feature_cols]
    row_display = row.copy()
    row_display.index = display_names

    filtered_indices = [
        i for i, col in enumerate(feature_cols)
        if col not in hidden_features
    ]

    filtered_display_names = [display_names[i] for i in filtered_indices]
    filtered_shap_values = shap_val[filtered_indices]
    filtered_row_values = row.values[filtered_indices]

    #waterfall plot
    plt.figure(figsize=(14, 11))

    shap.plots.waterfall(
        shap.Explanation(
            values = filtered_shap_values,
            base_values=expected_value,
            data=filtered_row_values,
            feature_names = filtered_display_names,
        ),
        max_display=15,
        show=False
    )

    plt.title(
        texts["title"],
        fontsize=19, fontweight='bold', pad=40, color='darkred'
    )
    plt.tight_layout()
    plt.subplots_adjust(left=0.35, bottom=0.2, top=0.88)

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    #save image
    base_dir = os.path.dirname(os.path.abspath(__file__))
    shap_dir = os.path.abspath(os.path.join(base_dir, "..", "..", "database", "shap"))
    os.makedirs(shap_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_uid = hashlib.md5(json.dumps(input_data, sort_keys=True).encode()).hexdigest()[:10]
    img_filename = f"shap_waterfall_{hash_uid}_{timestamp}.png"
    img_path = os.path.join(shap_dir, img_filename)

    with open(img_path, "wb") as f:
        f.write(base64.b64decode(img_base64))

    shap_image_url = f"https://demo.moliy.ai/database/shap/{img_filename}"


    impacts = []
    for i, col in enumerate(feature_cols):
        if col in hidden_features:
            continue 
        actual_value = row.iloc[i]
        shap_impact = shap_val[i]
        impacts.append((col, actual_value, shap_impact))

    impacts_sorted = sorted(impacts, key=lambda x: abs(x[2]), reverse=True)

    reasons = []
    for orig_col, actual_value, shap_impact in impacts_sorted[:10]:

        if abs(shap_impact) < 0.005:
            continue

        display_name = feature_display_names.get(orig_col, orig_col)
        impact_val = f"{abs(shap_impact):.3f}"

        if shap_impact > 0:
            reasons.append(
                texts["positive"].format(
                    feature=display_name,
                    value=actual_value,
                    impact=impact_val
                )
            )
        else:
            reasons.append(
                texts["negative"].format(
                    feature=display_name,
                    value=actual_value,
                    impact=impact_val
                )
            )

    explanation_text = texts["header"] + "\n"
    explanation_text += "\n".join(reasons) if reasons else texts["neutral"]

    return {
        "shap_image_url": shap_image_url,
        "explanation_text": explanation_text,
        "shap_values": shap_val.tolist(),
        "expected_value": float(expected_value),
    }
