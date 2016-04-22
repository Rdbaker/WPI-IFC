(function() {
  'use strict';

  GuestList.Models.Guest = Backbone.Model.extend({
    url: function() {
      if(this.has('id'))
        return base_url + '/guests/' + this.get('id');
      return base_url + '/guests';
    },

    parse: function(res) {
      if(!!res.guest) {
        return res.guest;
      } else {
        return res;
      }
    }
  });
})();
