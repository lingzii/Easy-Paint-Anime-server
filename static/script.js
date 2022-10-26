// Initial function

const btnGroup = document.querySelector("#btn-group");
const clear = document.querySelector(".btn#clear");
var drawMode = true;

new p5((p) => {
  p.setup = function () {
    p.createCanvas(580, 580);
    p.stroke(255);
    clear.addEventListener("click", () => {
      drawMode = true;
      p.clear();
    });
  };
  p.draw = function () {
    if (p.mouseIsPressed) {
      drawMode ? null : p.erase();
      p.strokeWeight(drawMode ? 2 : 30);
      p.line(p.mouseX, p.mouseY, p.pmouseX, p.pmouseY);
      p.noErase();
    }
  };
}, "drawable-area");

// Method function

function DataTransport() {
  let area = document.getElementById("drawable area").firstChild;
  let img = area.getContext("2d").getImageData(0, 0, 1024, 1024);
  // return JSON.stringify(img);
  return "foo";
}

// Listen function

$(document).ready(() => {
  var socket = io.connect();
  document.getElementById("generate").addEventListener("click", () => {
    socket.emit("test", DataTransport());
    console.log("foo");
  });
});

btnGroup.addEventListener("click", (e) => {
  if (e.target.id == "pen" || e.target.id == "erase") {
    drawMode = e.target.id == "pen" ? true : false;
    let x = e.target.id == "pen" ? "erase" : "pen";
    btnGroup.children[x].classList.remove("active");
    e.target.classList.add("active");
  }
});

// document.getElementById("generate").addEventListener("click", () => {
//   $.post(`${document.URL}generate`, getImageData(), (result) => {
//     console.log(result);
//   });
// });

$("button").on("click", function () {
  $(this).toggleClass("is-active");
});
