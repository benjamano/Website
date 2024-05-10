document.addEventListener('DOMContentLoaded', function() {
    const styleSwitch = document.getElementById('styleSwitch');
    const stylesheet = document.getElementById('stylesheet');

    styleSwitch.addEventListener('change', function() {
        if (styleSwitch.checked) {
            stylesheet.href = '/static/nostalgia.css';
        } else {
            stylesheet.href = '/static/styles.css';
        }
    });
});