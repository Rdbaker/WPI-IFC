var current_version = null;

$.get('/status').done(function(res) {
  current_version = res.version;
});

function closeHandler() {
  window.location.reload();
}

function notifyNewVersion() {
  var n = noty({
    text: 'A new version is available, please reload the page! <button class="btn btn-sm btn-info"><i class="fa fa-refresh" aria-hidden="true"></i> Refresh</button>',
    layout: 'top',
    theme: 'relax',
    type: 'error',
    animation: {
      open: {height: 'toggle'}, // jQuery animate function property object
      close: {height: 'toggle'}, // jQuery animate function property object
      easing: 'swing', // easing
      speed: 500 // opening & closing animation speed
    },
    callback: { onCloseClick: closeHandler }
  });
  clearInterval(pid);
}

function checkVersion() {
  $.get('/status').done(function(res) {
    if(res.version !== current_version) {
      notifyNewVersion();
    }
  })
}

var pid = setInterval(checkVersion, 5000);
