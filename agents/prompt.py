# agent2.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Load API Key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file.")

# LangChain Groq Chat Model for Image Prompt
image_agent = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0.7
)

def generate_image_prompt(description: str) -> str:
    """
    Generates a detailed AI image generation prompt for the given description.
    """
    prompt = f"""Create a highly detailed and visually rich very realistic image generation prompt. 
    The prompt should help an AI image generation tool visualize the description below. Description: {description}. 
    Make sure it's realistic, vivid, and suitable for image generation '
    'If the subject is a character or person, ensure they occupy only half of the image space.
    THE PROMPT SHOULD BE WITHIN 50 WORD PARAGRAPH"""

    return image_agent([HumanMessage(content=prompt)]).content.strip()
