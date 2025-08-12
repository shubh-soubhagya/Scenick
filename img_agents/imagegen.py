import os
import torch
import pandas as pd
from diffusers import StableDiffusionPipeline

# ==== Global: Load Model Once ====
custom_model_path = r"models_cpu"
model_id = "runwayml/stable-diffusion-v1-5"


pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32,  # CPU-friendly
    use_safetensors=True,
    cache_dir=custom_model_path
).to("cpu")


def generate_image(prompt: str, output_path: str, seed: int = 42):
    """
    Generates a single image from a given prompt and saves it to output_path.
    """
    generator = torch.manual_seed(seed)
    image = pipe(
        prompt=prompt,
        negative_prompt="bad hands, low quality, blurry, extra limbs, text, watermark",
        num_inference_steps=20,
        guidance_scale=9,
        width=512,
        height=512,
        generator=generator
    ).images[0]
    image.save(output_path)
    return output_path


def generate_images_from_csv(csv_path: str, output_dir: str = "generated_images"):
    """
    Reads a CSV containing 'character_image_prompt' and 'background_image_prompt',
    generates images for each row, and saves them in output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    saved_files = []
    for idx, row in df.iterrows():
        char_prompt = str(row["character_image_prompt"])
        bg_prompt = str(row["background_image_prompt"])

        # Save images with row index for uniqueness
        char_filename = os.path.join(output_dir, "char_img.png")
        bg_filename = os.path.join(output_dir, "background_img.png")

        generate_image(char_prompt, char_filename)
        generate_image(bg_prompt, bg_filename)

        saved_files.append((char_filename, bg_filename))

    return saved_files
