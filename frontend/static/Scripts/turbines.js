let canvas = document.getElementById('turbineCanvas');
let ctx = canvas.getContext('2d');
let stemHeight = canvas.height * 0.4;

let lctData = "";

let footer = document.getElementById('footer');

function resizeCanvas() {
    canvas.width = footer.clientWidth;
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
    ctx.beginPath();
    ctx.rect(canvas.width - stemHeight);
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
}

function draw(){
    drawTurbineStem();
    
    requestAnimationFrame(draw);
}


draw();
