# import pandas as pd
# from groq import Groq
# from dotenv import load_dotenv
# import os

# # ──────────────────────────────
# # Groq API Setup
# # ──────────────────────────────

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")

# client = Groq(api_key=api_key)

# def generate_image_prompt(description, type_):
#     """Generates an image prompt from a given description using Groq LLM."""
#     prompt = f"""
#     Create a highly detailed and visually rich image generation prompt for a {type_}.
#     The prompt should help an AI image generation tool visualize the description below.
#     Description: {description}
#     Make sure it's realistic, vivid, and suitable for image generation.
#     """
    
#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",  # You can change model if needed
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.7,
#         max_tokens=200
#     )

#     return response.choices[0].message.content.strip()

# # ──────────────────────────────
# # Read the CSV File
# # ──────────────────────────────
# df = pd.read_csv("groq_outputs.csv")  # Must have columns: character_description, background_description

# # ──────────────────────────────
# # Generate Prompts for Each Row
# # ──────────────────────────────
# char_prompts = []
# bg_prompts = []

# for _, row in df.iterrows():
#     char_desc = row['character_description']
#     bg_desc = row['background_description']
    
#     char_prompt = generate_image_prompt(char_desc, "character")
#     bg_prompt = generate_image_prompt(bg_desc, "background")
    
#     char_prompts.append(char_prompt)
#     bg_prompts.append(bg_prompt)

# # Add new columns to DataFrame
# df['character_image_prompt'] = char_prompts
# df['background_image_prompt'] = bg_prompts

# # Save updated CSV
# df.to_csv("groq_outputs.csv", index=False)

# print("✅ Prompts generated and saved to descriptions_with_prompts.csv")


"""
groq_image_prompt_generator_orchestrated.py
- Requires: pip install langchain-groq python-dotenv pandas
- Make a .env file with: GROQ_API_KEY=your_api_key_here
"""

import os
import pandas as pd
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
image_agent = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",  # You can change this if needed
    temperature=0.7
)

# ──────────────────────────────
# Generate image prompt
# ──────────────────────────────
def generate_image_prompt(description, type_):
    """Generates an image prompt from a given description using LangChain + Groq."""
    prompt = f"""
    Create a highly detailed and visually rich image generation prompt for a {type_}.
    The prompt should help an AI image generation tool visualize the description below.
    Description: {description}
    Make sure it's realistic, vivid, and suitable for image generation.
    """
    resp = image_agent([HumanMessage(content=prompt)])
    return resp.content.strip()

# ──────────────────────────────
# Read the CSV File
# ──────────────────────────────
df = pd.read_csv("groq_outputs.csv")  # Must have: character_description, background_description

# ──────────────────────────────
# Generate Prompts for Each Row
# ──────────────────────────────
char_prompts = []
bg_prompts = []

for _, row in df.iterrows():
    char_desc = row['character_description']
    bg_desc = row['background_description']

    char_prompt = generate_image_prompt(char_desc, "character")
    bg_prompt = generate_image_prompt(bg_desc, "background")

    char_prompts.append(char_prompt)
    bg_prompts.append(bg_prompt)

# Add new columns
df['character_image_prompt'] = char_prompts
df['background_image_prompt'] = bg_prompts

# Save updated CSV
df.to_csv("groq_outputs.csv", index=False)

print("✅ Prompts generated and saved to groq_outputs.csv")
