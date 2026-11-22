// The hello site's game, opened by clicking the logo five times.
//
// Requests arrive at the edge and wait in its queue. Send each to a worker
// that is free, before the queue overflows. Partway through, a green
// release starts beside the blue one: switch traffic to it once its
// workers are ready, and no request is dropped.

(function () {
  "use strict";

  var logo = document.getElementById("logo");
  var section = document.getElementById("game-section");
  var canvas = document.getElementById("game");
  var start = document.getElementById("game-start");
  var status = document.getElementById("game-status");
  var controls = document.getElementById("game-controls");

  if (!logo || !section || !canvas || !canvas.getContext) {
    return;
  }

  // Opening it.

  var CLICKS_TO_OPEN = 5;
  var clicks = 0;

  logo.addEventListener("click", function () {
    clicks += 1;

    if (clicks === CLICKS_TO_OPEN) {
      section.hidden = false;
      draw();
      start.focus();
    }
  });

  // The game.

  var context = canvas.getContext("2d");
  var WIDTH = 640;
  var HEIGHT = 300;
  var WORKERS = 3;
  var QUEUE_LIMIT = 8;
  var GREEN_AFTER = 12;
  var WARMING = 5;
  var SERVICE = { blue: 1.7, green: 1.1 };

  var queue, served, workers, green, serving, playing, last, untilNext, banner;

  function colour(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function makeWorkers(release) {
    var made = [];

    for (var index = 0; index < WORKERS; index += 1) {
      made.push({ release: release, busy: 0 });
    }

    return made;
  }

  function reset() {
    queue = 0;
    served = 0;
    workers = makeWorkers("blue");
    green = null;
    serving = "blue";
    untilNext = 1;
    banner = "";
  }

  // Requests arrive more often the more have been served.

  function gap() {
    return Math.max(0.42, 1.25 - served * 0.02);
  }

  function say(text) {
    status.textContent = text;
  }

  function progress() {
    var text = served + " served, " + queue + " of " + QUEUE_LIMIT + " waiting.";

    return banner ? banner + " " + text : text;
  }

  function end(text) {
    playing = false;
    controls.hidden = true;
    start.hidden = false;
    start.textContent = "Play again";
    say(text);
    start.focus();
  }

  // Send the request at the head of the queue to a worker of the release
  // that serves. A busy worker takes nothing.

  function route(index) {
    var worker = workers[index];

    if (!playing || queue === 0 || worker.busy > 0) {
      return;
    }

    queue -= 1;
    worker.busy = SERVICE[worker.release];
    say(progress());
  }

  function switchTraffic() {
    if (!playing || green === null || serving === "green") {
      return;
    }

    if (green.warming > 0) {
      end(
        "You switched traffic to a release that was not ready, and its requests were dropped. " +
          served + " served."
      );
      return;
    }

    // The blue workers finish what they hold and take nothing more.

    serving = "green";
    green.draining = workers;
    workers = green.workers;
    banner = "Traffic switched to green without dropping a request.";
    document.getElementById("game-switch").hidden = true;
    say(progress());
  }

  function step(seconds) {
    untilNext -= seconds;

    if (untilNext <= 0) {
      queue += 1;
      untilNext = gap();

      if (queue > QUEUE_LIMIT) {
        end("The queue overflowed. " + served + " served.");
        return;
      }

      say(progress());
    }

    workers.concat(green && green.draining ? green.draining : []).forEach(function (worker) {
      if (worker.busy > 0) {
        worker.busy = Math.max(0, worker.busy - seconds);

        if (worker.busy === 0) {
          served += 1;
          say(progress());
        }
      }
    });

    if (green === null && served >= GREEN_AFTER) {
      green = { warming: WARMING, workers: makeWorkers("green"), draining: null };
      banner = "Release green is starting: switch traffic when its workers are ready.";
      document.getElementById("game-switch").hidden = false;
      say(progress());
    } else if (green !== null && green.warming > 0) {
      green.warming = Math.max(0, green.warming - seconds);

      if (green.warming === 0) {
        banner = "Green is ready: switch traffic.";
        say(progress());
      }
    }
  }

  // The picture: the edge and its queue on the left, the workers of each
  // release in a column on the right.

  var BOX = { width: 150, height: 58, gap: 18, top: 44 };

  function column(release) {
    return release === "blue" ? 250 : 440;
  }

  function drawWorkers(list, release, label) {
    var x = column(release);
    var shade = colour(release === "blue" ? "--accent" : "--green");

    context.fillStyle = colour("--muted");
    context.fillText(label, x, 26);

    list.forEach(function (worker, index) {
      var y = BOX.top + index * (BOX.height + BOX.gap);

      context.strokeStyle = shade;
      context.lineWidth = 2;
      context.strokeRect(x, y, BOX.width, BOX.height);

      if (worker.busy > 0) {
        context.fillStyle = shade;
        context.fillRect(x, y, BOX.width * (worker.busy / SERVICE[worker.release]), BOX.height);
      }

      context.fillStyle = colour("--text");
      context.fillText(release + " " + (index + 1), x + 10, y + 34);
    });
  }

  function draw() {
    context.clearRect(0, 0, WIDTH, HEIGHT);
    context.font = "15px system-ui, sans-serif";

    context.fillStyle = colour("--muted");
    context.fillText("edge", 30, 26);
    context.strokeStyle = colour("--line");
    context.lineWidth = 2;
    context.strokeRect(30, BOX.top, 150, 210);

    context.fillStyle = queue >= QUEUE_LIMIT - 1 ? colour("--warn") : colour("--text");

    for (var waiting = 0; waiting < Math.min(queue, QUEUE_LIMIT); waiting += 1) {
      context.beginPath();
      context.arc(58 + (waiting % 4) * 32, BOX.top + 190 - Math.floor(waiting / 4) * 32, 10, 0, Math.PI * 2);
      context.fill();
    }

    if (serving === "blue") {
      drawWorkers(workers, "blue", "release blue, serving");

      if (green !== null) {
        var ready = green.warming === 0;

        drawWorkers(green.workers, "green", ready ? "release green, ready" : "release green, starting");
      }
    } else {
      drawWorkers(green.draining, "blue", "release blue, draining");
      drawWorkers(workers, "green", "release green, serving");
    }
  }

  function frame(now) {
    if (!playing) {
      draw();
      return;
    }

    // A long gap between frames, as after the tab was hidden, moves nothing.

    var seconds = Math.min(0.05, (now - last) / 1000);

    last = now;
    step(seconds);
    draw();
    window.requestAnimationFrame(frame);
  }

  function play() {
    reset();
    playing = true;
    start.hidden = true;
    controls.hidden = false;
    document.getElementById("game-switch").hidden = true;
    say(progress());
    controls.querySelector("button").focus();
    last = performance.now();
    window.requestAnimationFrame(frame);
  }

  // Controls: the buttons under the picture, the keys 1 to 3 and S, and a
  // click or a tap on a worker of the release that serves.

  start.addEventListener("click", play);

  controls.addEventListener("click", function (event) {
    var worker = event.target.getAttribute("data-worker");

    if (worker !== null) {
      route(Number(worker));
    } else if (event.target.id === "game-switch") {
      switchTraffic();
    }
  });

  section.addEventListener("keydown", function (event) {
    if (event.key >= "1" && event.key <= String(WORKERS)) {
      route(Number(event.key) - 1);
    } else if (event.key === "s" || event.key === "S") {
      switchTraffic();
    }
  });

  canvas.addEventListener("pointerdown", function (event) {
    var box = canvas.getBoundingClientRect();
    var x = ((event.clientX - box.left) / box.width) * WIDTH;
    var y = ((event.clientY - box.top) / box.height) * HEIGHT;
    var left = column(serving);

    if (x < left || x > left + BOX.width) {
      return;
    }

    for (var index = 0; index < WORKERS; index += 1) {
      var top = BOX.top + index * (BOX.height + BOX.gap);

      if (y >= top && y <= top + BOX.height) {
        route(index);
      }
    }
  });

  canvas.width = WIDTH;
  canvas.height = HEIGHT;
  reset();
})();
