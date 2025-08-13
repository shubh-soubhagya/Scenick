from django.db import models

class StoryImage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_input = models.TextField()
    short_story = models.TextField()
    character_description = models.TextField()
    background_description = models.TextField()
    character_image_prompt = models.TextField()
    background_image_prompt = models.TextField()
    char_img_path = models.CharField(max_length=255)
    bg_img_path = models.CharField(max_length=255)
    combined_img_path = models.CharField(max_length=255)

    def __str__(self):
        return f"StoryImage {self.id}"