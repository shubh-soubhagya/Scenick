document.addEventListener('DOMContentLoaded', function() {
    const voiceBtn = document.getElementById('voice-btn');
    const generateBtn = document.getElementById('generate-btn');
    const storyInput = document.getElementById('story-input');
    const resultContainer = document.getElementById('result-container');
    
    // Voice recognition using Django backend
    voiceBtn.addEventListener('click', async function() {
        voiceBtn.disabled = true;
        voiceBtn.textContent = 'Listening...';
        
        try {
            const response = await fetch('/voice-input/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                storyInput.value = data.text;
            } else {
                alert('Voice input failed: ' + data.message);
            }
        } catch (error) {
            console.error('Voice input error:', error);
            alert('Error accessing microphone: ' + error.message);
        } finally {
            voiceBtn.textContent = '🎤 Voice Input';
            voiceBtn.disabled = false;
        }
    });
    
    // Generate story and images
    generateBtn.addEventListener('click', async function() {
        const userInput = storyInput.value.trim();
        
        if (!userInput) {
            alert('Please enter or speak your story idea');
            return;
        }
        
        // Show loading state
        generateBtn.textContent = 'Generating...';
        generateBtn.disabled = true;
        
        try {
            // Send data to server as JSON
            const response = await fetch('/generate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ user_input: userInput })
            });
            
            const data = await response.json();
            
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
                alert('Error: ' + data.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while generating your scene');
        } finally {
            generateBtn.textContent = 'Generate Scene';
            generateBtn.disabled = false;
        }
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

