/**
 * Medicine Page JavaScript
 * Handles 2-step medicine form and reminder creation
 */

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect to login if not authenticated
}

let currentStep = 1;
let medicineData = {};

/**
 * Load patients and doctors for dropdown
 */
async function loadFormData() {
    try {
        // Load patients
        const patientsResponse = await apiRequest('/patients');
        if (patientsResponse.ok) {
            const patientsData = await patientsResponse.json();
            const patientSelect = document.getElementById('patient_id');

            if (patientsData.patients.length === 0) {
                patientSelect.innerHTML = '<option value="">No patients found - Add a patient first</option>';
            } else {
                patientSelect.innerHTML = '<option value="">Select a patient</option>' +
                    patientsData.patients.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
            }
        }

        // Load doctors
        const doctorsResponse = await apiRequest('/doctors');
        if (doctorsResponse.ok) {
            const doctorsData = await doctorsResponse.json();
            const doctorSelect = document.getElementById('doctor_id');

            if (doctorsData.doctors.length === 0) {
                doctorSelect.innerHTML = '<option value="">No doctors found - Add a doctor first</option>';
            } else {
                doctorSelect.innerHTML = '<option value="">Select a doctor</option>' +
                    doctorsData.doctors.map(d => `<option value="${d.id}">Dr. ${d.name} (${d.specialization})</option>`).join('');
            }
        }
    } catch (error) {
        showError('Failed to load form data');
        console.error('Error loading form data:', error);
    }
}

/**
 * Navigate to next step
 */
function goToStep2() {
    // Validate step 1 form
    const form = document.getElementById('medicine-form-step1');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    // Save step 1 data
    medicineData = {
        patient_id: parseInt(document.getElementById('patient_id').value),
        doctor_id: parseInt(document.getElementById('doctor_id').value),
        medicine_name: document.getElementById('medicine_name').value,
        dosage: document.getElementById('dosage').value,
        frequency: document.getElementById('frequency').value,
        time: document.getElementById('time').value
    };

    // Show step 2
    currentStep = 2;
    document.getElementById('medicine-form-step1').classList.remove('active');
    document.getElementById('medicine-form-step2').classList.add('active');
    document.getElementById('step-indicator-1').classList.remove('active');
    document.getElementById('step-indicator-2').classList.add('active');

    // Set default start date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('start_date').value = today;
}

/**
 * Navigate to previous step
 */
function goToStep1() {
    currentStep = 1;
    document.getElementById('medicine-form-step2').classList.remove('active');
    document.getElementById('medicine-form-step1').classList.add('active');
    document.getElementById('step-indicator-2').classList.remove('active');
    document.getElementById('step-indicator-1').classList.add('active');
}

/**
 * Add another reminder time input
 */
function addReminderTime() {
    const reminderTimesList = document.getElementById('reminder-times-list');
    const newTimeItem = document.createElement('div');
    newTimeItem.className = 'reminder-time-item';
    newTimeItem.innerHTML = `
        <input type="datetime-local" class="reminder-time-input" required>
        <button type="button" class="btn-remove-time" onclick="removeReminderTime(this)">Remove</button>
    `;
    reminderTimesList.appendChild(newTimeItem);
}

/**
 * Remove a reminder time input
 */
function removeReminderTime(button) {
    const reminderTimesList = document.getElementById('reminder-times-list');
    if (reminderTimesList.children.length > 1) {
        button.parentElement.remove();
    } else {
        showError('At least one reminder time is required');
    }
}

/**
 * Submit complete medicine and reminder form
 */
async function submitMedicineForm(e) {
    e.preventDefault();

    // Validate step 2 form
    const form = document.getElementById('medicine-form-step2');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    // Get step 2 data
    const step2Data = {
        start_date: document.getElementById('start_date').value,
        end_date: document.getElementById('end_date').value || null,
        status: document.getElementById('status').value
    };

    // Combine data
    const completeMedicineData = {
        ...medicineData,
        ...step2Data
    };

    try {
        // Create medicine
        const medicineResponse = await apiRequest('/medicines', {
            method: 'POST',
            body: JSON.stringify(completeMedicineData)
        });

        const medicineResult = await medicineResponse.json();

        if (!medicineResponse.ok) {
            showError(medicineResult.error || 'Failed to create medicine');
            return;
        }

        const medicineId = medicineResult.medicine.id;

        // Get all reminder times
        const reminderTimeInputs = document.querySelectorAll('.reminder-time-input');
        const reminderTimes = Array.from(reminderTimeInputs).map(input => input.value);

        // Create reminders
        let allRemindersCreated = true;
        for (const reminderTime of reminderTimes) {
            const reminderData = {
                medicine_id: medicineId,
                reminder_time: reminderTime,
                status: 'pending',
                notes: ''
            };

            const reminderResponse = await apiRequest('/reminders', {
                method: 'POST',
                body: JSON.stringify(reminderData)
            });

            if (!reminderResponse.ok) {
                allRemindersCreated = false;
                console.error('Failed to create reminder for time:', reminderTime);
            }
        }

        if (allRemindersCreated) {
            showSuccess('Medicine and reminders created successfully!');
        } else {
            showSuccess('Medicine created, but some reminders failed. You can add them manually.');
        }

        // Redirect to timeline after 2 seconds
        setTimeout(() => {
            window.location.href = 'timeline.html';
        }, 2000);

    } catch (error) {
        showError('Network error. Please check if the server is running.');
        console.error('Error creating medicine:', error);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load patients and doctors
    loadFormData();

    // Next step button
    document.getElementById('next-step-btn').addEventListener('click', goToStep2);

    // Previous step button
    document.getElementById('prev-step-btn').addEventListener('click', goToStep1);

    // Add reminder time button
    document.getElementById('add-reminder-time-btn').addEventListener('click', addReminderTime);

    // Submit step 2 form
    document.getElementById('medicine-form-step2').addEventListener('submit', submitMedicineForm);
});
