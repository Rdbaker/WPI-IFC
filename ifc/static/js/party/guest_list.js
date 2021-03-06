'use strict';

Backbone.$ = $;
// define the base URL for the backbone classes
window.base_url = document.location.pathname;

// see if the party has started
window.partyStarted = $('meta[name=started]').attr('content') === "True";

// see if the party has ended
window.partyEnded = $('meta[name=ended]').attr('content') === "True";

// define the current user
window.me = undefined;
$.get('/users/me').done(function(data) { window.me = data.me; });


// define the base module
window.GuestList = {
  Models: {},
  Collections: {},
  Views: {}
};


// define a common "Broadcaster" class
$(function() {
  function Broadcaster() {}
  var messageElt = $('#message');


  Broadcaster.prototype.flashMessage = function(type, message) {
    messageElt.removeClass();
    messageElt.addClass("row");
    messageElt.addClass("text-center", type);
    messageElt.addClass(type);
    messageElt.text(message);
  };

  Broadcaster.prototype.flashError = function(message) {
    this.flashMessage('bg-danger', message);
  };

  Broadcaster.prototype.flashSuccess = function(message) {
    this.flashMessage('bg-success', message);
  };

  Broadcaster.prototype.flashInfo = function(message) {
    this.flashMessage('bg-info', message);
  };

  Broadcaster.prototype.flashWarning = function(message) {
    this.flashMessage('bg-warning', message);
  };

  window.Broadcaster = new Broadcaster;
});



// kick off the application
$(function() {
  var maleCollection = new GuestList.Collections.GuestCollection(null, { is_male: true });
  var femaleCollection = new GuestList.Collections.GuestCollection(null, { is_male: false });

  var maleView = new GuestList.Views.GuestListView({
    el: $('#male-guest-list'),
    is_male: true,
    collection: maleCollection
  });

  var femaleView = new GuestList.Views.GuestListView({
    el: $('#female-guest-list'),
    is_male: false,
    collection: femaleCollection
  });

  // let's only run this if the party hasn't ended
  if(!window.partyEnded) {
    var maleAddView = new GuestList.Views.AddGuestView({
      el: $('#add-male'),
      is_male: true,
      collection: maleCollection
    });

    var femaleAddView = new GuestList.Views.AddGuestView({
      el: $('#add-female'),
      is_male: false,
      collection: femaleCollection
    });

    // this is an anti-pattern, but don't worry about it for now
    setInterval(maleCollection.fetch.bind(maleCollection), 5000);
    setInterval(femaleCollection.fetch.bind(femaleCollection), 5000);
  }
});
