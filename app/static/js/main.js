// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - Orphanage Management System');
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
