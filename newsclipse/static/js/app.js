window.App = {};
// Use the backbone.layoutmanager
// turn it on for all views by default
Backbone.Layout.configure({
    manage: true,
    // Set the prefix to where your templates live on the server
    //prefix: "/ui/templates/",
    // Not using prefix because the templates are compilted at JST['template-name']
    // and setting prefix here looks for them with the prefix prepended.

    // This method will check for prebuilt templates first and fall back to
    // loading in via AJAX.
    fetchTemplate: function(path) {
        // Check for a global JST object.  When you build your templates for
        // production, ensure they are all attached here.
        var JST = window.JST || {};

        // If the path exists in the object, use it instead of fetching remotely.
        if (JST[path]) {
            return JST[path];
        }

        // If it does not exist in the JST object, mark this function as
        // asynchronous.
        var done = this.async();

        // Fetch via jQuery's GET.  The third argument specifies the dataType.
        $.get('/static/js/templates/' + path + '.jst', function(contents) {
            // Assuming you're using underscore templates, the compile step here is
            // `_.template`.
            done(_.template(contents));
        }, "text");
    }
});

// ===================================================================
// Utilities
// ===================================================================


// ===================================================================
// Models
// ===================================================================

App.Card = Backbone.Model.extend({ 

});

App.Story = Backbone.Model.extend({ 

});

// ===================================================================
// Collections
// ===================================================================

App.StoriesCollection = Backbone.Collection.extend({
    model: App.Story,
    url: "/api/stories",
    comparator: 'title'
});

App.StoryCardsCollection = Backbone.Collection.extend({
    model: App.Card,
    //url: "/api/stories/id/cards",
    comparator: '' // Order of appearance in the story
});

App.CardsCollection = Backbone.Collection.extend({
    model: App.Card,
    url: "/api/cards",
    comparator: 'title'
});

// ===================================================================
// Views
// ===================================================================
// Site-wide views
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

App.StoryListView = Backbone.View.extend({
    template: "story-list",
    events: {
    }
});

App.StoryView = Backbone.View.extend({
    template: "story-editor",
    events: {
    }
});

App.CardsView = Backbone.View.extend({
    template: "card-editor",
    events: {
    }
});

App.DefaultView = Backbone.View.extend({
    template: "default",
    initialize: function(options) {
    },
    beforeRender: function() {
        console.log('Adding child views...');
        this.insertView("#story", new App.StoryView() );
        this.insertView("#cards", new App.CardsView() );
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

App.Router = Backbone.Router.extend({
    collection: App.StoriesCollection,
    initialize: function() { 
    },
    routes: {
        '': 'start',
        '*default': 'defaultRoute'
    },
    start: function() {
        console.log('App starting...');
        App.Layout.setView("#content", new App.DefaultView());
        App.Layout.render();
    },
    defaultRoute: function() {
        console.log("404");
    }
});

$(function() {
    // Initialize the Backbone router.
    App.router = new App.Router();
    // TODO change to PushState
    Backbone.history.start();
});
