from datetime import datetime
import csv
import cv2
import numpy as np
import speech_recognition as sr
from agents.story import generate_story
from agents.prompt import generate_image_prompt
from img_agents.imagegen import generate_images_from_csv
from combine import remove_bg, overlay_same_size

def listen_for_input():
    """
    Uses microphone to capture user speech and return recognized text.
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Adjusting for background noise... Please wait.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    print("🎤 Listening... Speak now.")
    with mic as source:
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            speech_text = recognizer.recognize_google(audio)
            print(f"✅ You said: {speech_text}")
            return speech_text.strip()
        except sr.WaitTimeoutError:
            print("⚠️ No speech detected.")
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio.")
        except sr.RequestError:
            print("⚠️ Speech recognition service error.")

    return ""

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


# Example run
if __name__ == "__main__":
    print("Choose input method:")
    print("1 → Type your story idea")
    print("2 → Speak your story idea")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        user_idea = input("✍️ Enter your story idea: ").strip()
    elif choice == "2":
        user_idea = listen_for_input()
        if not user_idea:
            print("⚠️ No valid speech detected. Exiting.")
            exit()
    else:
        print("⚠️ Invalid choice. Exiting.")
        exit()

    orchestrate_story_to_image(user_idea)
