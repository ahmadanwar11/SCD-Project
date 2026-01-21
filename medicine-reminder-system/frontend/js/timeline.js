/**
 * Timeline Page JavaScript
 * Handles loading and displaying reminders in chronological order
 */

// Check authentication on page load
if (!checkAuth()) {
    // Will redirect to login if not authenticated
}

let allReminders = [];

/**
 * Load all reminders from API
 */
async function loadReminders() {
    try {
        const response = await apiRequest('/reminders');

        if (!response.ok) {
            const data = await response.json();
            showError(data.error || 'Failed to load reminders');
            return;
        }

        const data = await response.json();
        allReminders = data.reminders;

        // Display reminders
        displayTimeline(allReminders);

    } catch (error) {
        showError('Network error. Please check if the server is running.');
        console.error('Error loading reminders:', error);
    }
}

/**
 * Display reminders in timeline format
 */
function displayTimeline(reminders) {
    const timelineContainer = document.getElementById('timeline-container');

    if (reminders.length === 0) {
        timelineContainer.innerHTML = '<p class="empty-message">No reminders found. <a href="add-medicine.html">Add a medicine</a> to create reminders.</p>';
        return;
    }

    // Group reminders by date
    const groupedReminders = groupByDate(reminders);

    // Create timeline HTML
    let timelineHTML = '<div class="timeline">';

    for (const [date, dateReminders] of Object.entries(groupedReminders)) {
        timelineHTML += `
            <div class="timeline-item">
                <div class="timeline-date">${formatDate(date)}</div>
                ${dateReminders.map(reminder => `
                    <div class="timeline-content">
                        <h4>${reminder.medicine_name}</h4>
                        <p><strong>Patient:</strong> ${reminder.patient_name || 'N/A'}</p>
                        <p><strong>Dosage:</strong> ${reminder.dosage || 'N/A'}</p>
                        <p><strong>Time:</strong> ${formatTime(reminder.reminder_time)}</p>
                        ${reminder.notes ? `<p><strong>Notes:</strong> ${reminder.notes}</p>` : ''}
                        <p>
                            <span class="reminder-status status-${reminder.status}">
                                ${reminder.status.toUpperCase()}
                            </span>
                        </p>
                        <div class="timeline-actions">
                            ${reminder.status === 'pending' ? `
                                <button class="btn btn-primary" onclick="updateReminderStatus(${reminder.id}, 'completed')">
                                    Mark as Completed
                                </button>
                            ` : ''}
                            ${reminder.status === 'completed' ? `
                                <button class="btn btn-secondary" onclick="updateReminderStatus(${reminder.id}, 'pending')">
                                    Mark as Pending
                                </button>
                            ` : ''}
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    timelineHTML += '</div>';
    timelineContainer.innerHTML = timelineHTML;
}

/**
 * Group reminders by date
 */
function groupByDate(reminders) {
    const grouped = {};

    reminders.forEach(reminder => {
        const date = reminder.reminder_time.split('T')[0];
        if (!grouped[date]) {
            grouped[date] = [];
        }
        grouped[date].push(reminder);
    });

    // Sort reminders within each date by time
    for (const date in grouped) {
        grouped[date].sort((a, b) => new Date(a.reminder_time) - new Date(b.reminder_time));
    }

    // Sort dates
    const sortedGrouped = {};
    Object.keys(grouped).sort().forEach(date => {
        sortedGrouped[date] = grouped[date];
    });

    return sortedGrouped;
}

/**
 * Filter reminders by status
 */
function filterReminders(status) {
    if (status === 'all') {
        displayTimeline(allReminders);
    } else {
        const filtered = allReminders.filter(r => r.status === status);
        displayTimeline(filtered);
    }
}

/**
 * Update reminder status
 */
async function updateReminderStatus(reminderId, newStatus) {
    try {
        const response = await apiRequest(`/reminders/${reminderId}`, {
            method: 'PUT',
            body: JSON.stringify({ status: newStatus })
        });

        if (!response.ok) {
            const data = await response.json();
            showError(data.error || 'Failed to update reminder');
            return;
        }

        showSuccess(`Reminder marked as ${newStatus}!`);

        // Reload reminders
        setTimeout(() => loadReminders(), 1000);

    } catch (error) {
        showError('Network error. Please try again.');
        console.error('Error updating reminder:', error);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load reminders on page load
    loadReminders();

    // Filter change event
    document.getElementById('status-filter').addEventListener('change', (e) => {
        filterReminders(e.target.value);
    });
});
