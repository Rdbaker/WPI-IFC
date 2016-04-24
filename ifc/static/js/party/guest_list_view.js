(function() {
  'use strict';

  GuestList.Views.GuestListView = Backbone.View.extend({
    template: "<div class=\"button-group\"><div class=\"btn btn-danger btn-exit\"><i class=\"fa fa-icon fa-minus\"></i></div><div class=\"btn btn-success btn-enter\"><i class=\"fa fa-icon fa-plus\"></i></div></div>",

    initialize: function(options) {
      this.collection = options.collection;
      this.collection.fetch();
      this.listenTo(this.collection, 'add', this.addNew);
      this.collection.bind('change', this.updateCount.bind(this));
      this.listenTo(this.collection, 'remove', this.updateCount);
      this.modelViews = [];
      this.collection.each(this.addNew, this);
      this.searchInput = $('#guest-search');
      this.searchBtn = $('#search-btn');
      this.searchBtn.click(this.search.bind(this));
      this.searchInput.keypress(function(e) {
        if(e.which === 13) {
          this.search();
          return false;
        }
      }.bind(this));
      this.searching = true;
      this.lastSearch = null;
      if(this.collection.is_male) {
        this.countElt = $('#male-count');
      } else {
        this.countElt = $('#female-count');
      }
      this.render();
    },

    events: {
      'click .btn-exit': 'randomLeftParty',
      'click .btn-enter': 'randomEnteredParty'
    },

    updateCount: function() {
      if(window.partyStarted) {
        var count = this.collection.checkedInCount();
      } else {
        var count = this.collection.models.length;
      }

      this.countElt.html(count);
    },

    randomEnteredParty: function() {
      this.collection.randomEnteredParty();
    },

    randomLeftParty: function() {
      this.collection.randomLeftParty();
    },

    addNew: function(model) {
      var elt = this.makeChildElt();
      this.$el.append(elt);
      var mv = new GuestList.Views.GuestView({ model: model, el: elt });
      this.modelViews.push(mv);
      this.updateCount();
    },

    makeChildElt: function() {
      var elt = document.createElement('div');
      elt.classList.add('guest');
      this.collection.is_male ? elt.classList.add('male-guest') : elt.classList.add('female-guest');
      return elt;
    },

    render: function() {
      if(window.partyStarted)
        this.$el.append(_.template(this.template));
    },

    search: function() {
      // get the query string
      var query = this.searchInput.val();

      // if it's the same as last time,
      // I think we're clearing the search
      if(query === this.lastSearch)
        this.searching = !this.searching;

      if(this.searching) {
        this.searchBtn.text("Clear Search");
      } else {
        this.searchBtn.text("Search");
        this.searchInput.val("");
      }

      this.lastSearch = query;
      query = query.split("").join(".{0,"+2+"}");
      var re = new RegExp(query);
      this.modelViews.forEach(function(mv) { mv.search(re); });
    }
  });
})();
