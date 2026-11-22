// A site's page: confirm the actions that change what visitors get, follow
// the site's log and events as they happen, and keep the part of the page
// that changes up to date.

(function () {
  "use strict";

  var live = document.getElementById("live");
  var feed = document.getElementById("feed");

  // A form with data-confirm asks before it is sent. The listener is on the
  // document, so it also covers forms that a refresh puts in the page.

  document.addEventListener("submit", function (event) {
    var question = event.target.getAttribute("data-confirm");

    if (question && !window.confirm(question)) {
      event.preventDefault();
    }
  });

  if (!live) {
    return;
  }

  // The part of the page that changes is fetched again: when the stream
  // says something happened at the site, every two seconds while a deploy
  // is under way, and every ten seconds while there is no stream to say
  // so. A refresh is put off while the page is hidden, or while the person
  // has the keyboard in that part or has selected text in it, so that
  // nothing is taken from under them.

  var FAST = 2000;
  var SLOW = 10000;
  var streaming = false;
  var timer = null;

  function busy() {
    return live.querySelector('[data-busy="1"]') !== null;
  }

  function inUse() {
    var selection = window.getSelection();
    var selecting =
      selection && !selection.isCollapsed && live.contains(selection.anchorNode);

    return selecting || live.contains(document.activeElement);
  }

  function schedule(soon) {
    window.clearTimeout(timer);

    if (soon !== undefined) {
      timer = window.setTimeout(refresh, soon);
    } else if (busy()) {
      timer = window.setTimeout(refresh, FAST);
    } else if (!streaming) {
      timer = window.setTimeout(refresh, SLOW);
    }
  }

  function refresh() {
    if (document.hidden || inUse()) {
      schedule(FAST);
      return;
    }

    fetch(live.getAttribute("data-url"), { headers: { Accept: "text/html" } })
      .then(function (response) {
        return response.ok ? response.text() : null;
      })
      .then(function (html) {
        if (html !== null && !inUse()) {
          live.innerHTML = html;
        }
      })
      .catch(function () {})
      .then(function () {
        schedule();
      });
  }

  schedule();

  // The log and the events. The page is loaded with the latest of each;
  // the stream sends them again from the start, then whatever follows.

  var log = document.getElementById("log");
  var logEmpty = document.getElementById("log-empty");
  var events = document.getElementById("events");
  var eventsEmpty = document.getElementById("events-empty");
  var feedState = document.getElementById("feed-state");
  var LOG_LINES_KEPT = 500;
  var EVENTS_KEPT = 50;

  if (!feed || !log || !events) {
    return;
  }

  function atEnd() {
    return log.scrollTop + log.clientHeight >= log.scrollHeight - 4;
  }

  function addLine(line) {
    var follow = atEnd();
    var lines = log.textContent === "" ? [] : log.textContent.split("\n");

    lines.push(line);
    log.textContent = lines.slice(-LOG_LINES_KEPT).join("\n");
    logEmpty.hidden = true;

    if (follow) {
      log.scrollTop = log.scrollHeight;
    }
  }

  function cell(text, className) {
    var made = document.createElement("td");

    made.textContent = text;

    if (className) {
      made.className = className;
    }

    return made;
  }

  function when(unixMs) {
    var months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" ");
    var date = new Date(unixMs);
    var two = function (number) {
      return (number < 10 ? "0" : "") + number;
    };

    return (
      date.getUTCDate() + " " + months[date.getUTCMonth()] + " " + two(date.getUTCHours()) + ":" +
      two(date.getUTCMinutes()) + ":" + two(date.getUTCSeconds()) + " UTC"
    );
  }

  // The newest event is the first row. An event the page already shows,
  // as after the stream is opened again, is not added twice.

  function addEvent(event) {
    if (events.querySelector('[data-sequence="' + event.sequence + '"]')) {
      return;
    }

    var row = document.createElement("tr");
    var type = document.createElement("code");
    var typeCell = document.createElement("td");

    type.textContent = event.type;
    typeCell.appendChild(type);
    row.setAttribute("data-sequence", event.sequence);
    row.appendChild(cell(when(event.time), "nowrap"));
    row.appendChild(typeCell);
    row.appendChild(cell(event.subject));
    row.appendChild(cell(event.message, event.level === "error" ? "error" : ""));

    // Events arrive oldest first, so each goes above those before it,
    // wherever its sequence number puts it.

    var before = null;

    Array.prototype.some.call(events.children, function (existing) {
      if (Number(existing.getAttribute("data-sequence")) < event.sequence) {
        before = existing;
        return true;
      }

      return false;
    });

    events.insertBefore(row, before);
    eventsEmpty.hidden = true;

    while (events.children.length > EVENTS_KEPT) {
      events.removeChild(events.lastElementChild);
    }
  }

  log.scrollTop = log.scrollHeight;

  if (!window.EventSource) {
    return;
  }

  var stream = new EventSource(feed.getAttribute("data-stream"));

  stream.addEventListener("open", function () {
    streaming = true;
    feedState.textContent = "following";
    schedule();
  });

  stream.addEventListener("log-reset", function () {
    log.textContent = "";
  });

  stream.addEventListener("log", function (message) {
    addLine(message.data);
  });

  stream.addEventListener("event", function (message) {
    addEvent(JSON.parse(message.data));
  });

  stream.addEventListener("changed", function () {
    schedule(300);
  });

  // The browser opens a stream that drops again by itself. One that was
  // refused, as where the hub cannot stream, is closed for good, and the
  // page goes back to asking.

  stream.addEventListener("error", function () {
    streaming = false;
    feedState.textContent = stream.readyState === EventSource.CLOSED ? "" : "connecting again";
    schedule();
  });
})();
