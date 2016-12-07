(function() {
  'use strict';

  GuestList.Collections.GuestCollection = Backbone.Collection.extend({
    model: GuestList.Models.Guest,

    initialize: function(models, options) {
      this.is_male = options.is_male;
    },

    url: function() {
      return this.is_male ? base_url + '/guests/males' : base_url + '/guests/females';
    },

    parse: function(res) {
      return res.guests;
    },

    checkedInCount: function() {
      return this.where({ is_at_party: true }).length;
    },

    randomEnteredParty: function() {
      var guests = this.where({ is_at_party: false });
      if(guests.length === 0)
        return;
      var guest = guests[Math.floor(Math.random()*guests.length)];
      guest.save({'is_at_party': true});
    },

    randomLeftParty: function() {
      var guests = this.where({ is_at_party: true });
      if(guest === 0)
        return;
      var guest = guests[Math.floor(Math.random()*guests.length)];
      guest.save({'is_at_party': false});
    },
  });
})();
