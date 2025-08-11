import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
from langchain.schema import HumanMessage
# from langchain.chat_models import ChatGroq
from langchain_groq import ChatGroq

# ──────────────────────────────
# Load API Key
# ──────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file.")

# ──────────────────────────────
# LangChain Groq Chat Models (Agents)
# ──────────────────────────────
story_agent = ChatGroq(
    groq_api_key=api_key,
    model_name="compound-beta-mini",
    temperature=0.7
)

image_agent = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

# ──────────────────────────────
# Orchestration Function
# ──────────────────────────────
def orchestrate_story_to_image(user_input, csv_path="groq_outputs.csv"):
    # Step 1: Agent 1 → Generate story + descriptions
    story_prompt = f"""
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
    story_response = story_agent([HumanMessage(content=story_prompt)]).content.strip()

    try:
        parsed = json.loads(story_response)
    except json.JSONDecodeError:
        start, end = story_response.find("{"), story_response.rfind("}")
        parsed = json.loads(story_response[start:end+1])

    # Step 2: Agent 2 → Generate image prompts
    char_desc = parsed.get("character_description", "")
    bg_desc = parsed.get("background_description", "")

    char_img_prompt = image_agent([
        HumanMessage(content=f"Create a highly detailed and visually rich image generation prompt. The prompt should help an AI image generation tool visualize the description below. Description: {char_desc}.Make sure it's realistic, vivid, and suitable for image generation in 80 words paragraph")]).content.strip()

    bg_img_prompt = image_agent([
        HumanMessage(content=f"Create a highly detailed and visually rich image generation prompt. The prompt should help an AI image generation tool visualize the description below. Description: {bg_desc}.Make sure it's realistic, vivid, and suitable for image generation in 80 words paragraph")
    ]).content.strip()

    # Step 3: Save all results into CSV
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input,
        "short_story": parsed.get("short_story", ""),
        "character_description": char_desc,
        "background_description": bg_desc,
        "character_image_prompt": char_img_prompt,
        "background_image_prompt": bg_img_prompt
    }

    # write_header = not os.path.exists(csv_path)
    # with open(csv_path, "a", newline="", encoding="utf-8") as f:
    #     writer = csv.DictWriter(f, fieldnames=row.keys())
    #     if write_header:
    #         writer.writeheader()
    #     writer.writerow(row)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    print(f"✅ Row added to {csv_path}")

# ──────────────────────────────
# Run Example
# ──────────────────────────────
if __name__ == "__main__":
    user_idea = input("Enter your story idea: ").strip()
    orchestrate_story_to_image(user_idea)
