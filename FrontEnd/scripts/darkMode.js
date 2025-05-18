// Dark mode functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for saved dark mode preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        // Update toggle button state
        const toggleBtn = document.getElementById('togglebtn');
        if (toggleBtn) {
            toggleBtn.querySelector('.slider').style.transform = 'translateX(30px)';
        }
    }
});

// Function to toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    // Save the preference
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    
    // Update toggle button state
    const toggleBtn = document.getElementById('togglebtn');
    if (toggleBtn) {
        const slider = toggleBtn.querySelector('.slider');
        if (document.body.classList.contains('dark-mode')) {
            slider.style.transform = 'translateX(30px)';
        } else {
            slider.style.transform = 'translateX(0)';
        }
    }
} 