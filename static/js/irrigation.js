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
    
    let waterRequirementHTML = '';
    let scheduleButtonHTML = '';
    
    if (result.prediction === 1 && result.water_requirement) {
        const wr = result.water_requirement;
        waterRequirementHTML = `
            <hr style="border-color: rgba(255,255,255,0.3); margin: 20px 0;">
            <h5><i class="fas fa-calculator me-2"></i>Water Requirement Calculation</h5>
            <div class="row text-start mt-3">
                <div class="col-6">
                    <small><strong>Growth Stage:</strong> ${wr.growth_stage}</small><br>
                    <small><strong>Crop Coefficient (Kc):</strong> ${wr.Kc}</small><br>
                    <small><strong>Reference ET (ETo):</strong> ${wr.ETo} mm/day</small><br>
                    <small><strong>Crop ET (ETc):</strong> ${wr.ETc} mm/day</small>
                </div>
                <div class="col-6">
                    <small><strong>Current Depletion:</strong> ${wr.current_depletion} mm</small><br>
                    <small><strong>Threshold (MAD):</strong> ${wr.threshold} mm</small><br>
                    <small><strong>Available Water:</strong> ${wr.available_water} mm</small>
                </div>
            </div>
            <div class="alert alert-light mt-3 mb-0">
                <h4 class="text-dark mb-2"><i class="fas fa-water me-2"></i>Irrigation Amount Needed</h4>
                <div class="row text-dark">
                    <div class="col-6">
                        <h5>${wr.irrigation_amount} mm</h5>
                        <small>or ${wr.irrigation_liters_per_m2} L/m²</small>
                    </div>
                    <div class="col-6">
                        <h5>${(wr.irrigation_liters_per_acre / 1000).toFixed(2)} m³/acre</h5>
                        <small>${wr.irrigation_liters_per_acre.toLocaleString()} L/acre</small>
                    </div>
                </div>
            </div>
        `;
        
        // Add schedule button
        scheduleButtonHTML = `
            <button class="btn btn-warning btn-lg w-100 mt-3" onclick="scheduleIrrigation(${result.prediction_id}, ${wr.irrigation_amount})">
                <i class="fas fa-calendar-plus me-2"></i>Schedule Irrigation
            </button>
        `;
    }
    
    document.getElementById('results').innerHTML = `
        <div class="result-card ${resultClass} fade-in">
            <i class="${icon} fa-3x mb-3"></i>
            <h3>${result.prediction_text}</h3>
            <div class="confidence-bar">
                <div class="confidence-fill ${confidenceClass}" 
                     style="width: ${(result.confidence * 100).toFixed(1)}%"></div>
            </div>
            <p><strong>Confidence: ${(result.confidence * 100).toFixed(1)}%</strong></p>
            ${waterRequirementHTML}
            ${scheduleButtonHTML}
        </div>
    `;
}

function scheduleIrrigation(predictionId, waterAmount) {
    // Calculate optimal time (6 AM tomorrow)
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(6, 0, 0, 0);
    
    const scheduleData = {
        prediction_id: predictionId,
        water_amount: waterAmount,
        duration: 60,  // 60 minutes default
        scheduled_time: tomorrow.toISOString()
    };
    
    fetch('/api/schedule/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(scheduleData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✓ Irrigation scheduled for ' + new Date(data.scheduled_time).toLocaleString());
            window.location.href = '/schedule';
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('Error scheduling irrigation');
        console.error(error);
    });
}

function showError(message) {
    document.getElementById('results').innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>${message}
        </div>
    `;
}

loadCropTypes();
