# from django.shortcuts import render
# from django.http import JsonResponse
# from datetime import datetime
# import csv
# import os
# from .models import StoryImage
# from agents.story import generate_story
# from agents.prompt import generate_image_prompt
# from img_agents.imagegen import generate_images_from_csv
# from img_agents.combine import remove_bg, overlay_same_size
# import cv2
# import numpy as np

# def index(request):
#     return render(request, 'storyapp/index.html')

# def generate_story_image(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input', '')
        
#         # Step 1 → Story and descriptions
#         story_data = generate_story(user_input)
#         char_desc = story_data.get("character_description", "")
#         bg_desc = story_data.get("background_description", "")

#         # Step 2 → Image prompts
#         char_img_prompt = generate_image_prompt(char_desc)
#         bg_img_prompt = generate_image_prompt(bg_desc)

#         # Generate CSV path
#         csv_path = "groq_outputs.csv"
        
#         # Step 3 → Save to CSV
#         row = {
#             "timestamp": datetime.utcnow().isoformat(),
#             "user_input": user_input,
#             "short_story": story_data.get("short_story", ""),
#             "character_description": char_desc,
#             "background_description": bg_desc,
#             "character_image_prompt": char_img_prompt,
#             "background_image_prompt": bg_img_prompt
#         }

#         with open(csv_path, "w", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=row.keys())
#             writer.writeheader()
#             writer.writerow(row)

#         # Generate images
#         image_paths = generate_images_from_csv(csv_path)
        
#         # Process images
#         bg_img = cv2.imread(r"generated_images\background_img.png")
#         char_img = cv2.imread(r"generated_images\char_img.png")
#         char_img_rgba = remove_bg(char_img)
#         final_img = overlay_same_size(bg_img, char_img_rgba)
#         combined_path = r"generated_images\combined_result.png"
#         cv2.imwrite(combined_path, final_img)

#         # Save to database
#         story_image = StoryImage.objects.create(
#             user_input=user_input,
#             short_story=story_data.get("short_story", ""),
#             character_description=char_desc,
#             background_description=bg_desc,
#             character_image_prompt=char_img_prompt,
#             background_image_prompt=bg_img_prompt,
#             char_img_path=r"generated_images\char_img.png",
#             bg_img_path=r"generated_images\background_img.png",
#             combined_img_path=combined_path
#         )

#         return JsonResponse({
#             'status': 'success',
#             'story': story_data.get("short_story", ""),
#             'char_img': story_image.char_img_path,
#             'bg_img': story_image.bg_img_path,
#             'combined_img': story_image.combined_img_path,
#             'char_desc': char_desc,
#             'bg_desc': bg_desc,
#             'char_prompt': char_img_prompt,
#             'bg_prompt': bg_img_prompt
#         })
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})

from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import csv
import os
from .models import StoryImage
from agents.story import generate_story
from agents.prompt import generate_image_prompt
from img_agents.imagegen import generate_images_from_csv
from img_agents.combine import remove_bg, overlay_same_size
import cv2
import numpy as np
import speech_recognition as sr
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'storyapp/index.html')

@csrf_exempt  # Temporary for testing, remove in production
def voice_input(request):
    if request.method == 'POST':
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            try:
                speech_text = recognizer.recognize_google(audio)
                return JsonResponse({
                    'status': 'success',
                    'text': speech_text.strip()
                })
            except sr.UnknownValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Could not understand audio'
                }, status=400)
            except sr.RequestError as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Speech recognition service error: {str(e)}'
                }, status=500)
                
        except sr.WaitTimeoutError:
            return JsonResponse({
                'status': 'error',
                'message': 'No speech detected'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Microphone error: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def generate_story_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input', '')
            
            if not user_input:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No input provided'
                }, status=400)
            
            # Step 1 → Story and descriptions
            story_data = generate_story(user_input)
            char_desc = story_data.get("character_description", "")
            bg_desc = story_data.get("background_description", "")

            # Step 2 → Image prompts
            char_img_prompt = generate_image_prompt(char_desc)
            bg_img_prompt = generate_image_prompt(bg_desc)

            # Generate CSV path
            csv_path = os.path.join("groq_outputs.csv")
            
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

            # Generate images
            image_paths = generate_images_from_csv(csv_path)
            
            # Process images
            bg_img = cv2.imread(os.path.join("generated_images", "background_img.png"))
            char_img = cv2.imread(os.path.join("generated_images", "char_img.png"))
            char_img_rgba = remove_bg(char_img)
            final_img = overlay_same_size(bg_img, char_img_rgba)
            combined_path = os.path.join("generated_images", "combined_result.png")
            cv2.imwrite(combined_path, final_img)

            # Save to database
            story_image = StoryImage.objects.create(
                user_input=user_input,
                short_story=story_data.get("short_story", ""),
                character_description=char_desc,
                background_description=bg_desc,
                character_image_prompt=char_img_prompt,
                background_image_prompt=bg_img_prompt,
                char_img_path=os.path.join("generated_images", "char_img.png"),
                bg_img_path=os.path.join("generated_images", "background_img.png"),
                combined_img_path=combined_path
            )

            return JsonResponse({
                'status': 'success',
                'story': story_data.get("short_story", ""),
                'char_img': story_image.char_img_path,
                'bg_img': story_image.bg_img_path,
                'combined_img': story_image.combined_img_path,
                'char_desc': char_desc,
                'bg_desc': bg_desc,
                'char_prompt': char_img_prompt,
                'bg_prompt': bg_img_prompt
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
