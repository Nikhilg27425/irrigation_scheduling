// Smart Irrigation Scheduler - Frontend JavaScript

class IrrigationScheduler {
    constructor() {
        this.recentPredictions = JSON.parse(localStorage.getItem('recentPredictions') || '[]');
        this.init();
    }

    init() {
        this.loadCropTypes();
        this.setupEventListeners();
        this.displayRecentPredictions();
    }

    async loadCropTypes() {
        try {
            const response = await fetch('/crop_types');
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
            this.showError('Failed to load crop types');
        }
    }

    setupEventListeners() {
        const form = document.getElementById('irrigationForm');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));

        // Real-time validation
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.validateInput(input));
        });
    }

    validateInput(input) {
        const value = input.value.trim();
        
        if (input.hasAttribute('required') && !value) {
            input.classList.add('is-invalid');
            input.classList.remove('is-valid');
            return false;
        }

        // Validate numeric inputs
        if (input.type === 'number') {
            const min = parseFloat(input.getAttribute('min'));
            const max = parseFloat(input.getAttribute('max'));
            const numValue = parseFloat(value);

            if (numValue < min || numValue > max) {
                input.classList.add('is-invalid');
                input.classList.remove('is-valid');
                return false;
            }
        }

        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
        return true;
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());

        // Validate all inputs
        const isValid = Array.from(e.target.querySelectorAll('input, select'))
            .every(input => this.validateInput(input));

        if (!isValid) {
            this.showError('Please fill in all fields correctly');
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                this.displayResults(result, data);
                this.savePrediction(result, data);
            } else {
                this.showError(result.error || 'Prediction failed');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Network error. Please try again.');
        }
    }

    showLoading() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Analyzing your data...</p>
            </div>
        `;
    }

    displayResults(result, inputData) {
        const resultsDiv = document.getElementById('results');
        
        const confidenceClass = result.confidence > 0.8 ? 'confidence-high' : 
                               result.confidence > 0.6 ? 'confidence-medium' : 'confidence-low';

        const resultClass = result.prediction === 1 ? 'result-irrigation' : 'result-no-irrigation';
        const icon = result.prediction === 1 ? 'fas fa-tint' : 'fas fa-ban';
        const recommendation = result.prediction === 1 ? 
            'Irrigation is recommended based on current conditions' : 
            'No irrigation needed at this time';

        resultsDiv.innerHTML = `
            <div class="result-card ${resultClass} fade-in">
                <i class="${icon} fa-3x mb-3"></i>
                <h3>${result.prediction_text}</h3>
                <p class="lead">${recommendation}</p>
                
                <div class="confidence-bar">
                    <div class="confidence-fill ${confidenceClass}" 
                         style="width: ${(result.confidence * 100).toFixed(1)}%">
                    </div>
                </div>
                <p><strong>Confidence: ${(result.confidence * 100).toFixed(1)}%</strong></p>
                
                <hr style="border-color: rgba(255,255,255,0.3);">
                
                <div class="row mt-3">
                    <div class="col-6">
                        <small>No Irrigation: ${(result.probabilities.no_irrigation * 100).toFixed(1)}%</small>
                    </div>
                    <div class="col-6">
                        <small>Irrigation Needed: ${(result.probabilities.irrigation_needed * 100).toFixed(1)}%</small>
                    </div>
                </div>
            </div>
            
            <div class="mt-3">
                <h6><i class="fas fa-info-circle me-2"></i>Input Summary</h6>
                <div class="row">
                    <div class="col-6">
                        <small><strong>Crop:</strong> ${inputData.crop_type}</small><br>
                        <small><strong>Days:</strong> ${inputData.crop_days}</small>
                    </div>
                    <div class="col-6">
                        <small><strong>Moisture:</strong> ${inputData.soil_moisture}</small><br>
                        <small><strong>Temp:</strong> ${inputData.temperature}°C</small>
                    </div>
                </div>
            </div>
        `;
    }

    showError(message) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `
            <div class="alert alert-danger fade-in">
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
    }

    savePrediction(result, inputData) {
        const prediction = {
            timestamp: new Date().toLocaleString(),
            input: inputData,
            result: result
        };

        this.recentPredictions.unshift(prediction);
        
        // Keep only last 5 predictions
        if (this.recentPredictions.length > 5) {
            this.recentPredictions = this.recentPredictions.slice(0, 5);
        }

        localStorage.setItem('recentPredictions', JSON.stringify(this.recentPredictions));
        this.displayRecentPredictions();
    }

    displayRecentPredictions() {
        const container = document.getElementById('recentPredictions');
        
        if (this.recentPredictions.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No recent predictions</p>';
            return;
        }

        const predictionsHtml = this.recentPredictions.map(pred => {
            const predictionClass = pred.result.prediction === 1 ? 'irrigation' : '';
            const icon = pred.result.prediction === 1 ? 'fas fa-tint text-danger' : 'fas fa-ban text-success';
            
            return `
                <div class="prediction-item ${predictionClass}">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <i class="${icon} me-2"></i>
                            <strong>${pred.input.crop_type}</strong> - ${pred.result.prediction_text}
                        </div>
                        <small class="text-muted">${pred.timestamp}</small>
                    </div>
                    <small class="text-muted">
                        Moisture: ${pred.input.soil_moisture}, Temp: ${pred.input.temperature}°C
                    </small>
                </div>
            `;
        }).join('');

        container.innerHTML = predictionsHtml;
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new IrrigationScheduler();
});

// Add some utility functions
function formatNumber(num, decimals = 1) {
    return parseFloat(num).toFixed(decimals);
}

function getConfidenceColor(confidence) {
    if (confidence > 0.8) return 'success';
    if (confidence > 0.6) return 'warning';
    return 'danger';
}

// Add smooth scrolling for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
