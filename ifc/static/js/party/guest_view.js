(function() {
  'use strict';

  GuestList.Views.GuestView = Backbone.View.extend({
    template: _.template("<div class=\"guest-name\"><%= name %><% if(me.full_name === host && !window.partyStarted) {  %><div class=\"btn btn-danger\"><i class=\"fa fa-icon fa-times\"></i></div><% } %><% if(window.partyStarted && is_at_party) { %><i class=\"fa fa-icon fa-check-circle-o checked-in-icon\"></i><% } %></div><div class=\"text-muted\">Added by <%= host %></div>"),

    initialize: function(options) {
      this.listenTo(this.model, 'remove', this.destroy);
      this.listenTo(this.model, 'change', this.render);
      this.render();
    },

    events: {
      'click .btn.btn-danger': 'deleteModel',
      'click': 'toggleHere'
    },

    render: function() {
      this.$el.html(this.template(_.extend(this.model.attributes, { me: window.me })));
      return this;
    },

    deleteModel: function() {
      this.model.destroy({
        success: this.modelDeleted,
        error: this.cantDelete
      });
    },

    modelDeleted: function() {
      Broadcaster.flashSuccess("Guest successfully removed from the list.");
    },

    cantDelete: function(res) {
      Broadcaster.flashError(res.responseJSON.error);
    },

    destroy: function() {
      this.remove();
      delete this;
    },

    search: function(re) {
      if(this.model.filter(re)) {
        this.$el.removeClass("hidden");
      } else {
        this.$el.addClass("hidden");
      }
    },

    toggleHere: function(e) {
      if(!window.partyStarted)
        return;
      // check the guest in/out
      this.model.set('is_at_party', !this.model.get('is_at_party'));
      // save it
      this.model.save();
    }
  });
})();
