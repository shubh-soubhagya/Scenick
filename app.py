# app.py
from datetime import datetime
import csv
import cv2
import numpy as np
from agents.story import generate_story
from agents.prompt import generate_image_prompt
from img_agents.imagegen import generate_images_from_csv
from combine import remove_bg, overlay_same_size

def orchestrate_story_to_image(user_input, csv_path="groq_outputs.csv"):
    # Step 1 → Story and descriptions
    story_data = generate_story(user_input)
    char_desc = story_data.get("character_description", "")
    bg_desc = story_data.get("background_description", "")

    # Step 2 → Image prompts
    char_img_prompt = generate_image_prompt(char_desc)
    bg_img_prompt = generate_image_prompt(bg_desc)

    # Step 3 → Save to CSV
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input,
        "short_story": story_data.get("short_story", ""),
        "character_description": char_desc,
        "background_description": bg_desc,
        "character_image_prompt": char_img_prompt,
        "background_image_prompt": bg_img_prompt
    }

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    print(f"✅ Row added to {csv_path}")

    image_paths = generate_images_from_csv(csv_path)
    print("✅ Generated Images:", image_paths)

    bg_img = cv2.imread(r"generated_images\background_img.png")
    char_img = cv2.imread(r"generated_images\char_img.png")

    # Remove background
    char_img_rgba = remove_bg(char_img)

    # Overlay
    final_img = overlay_same_size(bg_img, char_img_rgba)

    # Save and show
    cv2.imwrite("combined_result.png", final_img)
    # cv2.imshow("Combined", final_img)
    # cv2.waitKey(2000)
    # cv2.destroyAllWindows()


# Example run
if __name__ == "__main__":
    user_idea = input("Enter your story idea: ").strip()
    orchestrate_story_to_image(user_idea)
