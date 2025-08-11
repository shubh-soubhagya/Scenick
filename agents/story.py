# agent1.py
import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file.")

# LangChain Groq Chat Model for Story
story_agent = ChatGroq(
    groq_api_key=api_key,
    model_name="compound-beta-mini",
    temperature=0.7
)

def generate_story(user_input: str):
    """
    Generates short story, character description, and background description.
    Returns a dictionary with keys: short_story, character_description, background_description
    """
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
        return json.loads(story_response)
    except json.JSONDecodeError:
        start, end = story_response.find("{"), story_response.rfind("}")
        return json.loads(story_response[start:end+1])
