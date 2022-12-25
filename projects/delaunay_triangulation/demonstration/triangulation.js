var canvas;
var ctx;
var interval;
var speed;
var numPoints;
var topColour;
var bottomColour;
var badParams = false;

class Triangle {
    constructor(points) {
        this.points = points.slice();
        this.sortACW();
    }

    sortACW() {
        if ((this.points[1].position[0] - this.points[0].position[0]) * (this.points[2].position[1] - this.points[0].position[1]) - (this.points[2].position[0] - this.points[0].position[0]) * (this.points[1].position[1] - this.points[0].position[1]) < 0) {
            this.points = [this.points[1], this.points[0], this.points[2]]
        }
    }

    inCircumcircle(point) {
        let ax = this.points[0].position[0] - point.position[0];
        let ay = this.points[0].position[1] - point.position[1];
        let bx = this.points[1].position[0] - point.position[0];
        let by = this.points[1].position[1] - point.position[1];
        let cx = this.points[2].position[0] - point.position[0];
        let cy = this.points[2].position[1] - point.position[1];
        
        return (ax * ax + ay * ay) * (bx * cy - cx * by) - (bx * bx + by * by) * (ax * cy - cx * ay) + (cx * cx + cy * cy) * (ax * by - bx * ay) > 0;
    }

    meanHeight() {
        return Math.max(Math.min(this.points.reduce(function(a, p) { return a + p.position[1] }, 0) / (this.points.length * canvas.height), 1), 0);
    }
}

window.onload = () => {
    createCanvas();
    start();
}

window.onresize = () => {
    clearInterval(interval);
    start();
}

function createCanvas() {
    canvas = document.createElement("canvas");
    canvas.width = innerWidth;
    canvas.height = innerHeight - 1;
    ctx = canvas.getContext("2d");

    document.body.insertBefore(canvas, document.body.childNodes[0]);
}

function start() {
    canvas.width = innerWidth;
    canvas.height = innerHeight - 1;

    getURLParams();

    var buffer = 100;
    var points = Array.apply(null, Array(numPoints)).map(function () {
        return {
            position: [Math.random() * (innerWidth + 2 * buffer) - buffer, Math.random() * (innerHeight + 2 * buffer) - buffer],
            velocity: [(Math.random() - 0.5) * (speed / 100), (Math.random() - 0.5) * (speed / 100)]
        }
    });
    
    if (!badParams) {
        interval = setInterval(() => update(points, buffer), 20);
    } else {
        drawBadParamsMessage();
    }
}

function update(points, buffer) {
    points.forEach(function(point) {
        let w = (innerWidth + 2 * buffer);
        let h = (innerHeight + 2 * buffer);
        point.position[0] = ((point.position[0] + point.velocity[0] + buffer) % w + w) % w - buffer;
        point.position[1] = ((point.position[1] + point.velocity[1] + buffer) % h + h) % h - buffer;
    });

    let triangles = doTriangulation(points, buffer);

    triangles.forEach(function(triangle) {
        ctx.fillStyle = blend(bottomColour, topColour, triangle.meanHeight());
        ctx.beginPath();
        ctx.moveTo(triangle.points[2].position[0], triangle.points[2].position[1]);
        triangle.points.forEach(function(point) {
            ctx.lineTo(point.position[0], point.position[1]);
        });
        ctx.closePath();
        ctx.fill();
    });


}

function doTriangulation(points, buffer) {
    points = [
        { position: [-10 - buffer, -10 - buffer], velocity: [0, 0] },
        { position: [canvas.width + 10 +  buffer, -10 - buffer], velocity: [0, 0] },
        { position: [-10 - buffer, canvas.height + 10 + buffer], velocity: [0, 0] },
        { position: [canvas.width + 10 + buffer, canvas.height + 10 + buffer], velocity: [0, 0] }
    ].concat(points);

    let triangles = [new Triangle(points.slice(0, 3)), new Triangle(points.slice(1, 4))];
    points.slice(4).forEach(function(point) {
        let trianglesToRemove = [];
        triangles.forEach(function(triangle) {
            if (triangle.inCircumcircle(point)) {
                trianglesToRemove.push(triangle);
            }
        });

        let pointsIncluded = [];
        trianglesToRemove.forEach(function(triangle) {
            triangle.points.forEach(function(p) {
                pointsIncluded.push(p);
            });
            triangles.splice(triangles.indexOf(triangle), 1);
        });

        pointsIncluded = [...new Set(pointsIncluded)];
        pointsIncluded.sort(function (a, b) {
            return (
                Math.atan2(a.position[1] - point.position[1], a.position[0] - point.position[0]) - 
                Math.atan2(b.position[1] - point.position[1], b.position[0] - point.position[0])
            )
        });

        pointsIncluded.forEach(function(p, i) {
            triangles.push(new Triangle([point, p, pointsIncluded.at(i - 1)]));
        });
    });

    return triangles
}

function blend(colour1, colour2, blendValue) {
    let r = colour1[0] * blendValue + colour2[0] * (1 - blendValue);
    let g = colour1[1] * blendValue + colour2[1] * (1 - blendValue);
    let b = colour1[2] * blendValue + colour2[2] * (1 - blendValue);

    return "rgb(" + r + "," + g + "," + b + ")";
}

function getURLParams() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    topColour = urlParams.get('top_colour')
    if (topColour !== null) {
        topColour = topColour.split(',').map(i => { return parseInt(i) });

        if (isNaN(topColour[0]) || isNaN(topColour[1]) || isNaN(topColour[2]) || topColour.length != 3) {
            badParams = true;
        }
    }
    else {
        topColour = [11, 113, 88]
    }

    bottomColour = urlParams.get('bottom_colour')
    
    if (bottomColour !== null) {
        bottomColour = bottomColour.split(',').map(i => { return parseInt(i) });

        if (isNaN(bottomColour[0]) || isNaN(bottomColour[1]) || isNaN(bottomColour[2]) || bottomColour.length != 3) {
            badParams = true;
        }
    }
    else {
        bottomColour = [115, 240, 95]
    }

    speed = parseInt(urlParams.get('speed'));
    numPoints = parseInt(urlParams.get('num_points'));

    if (isNaN(speed)) {
        speed = 100;
    }
    if (isNaN(numPoints)) {
        numPoints = 100;
    }
}

function drawBadParamsMessage() {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = "bold 30px Helvetica";
    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.fillText("Bad Colour Parameters", canvas.width / 2, canvas.height / 2);

    let boxSize = [500, 150];
    ctx.strokeStyle = 'red';
    ctx.lineWidth = 10;
    ctx.beginPath();
    ctx.roundRect(canvas.width / 2 - boxSize[0] / 2, canvas.height / 2 - boxSize[1] / 2 - 5, boxSize[0], boxSize[1], 20);
    ctx.stroke();
}