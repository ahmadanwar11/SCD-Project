/**
 * Dashboard Page JavaScript
 * Handles loading and displaying dashboard data
 */

// Check authentication on page load - wrapped in DOMContentLoaded to ensure page is ready
document.addEventListener('DOMContentLoaded', () => {
    // Debug: Log token status
    const token = localStorage.getItem('token');
    console.log('Dashboard loaded. Token present:', !!token);

    if (!checkAuth()) {
        // Will redirect to login if not authenticated
        console.log('No token found, redirecting to login');
    } else {
        console.log('Token found, loading dashboard');
    }
});

/**
 * Load dashboard data from API
 */
async function loadDashboard() {
    try {
        const response = await apiRequest('/dashboard');

        if (!response.ok) {
            const data = await response.json();
            showError(data.error || 'Failed to load dashboard');
            return;
        }

        const data = await response.json();

        // Update statistics
        document.getElementById('patient-count').textContent = data.patients.length;
        document.getElementById('doctor-count').textContent = data.doctors.length;
        document.getElementById('medicine-count').textContent = data.total_medicines;
        document.getElementById('reminder-count').textContent = data.today_reminders.length;

        // Display patients
        displayPatients(data.patients);

        // Display doctors
        displayDoctors(data.doctors);

        // Display today's reminders
        displayTodayReminders(data.today_reminders);

    } catch (error) {
        showError('Network error. Please check if the server is running.');
        console.error('Error loading dashboard:', error);
    }
}

/**
 * Display patients list
 */
function displayPatients(patients) {
    const patientsList = document.getElementById('patients-list');

    if (patients.length === 0) {
        patientsList.innerHTML = '<p class="empty-message">No patients added yet. <a href="add-patient.html">Add your first patient</a></p>';
        return;
    }

    patientsList.innerHTML = patients.map(patient => `
        <div class="card">
            <h4>${patient.name}</h4>
            <p><span class="card-label">Age:</span> ${patient.age} years</p>
            <p><span class="card-label">Gender:</span> ${patient.gender}</p>
            <p><span class="card-label">Phone:</span> ${patient.phone}</p>
            ${patient.address ? `<p><span class="card-label">Address:</span> ${patient.address}</p>` : ''}
            ${patient.medical_history ? `<p><span class="card-label">Medical History:</span> ${patient.medical_history}</p>` : ''}
        </div>
    `).join('');
}

/**
 * Display doctors list
 */
function displayDoctors(doctors) {
    const doctorsList = document.getElementById('doctors-list');

    if (doctors.length === 0) {
        doctorsList.innerHTML = '<p class="empty-message">No doctors assigned yet. <a href="add-doctor.html">Add a doctor</a></p>';
        return;
    }

    doctorsList.innerHTML = doctors.map(doctor => `
        <div class="card">
            <h4>Dr. ${doctor.name}</h4>
            <p><span class="card-label">Specialization:</span> ${doctor.specialization}</p>
            <p><span class="card-label">Phone:</span> ${doctor.phone}</p>
            ${doctor.email ? `<p><span class="card-label">Email:</span> ${doctor.email}</p>` : ''}
            ${doctor.hospital ? `<p><span class="card-label">Hospital:</span> ${doctor.hospital}</p>` : ''}
        </div>
    `).join('');
}

/**
 * Display today's reminders
 */
function displayTodayReminders(reminders) {
    const remindersList = document.getElementById('today-reminders');

    if (reminders.length === 0) {
        remindersList.innerHTML = '<p class="empty-message">No reminders for today</p>';
        return;
    }

    remindersList.innerHTML = reminders.map(reminder => `
        <div class="reminder-item">
            <div class="reminder-info">
                <h4>${reminder.medicine_name}</h4>
                <p><strong>Patient:</strong> ${reminder.patient_name}</p>
                <p><strong>Dosage:</strong> ${reminder.dosage}</p>
                <p><strong>Time:</strong> ${formatTime(reminder.reminder_time)}</p>
                ${reminder.notes ? `<p><strong>Notes:</strong> ${reminder.notes}</p>` : ''}
            </div>
            <div>
                <span class="reminder-status status-${reminder.status}">${reminder.status.toUpperCase()}</span>
                ${reminder.status === 'pending' ? `
                    <button class="btn btn-primary" style="margin-top: 0.5rem;" onclick="markAsCompleted(${reminder.id})">
                        Mark as Completed
                    </button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

/**
 * Mark reminder as completed
 */
async function markAsCompleted(reminderId) {
    try {
        const response = await apiRequest(`/reminders/${reminderId}`, {
            method: 'PUT',
            body: JSON.stringify({ status: 'completed' })
        });

        if (!response.ok) {
            const data = await response.json();
            showError(data.error || 'Failed to update reminder');
            return;
        }

        showSuccess('Reminder marked as completed!');
        // Reload dashboard to reflect changes
        setTimeout(() => loadDashboard(), 1000);

    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error updating reminder:', error);
    }
}

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
