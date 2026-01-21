/**
 * Patient Page JavaScript
 * Handles patient form submission
 */

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect to login if not authenticated
}

// Handle patient form submission
document.getElementById('patient-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address').value,
        medical_history: document.getElementById('medical_history').value
    };

    try {
        const response = await apiRequest('/patients', {
            method: 'POST',
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showSuccess('Patient added successfully!');

            // Clear form
            document.getElementById('patient-form').reset();

            // Redirect to dashboard after 2 seconds
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 2000);
        } else {
            showError(data.error || 'Failed to add patient');
        }
    } catch (error) {
        showError('Network error. Please check if the server is running.');
        console.error('Error adding patient:', error);
    }
});
