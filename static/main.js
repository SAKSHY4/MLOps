// static/main.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const predictBtn = document.getElementById('predictBtn');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const predictionValue = document.getElementById('predictionValue');
    const errorMessage = document.getElementById('errorMessage');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get feature values
        const features = [
            parseFloat(document.getElementById('feature1').value),
            parseFloat(document.getElementById('feature2').value),
            parseFloat(document.getElementById('feature3').value),
            parseFloat(document.getElementById('feature4').value)
        ];

        // Disable button and show loading
        predictBtn.disabled = true;
        predictBtn.textContent = '🔄 Predicting...';
        
        // Hide previous results
        resultDiv.style.display = 'none';
        errorDiv.style.display = 'none';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    features: features
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Show success result
                predictionValue.textContent = `${data.prediction}`;
                resultDiv.style.display = 'block';
            } else {
                // Show error
                errorMessage.textContent = data.error || 'Unknown error occurred';
                errorDiv.style.display = 'block';
            }
        } catch (error) {
            // Network or other error
            errorMessage.textContent = 'Network error: ' + error.message;
            errorDiv.style.display = 'block';
        } finally {
            // Re-enable button
            predictBtn.disabled = false;
            predictBtn.textContent = '🔮 Predict';
        }
    });

    // Add health check
    checkHealth();
});

async function checkHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('API Health:', data);
    } catch (error) {
        console.error('Health check failed:', error);
    }
}