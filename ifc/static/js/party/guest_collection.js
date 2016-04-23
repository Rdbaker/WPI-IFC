(function() {
  'use strict';

  GuestList.Collections.GuestCollection = Backbone.Collection.extend({
    model: GuestList.Models.Guest,

    initialize: function(models, options) {
      this.is_male = options.is_male;
    },

    url: function() {
      return base_url + '/guests?is_male=' + this.is_male;
    },

    parse: function(res) {
      return res.guests;
    },

    checkedInCount: function() {
      return this.where({ is_at_party: true }).length;
    }
  });
})();
