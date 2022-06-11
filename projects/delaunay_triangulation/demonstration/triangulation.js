var canvas;
var ctx;
var interval;

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
    
    var buffer = 100;
    var points = Array.apply(null, Array(100)).map(function () {
        return {
            position: [Math.random() * (innerWidth + 2 * buffer) - buffer, Math.random() * (innerHeight + 2 * buffer) - buffer],
            velocity: [Math.random() - 0.5, Math.random() - 0.5]
        }
    });
    
    interval = setInterval(() => update(points, buffer), 20);
}

function update(points, buffer) {
    points.forEach(function(point, i) {
        let w = (innerWidth + 2 * buffer);
        let h = (innerHeight + 2 * buffer);
        point.position[0] = ((point.position[0] + point.velocity[0] + buffer) % w + w) % w - buffer;
        point.position[1] = ((point.position[1] + point.velocity[1] + buffer) % h + h) % h - buffer;
    });

    let triangles = doTriangulation(points, buffer);

    triangles.forEach(function(triangle) {
        ctx.fillStyle = blend([115, 240, 95], [11, 113, 88], triangle.meanHeight());
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
        pointsIncluded.sort(function (a, b) { return Math.atan2(a.position[1] - point.position[1], a.position[0] - point.position[0]) - Math.atan2(b.position[1] - point.position[1], b.position[0] - point.position[0]) });

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