// Initial function

const btnGroup = document.querySelector("#btn-group");
const clear = document.querySelector(".btn#clear");
const bar = document.querySelector("#bar");
const SIZE = 580;
var sendLock = true;
var drawMode = true;
var socket;

new p5((p) => {
  p.setup = function () {
    p.createCanvas(SIZE, SIZE);
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
  let newData = new Array(SIZE * SIZE * 4);
  let data = document
    .getElementById("drawable-area")
    .firstChild.getContext("2d")
    .getImageData(0, 0, SIZE * 2, SIZE * 2).data;
  for (let i = 0, j = 0; j < SIZE * SIZE * 16; j += 4) {
    newData[i++] = data[j];
  }
  return JSON.stringify(newData);
}

function changeBar(data) {
  now = (100 * data[1] / data[2]) + "%";
  bar.style.width = bar.innerText = now;
  $(".lockBoard").text(data[0]+"...");
}

// Listen function

$("button").on("click", function () {
  $(this).toggleClass("is-active");
});

$(document).ready(() => {
  socket = io.connect();
  sendLock = false;
  
  socket.on('progress', (data) => {
    changeBar(data);
  });

  socket.on('finish', (data) => {
    $("#lockBoard").modal("hide");
    sendLock = false;
    // show output image
  });
});

btnGroup.addEventListener("click", (e) => {
  if (e.target.id == "pen" || e.target.id == "erase") {
    drawMode = e.target.id == "pen" ? true : false;
    let x = e.target.id == "pen" ? "erase" : "pen";
    btnGroup.children[x].classList.remove("active");
    e.target.classList.add("active");
  } else if (e.target.id == "random") {
    console.log("random");
  } else if (e.target.id == "send") {
    if (sendLock) {
      console.log("foo");
    } else {
      $("#lockBoard").modal("show");
      changeBar(["Pending", 0, 10]);
      sendLock = true;
      let data = DataTransport();
      let url = document.URL + "generate";
      $.post(url, data, (res) => {
        if (res == "OK") {

        } else {
          sendLock = false;
        }
      });
    }
  }
});
