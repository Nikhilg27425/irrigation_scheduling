// Irrigation Model Page JavaScript

async function loadCropTypes() {
    try {
        const response = await fetch('/api/crop_types');
        const data = await response.json();
        
        const cropTypeSelect = document.getElementById('cropType');
        cropTypeSelect.innerHTML = '<option value="">Select Crop Type</option>';
        
        data.crop_types.forEach(cropType => {
            const option = document.createElement('option');
            option.value = cropType;
            option.textContent = cropType;
            cropTypeSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading crop types:', error);
    }
}

document.getElementById('irrigationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());
    
    showLoading();
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            displayResults(result, data);
        } else {
            showError(result.error || 'Prediction failed');
        }
    } catch (error) {
        showError('Network error. Please try again.');
    }
});

function showLoading() {
    document.getElementById('results').innerHTML = `
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-3">Analyzing...</p>
    `;
}

function displayResults(result, inputData) {
    const confidenceClass = result.confidence > 0.8 ? 'confidence-high' : 
                           result.confidence > 0.6 ? 'confidence-medium' : 'confidence-low';
    const resultClass = result.prediction === 1 ? 'result-irrigation' : 'result-no-irrigation';
    const icon = result.prediction === 1 ? 'fas fa-tint' : 'fas fa-ban';
    
    document.getElementById('results').innerHTML = `
        <div class="result-card ${resultClass} fade-in">
            <i class="${icon} fa-3x mb-3"></i>
            <h3>${result.prediction_text}</h3>
            <div class="confidence-bar">
                <div class="confidence-fill ${confidenceClass}" 
                     style="width: ${(result.confidence * 100).toFixed(1)}%"></div>
            </div>
            <p><strong>Confidence: ${(result.confidence * 100).toFixed(1)}%</strong></p>
        </div>
    `;
}

function showError(message) {
    document.getElementById('results').innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>${message}
        </div>
    `;
}

loadCropTypes();
