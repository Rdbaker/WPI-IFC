(function() {
  'use strict';

  GuestList.Views.GuestView = Backbone.View.extend({
    template: _.template("<div class=\"guest-name\"><%= name %><% if(me.full_name === host) {  %><div class=\"btn btn-danger btn-xs\"><i class=\"fa fa-icon fa-times\"></i></div><% } %></div><div class=\"text-muted\">Added by <%= host %></div>"),

    initialize: function(options) {
      this.listenTo(this.model, 'remove', this.destroy);
      this.listenTo(this.model, 'change', this.render);
      this.render();
    },

    events: {
      'click .btn.btn-danger': 'deleteModel'
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
    }
  });
})();
