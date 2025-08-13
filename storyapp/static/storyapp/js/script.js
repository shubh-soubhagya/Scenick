document.addEventListener('DOMContentLoaded', function() {
    const voiceBtn = document.getElementById('voice-btn');
    const generateBtn = document.getElementById('generate-btn');
    const storyInput = document.getElementById('story-input');
    const resultContainer = document.getElementById('result-container');
    
    // Voice recognition
    voiceBtn.addEventListener('click', function() {
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            
            recognition.onstart = function() {
                voiceBtn.textContent = 'Listening...';
                storyInput.placeholder = 'Speak now...';
            };
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                storyInput.value = transcript;
                voiceBtn.textContent = '🎤 Voice Input';
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error', event.error);
                voiceBtn.textContent = '🎤 Voice Input';
                alert('Voice recognition failed. Please try again.');
            };
            
            recognition.onend = function() {
                voiceBtn.textContent = '🎤 Voice Input';
            };
            
            recognition.start();
        } else {
            alert('Your browser does not support speech recognition. Please use Chrome or Edge.');
        }
    });
    
    // Generate story and images
    generateBtn.addEventListener('click', function() {
        const userInput = storyInput.value.trim();
        
        if (!userInput) {
            alert('Please enter or speak your story idea');
            return;
        }
        
        // Show loading state
        generateBtn.textContent = 'Generating...';
        generateBtn.disabled = true;
        
        // Send data to server
        fetch('/generate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: `user_input=${encodeURIComponent(userInput)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update the UI with results
                document.getElementById('combined-img').src = data.combined_img;
                document.getElementById('char-img').src = data.char_img;
                document.getElementById('bg-img').src = data.bg_img;
                document.getElementById('story-text').textContent = data.story;
                document.getElementById('char-desc').textContent = data.char_desc;
                document.getElementById('bg-desc').textContent = data.bg_desc;
                document.getElementById('char-prompt').textContent = data.char_prompt;
                document.getElementById('bg-prompt').textContent = data.bg_prompt;
                
                // Show results
                resultContainer.classList.remove('hidden');
            } else {
                alert('Error generating story and images: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while generating your scene');
        })
        .finally(() => {
            generateBtn.textContent = 'Generate Scene';
            generateBtn.disabled = false;
        });
    });
    
    // Helper function to get CSRF token
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
});

