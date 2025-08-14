# agent2.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import pandas as pd
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

df = pd.read_csv(r"groq_outputs.csv")  # Change to your CSV path
story = df.loc[0, "short_story"]

def generate_image_prompt(description: str) -> str:
    """
    Generates a detailed AI image generation prompt for the given description.
    """
    # prompt = f"""Create a highly detailed and visually rich very realistic image generation prompt. 
    # The prompt should help an AI image generation tool visualize the description below.
    # Description: {description}. 
    # Story context: {story}.
    # Make sure it's realistic, vivid, and suitable according to the story for image generation.
    # Ensure that if the subject is a character or person, they are positioned so they occupy only half of the image space.
    # THE PROMPT MUST be short, clear, and stay under 77 Stable Diffusion tokens (about 50 simple words or fewer).
    # Do not exceed this length."""

    
    prompt = f"""Create a highly detailed and visually rich very realistic image generation prompt. 
    The prompt should help an AI image generation tool visualize the description below.
    Write only the final image generation prompt. 
    Do not include explanations, introductions, or extra text — just the prompt itself.

    Description: {description}. 
    

    Make sure it's realistic, vivid, and suitable according to the story for image generation.
    If the description contains a character or person, depict them occupying only half of the image space, else ignore.
    THE PROMPT SHOULD BE WITHIN 40 WORD PARAGRAPH"""

    return image_agent([HumanMessage(content=prompt)]).content.strip()
