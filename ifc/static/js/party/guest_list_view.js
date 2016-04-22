(function() {
  'use strict';

  GuestList.Views.GuestListView = Backbone.View.extend({
    initialize: function(options) {
      this.collection = options.collection;
      this.collection.fetch();
      this.listenTo(this.collection, 'add', this.addNew);
      this.modelViews = [];
      this.collection.each(this.addNew, this);
    },

    addNew: function(model) {
      var elt = this.makeChildElt();
      this.$el.append(elt);
      var mv = new GuestList.Views.GuestView({ model: model, el: elt });
      this.modelViews.push(mv);
    },

    makeChildElt: function() {
      var elt = document.createElement('div');
      elt.classList.add('guest');
      this.collection.is_male ? elt.classList.add('male-guest') : elt.classList.add('female-guest');
      return elt;
    },

    render: function() {
      this.modelViews.each(function(mv) { mv.render(); });
    }
  });
})();
