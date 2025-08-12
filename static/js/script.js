// DOM Elements
const storyInput = document.getElementById('storyInput');
const generateBtn = document.getElementById('generateBtn');
const voiceBtn = document.getElementById('voiceBtn');
const voiceStatus = document.getElementById('voiceStatus');
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');
const errorModal = document.getElementById('errorModal');
const errorMessage = document.getElementById('errorMessage');
const closeError = document.getElementById('closeError');
const errorOk = document.getElementById('errorOk');

// Result elements
const combinedImage = document.getElementById('combinedImage');
const characterImage = document.getElementById('characterImage');
const backgroundImage = document.getElementById('backgroundImage');
const storyText = document.getElementById('storyText');
const characterDescription = document.getElementById('characterDescription');
const backgroundDescription = document.getElementById('backgroundDescription');
const characterPrompt = document.getElementById('characterPrompt');
const backgroundPrompt = document.getElementById('backgroundPrompt');

// Progress steps
const steps = document.querySelectorAll('.step');

// State management
let isProcessing = false;
let recognition = null;

// Initialize speech recognition if available
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
} else {
    voiceBtn.disabled = true;
    voiceBtn.innerHTML = '<span class="btn-text">🚫 Voice not supported</span>';
}

// Event Listeners
generateBtn.addEventListener('click', handleTextInput);
voiceBtn.addEventListener('click', handleVoiceInput);
closeError.addEventListener('click', hideError);
errorOk.addEventListener('click', hideError);

// Enter key support for textarea
storyInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        handleTextInput();
    }
});

// Functions
async function handleTextInput() {
    const input = storyInput.value.trim();
    if (!input) {
        showError('Please enter a story idea first.');
        return;
    }
    
    if (isProcessing) return;
    
    await processStory(input);
}

async function handleVoiceInput() {
    if (!recognition || isProcessing) return;
    
    setButtonLoading(voiceBtn, true);
    voiceStatus.textContent = 'Listening... Please speak clearly.';
    
    try {
        const spokenText = await startListening();
        voiceStatus.textContent = `You said: "${spokenText}"`;
        await processStory(spokenText);
    } catch (error) {
        console.error('Voice recognition error:', error);
        showError('Could not understand your speech. Please try again.');
        voiceStatus.textContent = 'Voice recognition failed. Try again.';
    } finally {
        setButtonLoading(voiceBtn, false);
    }
}

function startListening() {
    return new Promise((resolve, reject) => {
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            resolve(transcript);
        };
        
        recognition.onerror = (event) => {
            reject(new Error(event.error));
        };
        
        recognition.onend = () => {
            voiceStatus.textContent = 'Processing your speech...';
        };
        
        recognition.start();
    });
}

async function processStory(userInput) {
    if (isProcessing) return;
    
    isProcessing = true;
    hideResults();
    showLoading();
    setButtonLoading(generateBtn, true);
    
    try {
        // Simulate progress through steps
        await simulateProgress();
        
        // Make API call
        const response = await fetch('/process-story/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ user_input: userInput })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Server error occurred');
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
        
    } catch (error) {
        console.error('Error processing story:', error);
        showError(`Failed to generate your scene: ${error.message}`);
    } finally {
        hideLoading();
        setButtonLoading(generateBtn, false);
        isProcessing = false;
    }
}

async function simulateProgress() {
    const stepMessages = [
        'Analyzing your story...',
        'Creating character description...',
        'Designing background elements...',
        'Generating images...',
        'Combining final scene...'
    ];
    
    for (let i = 0; i < steps.length; i++) {
        // Activate current step
        steps[i].classList.add('active');
        loadingText.textContent = stepMessages[i];
        
        // Wait for a bit to simulate processing
        await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
        
        // Mark as completed
        steps[i].classList.remove('active');
        steps[i].classList.add('completed');
    }
}

function displayResults(data) {
    // Set images
    combinedImage.src = data.combined_image_url;
    characterImage.src = data.character_image_url;
    backgroundImage.src = data.background_image_url;
    
    // Set text content
    storyText.textContent = data.story;
    characterDescription.textContent = data.character_description;
    backgroundDescription.textContent = data.background_description;
    characterPrompt.textContent = `Prompt: ${data.character_prompt}`;
    backgroundPrompt.textContent = `Prompt: ${data.background_prompt}`;
    
    // Show results with animation
    showResults();
    
    // Clear input
    storyInput.value = '';
    voiceStatus.textContent = '';
}

function showResults() {
    resultsSection.classList.add('show');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResults() {
    resultsSection.classList.remove('show');
}

function showLoading() {
    // Reset all steps
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
    
    loadingOverlay.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
    document.body.style.overflow = 'auto';
}

function showError(message) {
    errorMessage.textContent = message;
    errorModal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function hideError() {
    errorModal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Handle image loading errors
function handleImageError(img) {
    img.style.display = 'none';
    img.parentElement.innerHTML += '<div class="image-placeholder">Image could not be loaded</div>';
}

// Add error handlers to images
combinedImage.addEventListener('error', () => handleImageError(combinedImage));
characterImage.addEventListener('error', () => handleImageError(characterImage));
backgroundImage.addEventListener('error', () => handleImageError(backgroundImage));

// Add some visual feedback for image loading
[combinedImage, characterImage, backgroundImage].forEach(img => {
    img.addEventListener('load', function() {
        this.style.opacity = '0';
        this.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            this.style.opacity = '1';
        }, 100);
    });
});

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === errorModal) {
        hideError();
    }
});

// Add keyboard shortcut hints
document.addEventListener('DOMContentLoaded', () => {
    // Add tooltip to generate button
    generateBtn.title = 'Click or press Ctrl+Enter to generate';
    
    // Auto-focus on story input
    storyInput.focus();
    
    console.log('🎭 Scenick loaded successfully!');
});