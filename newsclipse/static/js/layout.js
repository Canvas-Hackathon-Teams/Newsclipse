// ===================================================================
// Views
// ===================================================================

App.HeaderView = Backbone.View.extend({
    template: "header",
    events: {
    }
});

App.FooterView = Backbone.View.extend({
    template: "footer",
    events: {
    }
});

App.DefaultView = Backbone.View.extend({
    template: "default",
    initialize: function(options) {
    },
    beforeRender: function() {
        //console.log('Adding child views...');
        //this.insertView("#story", new App.StoryView() );
        //this.insertView("#cards", new App.CardsView() );
    },
    events: {
    }
});

// ===================================================================
// Layouts
// ===================================================================

App.Layout = new Backbone.Layout({
    // Attach the Layout to the main container.
    el: "body",
    views: {
        "header": new App.HeaderView(),
        "footer": new App.FooterView(),
    }
});

