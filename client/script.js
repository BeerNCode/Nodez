var socket;

const CONTROLLER_STATE_UPDATE = "update";
const CONTROLLER_STATE_UPDATE_FREQUENCY = 100;
const IP_ADDRESS = "localhost";
const PORT = "5000";

let canvas;
let buttons;
let button_list;

function setup() {
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.parent('sketch-div');

    buttons = {
        a: new Button("A", 0.625, 0.5),
        b: new Button("B", 0.75, 0.75),
        c: new Button("C", 0.875, 0.5),
        d: new Button("D", 0.75, 0.25),
        up: new Button("🡅", 0.25, 0.25),
        down: new Button("🡇", 0.25, 0.75),
        left: new Button("🡄", 0.125, 0.5),
        right: new Button("🡆", 0.375, 0.5),
    }
    button_list = Object.values(buttons);
    background(51);
    textAlign(CENTER, CENTER);

    setInterval(sendControllerState, CONTROLLER_STATE_UPDATE_FREQUENCY);
}

function sendControllerState() {
    if (!socket.connected) return;
    let state = {
        a: buttons.a.is_pressed(touches),
        b: buttons.b.is_pressed(touches),
        c: buttons.c.is_pressed(touches),
        d: buttons.d.is_pressed(touches),
        up: buttons.up.is_pressed(touches),
        down: buttons.down.is_pressed(touches),
        left: buttons.left.is_pressed(touches),
        right: buttons.right.is_pressed(touches),
    }
    console.log("Sending state update..");

    socket.emit(CONTROLLER_STATE_UPDATE, state);
}

function mousePressed() {
    console.log("Trying to connect to http://"+IP_ADDRESS+":"+PORT)
    socket = io.connect('http://' + IP_ADDRESS + ':' + PORT);
    //console.log("State is: "+socket.connected);
}

function draw() {
    fill(20)

    for(let i=0;i<button_list.length;i++) {
        button_list[i].draw();
    }
    textSize(width / 20);
    if (socket.connected) {
        fill(0, 255, 0);
        text("Connected", width * 0.5, height * 0.1);
    }
    else {
        fill(255, 0, 0);
        text("Not Connected", width * 0.5, height * 0.1);
    }
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

class Button {

    constructor(name, x, y, radius) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.radius = radius;
    }

    is_pressed(touches) {
        let r2 = this.radius * this.radius;
        for(let i=0;i<touches.length;i++) {
            let touch = touches[i];
            let dx = touch.x - this.x; 
            let dy = touch.y - this.y; 
            if (dx * dx + dy * dy < r2) return true;
        }
        return false;
    }

    draw() {
        fill(200)
        let dx = width * this.x;
        let dy = height * this.y;

        ellipse(dx, dy, 100, 100);
        fill(255);
        stroke(0);
        textSize(width / 10);
        text(this.name, dx, dy);
    }
}