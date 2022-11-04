// Initial function

const bar = document.querySelector("#bar");
const SIZE = 600;
var drawMode = true;
var select;
var socket;

new p5((p) => {
  p.setup = function () {
    p.createCanvas(SIZE, SIZE);
    p.stroke(255);
    $(".btn#clear").click(() => {
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

const validateEmail = (email) => {
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};

function DataTransport() {
  let newData = new Array(SIZE * SIZE);
  let data = document
    .getElementById("drawable-area")
    .firstChild.getContext("2d")
    .getImageData(0, 0, SIZE, SIZE).data;
  for (let i = 0, j = 0; j < SIZE * SIZE * 4; j += 4) {
    newData[i++] = data[j];
  }
  return JSON.stringify(newData);
}

function changeBar(data) {
  let val = (100 * data[1]) / data[2];
  let now = `${Math.round(val)}%`;
  bar.style.width = bar.innerText = now;
  $(".lockBoard").text(data[0] + "...");
}

function imgUri(i) {
  let time = new Date().getTime();
  return `image/${i}.png?t=${time}`;
}

function refreshDisplay() {
  let img = `<img src="${imgUri(select)}" width=600>`;
  $("#display-area").empty();
  $("#display-area").append(img);
}

// Socket function

$(document).ready(() => {
  socket = io.connect();

  $(".carousel").carousel({
    interval: false,
  });

  socket.on("progress", (data) => {
    changeBar(data);
  });

  socket.on("finish", () => {
    let first = $('<div class="row g-4 mb-4"></div>');
    let second = $('<div class="row mb-4"></div>');
    for (let i = 0; i < 10; i++) {
      let card = $('<div class="card" style="width: 12rem;"></div>');
      let area = $('<div class="col"></div>');
      card.append($(`<img src="${imgUri(i)}" data=${i}>`));
      area.append(card);
      i < 5 ? first.append(area) : second.append(area);
    }
    $("div#view-area").empty();
    $("div#view-area").append(first, second);
    select = 0;
    let ls = $("#view-area>div>div>div>img");
    ls.first().parent().addClass("border-primary");
    refreshDisplay();
    $("#lockBoard").modal("hide");
  });
});

// Listen function

$("button").click(() => {
  $(this).toggleClass("is-active");
});

$(".btn#pen").click((e) => {
  $(".btn#erase").removeClass("active");
  e.target.classList.add("active");
  drawMode = true;
});

$(".btn#erase").click((e) => {
  $(".btn#pen").removeClass("active");
  e.target.classList.add("active");
  drawMode = false;
});

$(".btn#train").click((e) => {
  $("#lockBoard").modal("show");
  changeBar(["Pending", 1, 1]);
  let url = document.URL + "training";
  let data = DataTransport();
  $.post(url, data, (res) => {
    if (res != "OK") {
      console.log("error"); // TODO: Error method
    }
  });
});

$(".btn#generate").click(() => {
  $("#lockBoard").modal("show");
  changeBar(["Pending", 1, 1]);
  socket.emit("generate");
});

$(".btn#more").click(() => {
  $("#viewList").modal("show");
});

$(".btn#email").click(() => {
  $("#figure").attr("src", imgUri(select));
  $("#emailBox").modal("show");
});

$("button#send").click(() => {
  let val = $("input#email").val();
  if (!!val && validateEmail(val)) {
    socket.emit("email", [val, select]);
    $("#emailBox").modal("hide");
  } else {
    console.log("error");
  }
});

$("#view-area").click((e) => {
  if (e.target.nodeName == "IMG") {
    select = parseInt($(e.target).attr("data"));
    let ls = $("#view-area>div>div>div>img");
    ls.each((i) => {
      let box = $(ls[i]).parent();
      if (select == i) box.addClass("border-primary");
      else box.removeClass("border-primary");
    });
    refreshDisplay();
    $("#viewList").modal("hide");
  }
});
