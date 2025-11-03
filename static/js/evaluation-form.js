// Evaluation Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Update slider values in real-time
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        const valueDisplay = slider.parentElement.querySelector('.slider-value');
        
        slider.addEventListener('input', (e) => {
            valueDisplay.textContent = e.target.value;
            updateOverallAverage();
        });
    });
    
    // Calculate and display overall average
    function updateOverallAverage() {
        const reliability = parseInt(document.getElementById('reliability')?.value || 0);
        const quality = parseInt(document.getElementById('quality_of_work')?.value || 0);
        const initiative = parseInt(document.getElementById('initiative')?.value || 0);
        const teamwork = parseInt(document.getElementById('teamwork')?.value || 0);
        const communication = parseInt(document.getElementById('communication')?.value || 0);
        
        const average = (reliability + quality + initiative + teamwork + communication) / 5;
        const overallDisplay = document.getElementById('overall-average');
        
        if (overallDisplay) {
            overallDisplay.textContent = average.toFixed(1);
        }
    }
    
    // Handle async form submission
    const form = document.getElementById('evaluationForm');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const submitBtn = e.target.querySelector('button[type="submit"]');
            
            // Disable submit button
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            try {
                const response = await fetch('/evaluate', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    // Show success modal
                    showSuccessModal();
                    
                    // Reset form
                    e.target.reset();
                    
                    // Reset sliders to default value
                    document.querySelectorAll('input[type="range"]').forEach(slider => {
                        slider.value = 7;
                        const valueDisplay = slider.parentElement.querySelector('.slider-value');
                        if (valueDisplay) {
                            valueDisplay.textContent = '7';
                        }
                    });
                    
                    updateOverallAverage();
                } else {
                    alert('Error submitting evaluation. Please try again.');
                }
            } catch (error) {
                alert('Error submitting evaluation. Please try again.');
                console.error(error);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit Evaluation';
            }
        });
    }
    
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// Show success modal
function showSuccessModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.add('active');
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('successModal');
    if (e.target === modal) {
        closeModal();
    }
});
