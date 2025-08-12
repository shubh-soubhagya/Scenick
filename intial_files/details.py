"""
groq_csv_generator_orchestrated.py
- Requires: pip install langchain-groq python-dotenv pandas
- Make a .env file with: GROQ_API_KEY=your_api_key_here
"""

import os
import json
import csv
from datetime import datetime
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# ──────────────────────────────
# Load API key
# ──────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Groq API key not found in .env file.")

# ──────────────────────────────
# LangChain Groq model setup
# ──────────────────────────────
MODEL = "compound-beta-mini"

story_agent = ChatGroq(
    groq_api_key=api_key,
    model_name=MODEL,
    temperature=0.7
)

PROMPT_TEMPLATE = """
You are a creative writer. Given the following user input, produce a JSON object with exactly three keys:
  1) "short_story" - a short fictional story (about 6-12 sentences).
  2) "character_description" - a detailed description of the main character (Age, Gender, Physical features (hair, eyes, height, skin tone, clothing), Facial expression or mood,
     Accessories, if any, Artistic style suggestion, etc).
  3) "background_description" - a detailed setting / background (Environment type (indoor, outdoor, natural, urban), Time of day and lighting,
     Colors and textures, Objects present, Mood or atmosphere, Artistic style suggestion, etc).

Return ONLY valid JSON (no extra commentary). Make sure strings are properly escaped and the JSON can be parsed by a program.

User input:
\"\"\"{user_input}\"\"\"
"""

# ──────────────────────────────
# Function to call Groq model via LangChain
# ──────────────────────────────
def call_groq_and_get_json(user_input, temperature=0.7, max_tokens=800):
    prompt = PROMPT_TEMPLATE.format(user_input=user_input)

    # Call LangChain Groq agent
    resp = story_agent([HumanMessage(content=prompt)])
    text = resp.content.strip()

    # Try parsing JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except json.JSONDecodeError:
                pass
    raise ValueError(f"Could not parse JSON from model output:\n{text}")

# ──────────────────────────────
# CSV Writer
# ──────────────────────────────
def append_row_to_csv(csv_path, row_dict):
    fieldnames = ["timestamp", "user_input", "short_story", "character_description", "background_description"]

    # Always overwrite so only one row exists
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row_dict)

# ──────────────────────────────
# Main Orchestration
# ──────────────────────────────
def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("Enter a short prompt for the story/character/background: ").strip()
        if not user_input:
            print("No input provided. Exiting.")
            return

    print("Calling Groq model via LangChain orchestration...")

    try:
        parsed = call_groq_and_get_json(user_input)
    except Exception as e:
        print("Generation or parsing failed:", e)
        return

    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input,
        "short_story": parsed.get("short_story", ""),
        "character_description": parsed.get("character_description", ""),
        "background_description": parsed.get("background_description", "")
    }

    csv_path = "groq_outputs.csv"
    append_row_to_csv(csv_path, row)
    print(f"✅ Wrote generated row to {csv_path}")

if __name__ == "__main__":
    main()
