// Dark Mode Functionality
function initDarkMode() {
    const html = document.documentElement;
    
    // Create toggle button if it doesn't exist
    let themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) {
        // Find nav element
        const nav = document.querySelector('.nav') || document.querySelector('nav');
        if (nav) {
            // Create toggle button
            themeToggle = document.createElement('button');
            themeToggle.className = 'theme-toggle';
            themeToggle.id = 'themeToggle';
            themeToggle.setAttribute('aria-label', 'Toggle dark mode');
            themeToggle.innerHTML = `
                <svg class="theme-icon" id="themeIcon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
                <span class="theme-text" id="themeText">Dark</span>
            `;
            nav.appendChild(themeToggle);
        }
    }
    
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', currentTheme);
    if (themeIcon) updateThemeIcon(currentTheme);
    
    // Toggle theme on button click
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            if (themeIcon) updateThemeIcon(newTheme);
        });
    }
    
    function updateThemeIcon(theme) {
        if (themeIcon) {
            if (theme === 'light') {
                themeIcon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
                if (themeText) themeText.textContent = 'Dark';
            } else {
                themeIcon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
                if (themeText) themeText.textContent = 'Light';
            }
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDarkMode);
} else {
    initDarkMode();
}