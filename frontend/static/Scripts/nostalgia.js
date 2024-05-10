document.addEventListener('DOMContentLoaded', function() {
    const styleSwitch = document.getElementById('styleSwitch');
    const stylesheet = document.getElementById('stylesheet');

    styleSwitch.addEventListener('change', function() {
        if (styleSwitch.checked) {
            stylesheet.href = '/frontend/static/nostalgia.css';
        } else {
            stylesheet.href = '/frontend/static/stylea.css';
        }
    });
});