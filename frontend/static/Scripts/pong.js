// window.addEventListener('DOMContentLoaded', (event) => {
//     const footerWidth = document.getElementById('footer').offsetWidth;
//     const canvas = document.getElementById('pongCanvas');
//     canvas.width = footerWidth;
// });

// window.addEventListener('DOMContentLoaded', (event) => {
//     const footerHeight = document.getElementById('footer').offsetHeight;
//     const canvas = document.getElementById('pongCanvas');
//     canvas.height = footerHeight;
// });

let canvas = document.getElementById('pongCanvas');
let ctx = canvas.getContext('2d');
let ballRadius = 1;
let x = canvas.width / 2;
let y = canvas.height / 2;
let dx = 0.5;
let dy = 0.1;
let paddleHeight = canvas.height / 2;
let paddleWidth = canvas.width / 240;
let paddle1Y = canvas.height /2 - paddleHeight / 2;
let paddle2Y = canvas.height /2 - paddleHeight / 2;
let aiSpeed = 1;

function drawBall(){
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle1(){
    ctx.beginPath();
    ctx.rect(0, paddle1Y, paddleWidth, paddleHeight);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.closePath();
}

function drawPaddle2(){
    ctx.beginPath();
    ctx.rect(canvas.width - paddleWidth, paddle2Y, paddleWidth, paddleHeight);
    ctx.fillStyle = "white";
    ctx.fill();
    ctx.closePath();
}


function aiControl() {

    let paddle1Center = paddle1Y + paddleHeight / 2;
    let paddle2Center = paddle2Y + paddleHeight / 2;
    if (paddle1Center < y - 2) {
        paddle1Y += aiSpeed;
    } else if (paddle1Center > y + 5) {
        paddle1Y -= aiSpeed;
    }
    if (paddle2Center < y - 1) {
        paddle2Y += aiSpeed;
    } else if (paddle2Center > y + 5) {
        paddle2Y -= aiSpeed;
    }
}

function draw(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBall();
    drawPaddle1();
    drawPaddle2();
    aiControl();

    if (y + dy > canvas.height - ballRadius || y + dy < ballRadius){
        dy = -dy;
    }

    if (x + dx > canvas.width - ballRadius - paddleWidth && y > paddle2Y && y < paddle2Y + paddleHeight ||
        x + dx < ballRadius + paddleWidth && y > paddle1Y && y < paddle1Y + paddleHeight) {
        dx = -dx;
    }

    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
        x = canvas.width / 2;
        y = canvas.height / 2;
        paddle1Y = canvas.height / 2 - paddleHeight / 2;
        paddle2Y = canvas.height / 2 - paddleHeight / 2;
        dx = -dx;
    }

    x += dx;
    y += dy;

    requestAnimationFrame(draw);

}

draw();