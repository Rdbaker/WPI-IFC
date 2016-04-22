(function() {
  'use strict';

  GuestList.Views.AddGuestView = Backbone.View.extend({
    initialize: function(options) {
      this.collection = options.collection;
      this.is_male = options.is_male;
    },

    events: {
      'keydown .enter-user-name' : 'nameType',
      'click .add-user-btn' : 'addUser'
    },

    nameType: function(e) {
      if(e.which === 13)
        this.addUser();
    },

    addFailed: function(model, res) {
      Broadcaster.flashError(res.responseJSON.error);
    },

    addSuccess: function(model, res) {
      this.collection.add(model);
      Broadcaster.flashSuccess("Guest successfully added to the list.");
    },

    addUser: function(e) {
      var inputElt = $('.enter-user-name', this.$el)
      var props = {
        name : inputElt.val(),
        is_male : this.is_male,
        host : window.me.first_name + " " + window.me.last_name
      };

      var guest = new GuestList.Models.Guest(props);
      inputElt.val("");

      guest.save(null, {
        success: this.addSuccess.bind(this),
        error: this.addFailed.bind(this)
      });
    }
  });
})();
