# Scenick - AI Story to Image Generator

Transform text narratives into immersive visual scenes with Scenick - an AI-powered platform that automatically generates characters and backgrounds using cutting-edge Groq language models and Stable Diffusion image generation.

Prompt Enginnering Documentaion: [PDF](/Prompt engineering documentation.pdf)
Output Examples: [`generated_images/` directory](/generated_images/)  

## Features

- 🎙️ Voice or text input for story ideas
- 📖 Automatic story generation using Groq AI models
- 🖼️ AI-generated character and background images
- 🎨 Combined scene composition
- ⚡ Fast inference with Groq's LPU technology

## Technology Stack

- **Backend**: Django
- **AI Models**: 
    - `llama-3.1-8b-instant` and `compound-beta-mini` for text generation
    - `runwayml/stable-diffusion-v1-5` for image generation
- **Frontend**: HTML, CSS, JavaScript
- **Audio**: Google's `speech_recognition`
- **Image Processing**: OpenCV and `mediapipe` for bg remover.

## Setup Instructions

### Prerequisites

- Python 3.10+
- Groq API key (free)
- NVIDIA GPU (recommended for image generation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shubh-soubhagya/scenick.git
   cd scenick

2. **Set up virtual environment**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate

3. **Install Dependencies**
    ```bash 
    pip install -r requirements.txt

4. **Set up environment variables**: Create a .env file:
    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

5. **Database Setup**
    ```bash
    python manage.py migrate

6. **Run the application**
    ```bash
    python manage.py runserver
    ```
    Open http://localhost:8000 in your browser.

### Configuration
1. Get your API key from [Groq Cloud](https://console.groq.com/keys)
2. Add it to your `.env` file:

    ```bash
    GROQ_API_KEY=your_api_key_here
    ```

## Design Architecture Structure
```bash
Scenick/
├── agents/
│ ├── prompt.py
│ ├── story.py
│── demo/
├── generated_images/
├── img_agents/
│ ├── combine.py
│ ├── imagegen.py
│── initial_files/
├── models_cpu
├── scenick/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── storyapp/
│ ├── migrations/
│ ├── static/
│ │ └── storyapp/
│ │ ├── css/
│ │ │ └── style.css
│ │ └── js/
│ │   └── script.js
│ ├── templates/
│ │   └── storyapp/
│ │     └── index.html
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
├── venv/
├── .env
├── .gitignore
├── app.py
├── db.sqlite3
├── groq_outputs.csv
├── manage.py
└── README.md
```

### Key Directories and Files

- **agents/**: Contains scripts for story generation and prompts
  - `prompt.py`: Handles prompt generation
  - `story.py`: Manages story and description creation logic
- **img_agents/**: Contains image generation components
  - `combine.py`: Combines generated images
  - `imagegen.py`: Handles image generation
- **scenick/**: Django project configuration
  - Core settings and URL configurations
- **storyapp/**: Django application
  - `models.py`: Database models
  - `views.py`: Application logic
  - `static/`: CSS and JavaScript files
  - `templates/`: HTML templates
- **generated_images/**: Stores output images
- **root files**:
  - `manage.py`: Django management script
  - `app.py`: Script to run in CLI
  - `.env`: Environment variables
  - `requirements.txt`: Python dependencies
