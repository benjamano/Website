let canvas = document.getElementById('pongCanvas');
let ctx = canvas.getContext('2d');
let ballRadius = 2;
let x = canvas.width / 2;
let y = canvas.height / 2;
let dx = 2;
let dy = 0.2;
let paddleHeight = (canvas.height / 3 )
let paddleWidth = 2 * (canvas.width / 100);
let paddle1Y = (canvas.height / 2) - (paddleHeight / 2);
let paddle2Y = (canvas.height / 2) - (paddleHeight / 2);
let aiSpeed = 0.5;

// Function to set canvas size based on viewport dimensions
function resizeCanvas() {
    canvas.width = window.innerWidth * 0.99;
    canvas.height = window.innerHeight * 0.10;
}

// Call resizeCanvas initially and on window resize
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// AI control for both paddles
function aiControl() {
    let paddle1Center = paddle1Y + (paddleHeight / 2);
    let paddle2Center = paddle2Y + (paddleHeight / 2);
    if (paddle1Center < y - (canvas.height * 0.0583)) { // Scale AI control threshold
        paddle1Y += aiSpeed;
    } else if (paddle1Center > y + (canvas.height * 0.0583)) {
        paddle1Y -= aiSpeed;
    }
    if (paddle2Center < y - (canvas.height * 0.0583)) {
        paddle2Y += aiSpeed;
    } else if (paddle2Center > y + (canvas.height * 0.0583)) {
        paddle2Y -= aiSpeed;
    }
}

// Drawing functions
function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, (ballRadius) * (canvas.width / 800), 0, Math.PI * 2); // Scale ball radius
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
}

function drawPaddle1() {
    ctx.beginPath();
    ctx.rect(0, paddle1Y, paddleWidth, paddleHeight);
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
}

function drawPaddle2() {
    ctx.beginPath();
    ctx.rect(canvas.width - paddleWidth, paddle2Y, paddleWidth, paddleHeight);
    ctx.fillStyle = 'white';
    ctx.fill();
    ctx.closePath();
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBall();
    drawPaddle1();
    drawPaddle2();
    aiControl();

    // Ball collision with top and bottom walls
    if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
        dy = -dy;
    }
    // Ball collision with paddles
    if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
        dy = -dy; // Reverse the vertical direction
    
        // Adjust the ball's position to ensure it stays within the canvas boundaries
        if (y + dy > canvas.height - ballRadius) {
            y = canvas.height - ballRadius;
        } else if (y + dy < ballRadius) {
            y = ballRadius;
        }
    }

    // Ball goes out of bounds
    if (x + dx > canvas.width - (canvas.width * 0.001) || x + dx < (canvas.width * 0.001)) { // 
        // Reverse ball direction
        dx = -dx;
    }

    x += dx;
    y += dy;

    requestAnimationFrame(draw);
}

draw();
