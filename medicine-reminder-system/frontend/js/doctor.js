/**
 * Doctor Page JavaScript
 * Handles doctor form submission
 */

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect to login if not authenticated
}

// Handle doctor form submission
document.getElementById('doctor-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = {
        name: document.getElementById('name').value,
        specialization: document.getElementById('specialization').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        hospital: document.getElementById('hospital').value
    };

    try {
        const response = await apiRequest('/doctors', {
            method: 'POST',
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showSuccess('Doctor added successfully!');

            // Clear form
            document.getElementById('doctor-form').reset();

            // Redirect to dashboard after 2 seconds
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 2000);
        } else {
            showError(data.error || 'Failed to add doctor');
        }
    } catch (error) {
        showError('Network error. Please check if the server is running.');
        console.error('Error adding doctor:', error);
    }
});
