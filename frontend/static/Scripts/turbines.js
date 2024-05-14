document.addEventListener('DOMContentLoaded', () => {
    let canvas = document.getElementById('turbineCanvas');
    let ctx = canvas.getContext('2d');
    let footer = document.getElementById('footer');

    function resizeCanvas() {
        canvas.width = footer.clientWidth / 50;
        canvas.height = footer.clientHeight;
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function fetchLCTData() {
        fetch('/getlctdata')
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to fetch fault data');
                }
            })
            .then(data => {
                lctData = data;
                console.log('Fetched lct data:', lctData);
            })
            .catch(error => {
                console.error('Error fetching fault data:', error);
            });
    }

    function drawTurbineStem() {
        let stemHeight = canvas.height * 0.4;
        ctx.fillStyle = 'white';
        ctx.fillRect(canvas.width / 2 - 5, canvas.height - stemHeight, 10, stemHeight);
    }

    function drawTurbineBlades(angle) {
        let centerX = canvas.width / 2;
        let centerY = canvas.height - (canvas.height * 0.2);
        let bladeLength = 50;

        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle);
        ctx.fillStyle = 'white';

        for (let i = 0; i < 3; i++) {
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(bladeLength, 10);
            ctx.lineTo(bladeLength, -10);
            ctx.closePath();
            ctx.fill();
            ctx.rotate((2 * Math.PI) / 3); // Rotate 120 degrees for each blade
        }

        ctx.restore();
    }

    let angle = 0;
    const rotationSpeed = 0.02; // Adjust to change the speed of rotation

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawTurbineStem();
        drawTurbineBlades(angle);
        angle += rotationSpeed;
        requestAnimationFrame(draw);
    }

    draw();
});