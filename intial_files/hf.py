import torch
from diffusers import StableDiffusionPipeline
import time
import os

# ==== 1. Custom local path for model download ====
custom_model_path = r"models_cpu"

# ==== 2. Choose a CPU-friendly model ====
model_id = "runwayml/stable-diffusion-v1-5"

# ==== 3. Load or download model to custom path ====
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32,   # CPU precision
    use_safetensors=True,
    cache_dir=custom_model_path  # custom path
).to("cpu")

# ==== 4. Generate image ====
seed = 42
generator = torch.manual_seed(seed)
filename = r"output.png"

image = pipe(
    prompt="""Generate a vibrant outdoor market scene under a warm 2 pm sun. A kaleidoscope of fresh produce is displayed on wooden crates, 
    wicker baskets, and burlap sacks. Tomatoes, lemons, and bell peppers glisten in the sunlight, while leafy greens and vibrant flowers add 
    pops of green and yellow to the canvas. Vendors' calls and friendly chatter fill the air, captured in soft brushstrokes reminiscent of 
    Impressionism. Incorporate weathered stone, 
    rustic metal, and worn wooden beams to create a lively and carefree atmosphere, with textures and colors that leap off the canvas.""",

    negative_prompt="bad hands, low quality, blurry, extra limbs, text, watermark",
    num_inference_steps=20,  # reduce for faster CPU inference
    guidance_scale=9,
    width=512,
    height=512,
    generator=generator
).images[0]

# ==== 5. Save result ====
image.save(filename)
print(f"Saved as {filename} (seed: {seed})")
