var rotationSpeed = 0.001;

document.addEventListener('DOMContentLoaded', () => {
    let canvas = document.getElementById('turbineCanvas');
    let ctx = canvas.getContext('2d');
    let footer = document.getElementById('footer');

    function resizeCanvas() {
        canvas.width = footer.clientWidth * 0.5;
        canvas.height = footer.clientHeight;
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function drawTurbineStem() {
        let stemHeight = canvas.height * 0.5;
        ctx.fillStyle = 'white';
        ctx.fillRect(canvas.width / 2 - 5, canvas.height - stemHeight, 10, stemHeight);
    }

    function drawTurbineCircle() {
        let centerX = canvas.width / 2;
        let centerY = canvas.height - (canvas.height * 0.45);
        let radius = 7;

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
        ctx.fillStyle = 'black';
        ctx.fill();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.closePath();
    }

    function drawTurbineBlades(angle) {
        let centerX = canvas.width / 2;
        let centerY = canvas.height - (canvas.height * 0.47);
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
            ctx.rotate((2 * Math.PI) / 3);
        }

        ctx.restore();
    }

    let angle = 0;
    let numofTurbines = 3;

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let turbineOffset =  -(canvas.width * numofTurbines * 0.06); 

        for (let i = 0; i < numofTurbines; i++) {
            ctx.save();
            ctx.translate(turbineOffset * i, 0);
            drawTurbineStem();
            drawTurbineBlades(angle);
            drawTurbineCircle();
            angle += rotationSpeed;
            ctx.restore();
        }
        requestAnimationFrame(draw);
    }

    draw();
});

function fetchLCTData() {
    return fetch('/getlctdata')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch fault data');
            }
        })
        .then(data => {
            //console.log('Fetched lct data:', data);
            return data;
        })
        .catch(error => {
            console.error('Error fetching fault data:', error);
        });
}

fetchLCTData()
    .then(lctdata => {

        for (const record of lctdata) {
            if (record.type == "Wind") {
                rotationSpeed += record.exportrating_mw * 0.003;
            }
        }
    })
    .catch(error => {
        console.error('Error fetching fault data:', error);
    });