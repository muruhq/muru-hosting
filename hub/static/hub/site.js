// A site's page: confirm the actions that change what visitors get, and keep
// the part of the page that changes up to date.

(function () {
  "use strict";

  var live = document.getElementById("live");

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

  // Refresh often while a deploy is under way, and slowly otherwise. A
  // refresh is skipped while the page is hidden, or while the person has
  // the keyboard in the part that would be replaced or has selected text
  // in it, so that nothing is taken from under them.

  var FAST = 2000;
  var SLOW = 10000;

  function busy() {
    return live.querySelector('[data-busy="1"]') !== null;
  }

  function inUse() {
    var selection = window.getSelection();
    var selecting =
      selection && !selection.isCollapsed && live.contains(selection.anchorNode);

    return selecting || live.contains(document.activeElement);
  }

  function schedule() {
    window.setTimeout(refresh, busy() ? FAST : SLOW);
  }

  function refresh() {
    if (document.hidden || inUse()) {
      schedule();
      return;
    }

    fetch(live.getAttribute("data-url"), { headers: { Accept: "text/html" } })
      .then(function (response) {
        return response.ok ? response.text() : null;
      })
      .then(function (html) {
        if (html !== null && !inUse()) {
          var log = live.querySelector(".log");
          var atEnd = !log || log.scrollTop + log.clientHeight >= log.scrollHeight - 4;
          var top = log ? log.scrollTop : 0;

          live.innerHTML = html;
          showLogEnd(atEnd, top);
        }
      })
      .catch(function () {})
      .then(schedule);
  }

  // The log reads from its newest lines, and stays where the person
  // scrolled it to across a refresh.

  function showLogEnd(atEnd, top) {
    var log = live.querySelector(".log");

    if (log) {
      log.scrollTop = atEnd ? log.scrollHeight : top;
    }
  }

  showLogEnd(true, 0);
  schedule();
})();
