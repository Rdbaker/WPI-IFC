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
    },

    validate: function(attrs, options) {
      if(attrs.name.length < 3)
        return "Give a real name for the user.";
    },

    filter: function(re) {
      // let's fuzzy search on the query
      // check the guests's name
      if(re.test(this.get('name').toLowerCase()))
        return true;
      // check the host's name
      return re.test(this.get('host').toLowerCase());
    }
  });
})();
