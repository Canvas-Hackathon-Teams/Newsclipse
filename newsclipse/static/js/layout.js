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
