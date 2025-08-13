from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_story_image, name='generate_story_image'),
    # path('voice-input/', views.voice_input, name='voice_input'),
] + static('/generated_images/', document_root='generated_images')