// A run's page: follow what the run writes until it ends, then load the
// page again to show how it ended.

(function () {
  "use strict";

  var log = document.getElementById("log");
  var empty = document.getElementById("log-empty");

  document.addEventListener("submit", function (event) {
    var question = event.target.getAttribute("data-confirm");

    if (question && !window.confirm(question)) {
      event.preventDefault();
    }
  });

  if (!log) {
    return;
  }

  log.scrollTop = log.scrollHeight;

  var url = log.getAttribute("data-stream");

  if (!url) {
    return;
  }

  // Without a stream, as where the hub cannot stream, the page is loaded
  // again every few seconds while the run is under way.

  function reloadSoon(after) {
    window.setTimeout(function () {
      window.location.reload();
    }, after);
  }

  if (!window.EventSource) {
    reloadSoon(3000);
    return;
  }

  var stream = new EventSource(url);

  stream.addEventListener("log-reset", function () {
    log.textContent = "";
  });

  stream.addEventListener("log", function (message) {
    var follow = log.scrollTop + log.clientHeight >= log.scrollHeight - 4;

    log.textContent += (log.textContent === "" ? "" : "\n") + message.data;
    empty.hidden = true;

    if (follow) {
      log.scrollTop = log.scrollHeight;
    }
  });

  stream.addEventListener("finished", function () {
    stream.close();
    reloadSoon(500);
  });

  stream.addEventListener("error", function () {
    if (stream.readyState === EventSource.CLOSED) {
      reloadSoon(3000);
    }
  });
})();
