# app.py
from datetime import datetime
import csv
from agents.story import generate_story
from agents.prompt import generate_image_prompt
from img_agents.imagegen import generate_images_from_csv

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


# Example run
if __name__ == "__main__":
    user_idea = input("Enter your story idea: ").strip()
    orchestrate_story_to_image(user_idea)
