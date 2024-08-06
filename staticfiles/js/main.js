document.addEventListener('DOMContentLoaded', () => {
    const switcherTheme = document.querySelector('.main__check');
    const root = document.documentElement;
    const storedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const initialTheme = storedTheme || systemPrefersDark;
    root.setAttribute('data-theme', initialTheme);
    if (initialTheme === 'dark') {
        switcherTheme.checked = true;
    }
    switcherTheme.addEventListener('change', () => {
        const isChecked = switcherTheme.checked;
        const newTheme = isChecked ? 'dark' : 'light';
        root.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateSwitcher(isChecked);
    });
    function updateSwitcher(isChecked) {
        const mainOption = document.querySelector('.main__option');
        if (isChecked) {
            mainOption.style.transform = 'translateX(100%)';
        } else {
            mainOption.style.transform = 'translateX(0)';
        }
    }

    updateSwitcher(initialTheme === 'dark');
});