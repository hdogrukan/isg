import os
import json

# GitHub raw URL kökü
RAW_BASE_URL = "https://raw.githubusercontent.com/hdogrukan/isg/main/images"

# JSONL dosyasına yaz
with open("isg_train.jsonl", "w", encoding="utf-8") as fp:
    # Klasörleri gez (örneğin: images/kask, images/eldiven, ...)
    for class_name in sorted(os.listdir("images")):
        class_dir = os.path.join("images", class_name)
        if not os.path.isdir(class_dir):
            continue

        # Her görsel için
        for image_file in sorted(os.listdir(class_dir)):
            if not image_file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            # Görsel URL’si
            image_url = f"{RAW_BASE_URL}/{class_name}/{image_file}"
            ground_truth = class_name.replace("_", " ")
            # JSONL mesaj yapısı
            example = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an assistant that identifies equipment used in electricity distribution networks and occupational safety."
                    },
                    {
                        "role": "user",
                        "content": "Identify the object in the image."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                    "detail": "low"
                                }
                            }
                        ]
                    },
                    {
                        "role": "assistant",
                        "content": ground_truth
                    }
                ]
            }

            # Dosyaya yaz
            fp.write(json.dumps(example) + "\n")