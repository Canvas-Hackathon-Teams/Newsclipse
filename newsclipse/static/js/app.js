window.App = {};
console.log('this...');
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
        console.log('fetching...');
        // Check for a global JST object.  When you build your templates for
        // production, ensure they are all attached here.
        var JST = window.JST || {};

        // If the path exists in the object, use it instead of fetching remotely.
        if (JST[path]) {
            console.log('JST');
            return JST[path];
        }

        // If it does not exist in the JST object, mark this function as
        // asynchronous.
        var done = this.async();

        // Fetch via jQuery's GET.  The third argument specifies the dataType.
        $.get('/static/js/templates/' + path + '.jst', function(contents) {
            console.log('templates');
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


// ===================================================================
// Collections
// ===================================================================


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
    template: "footer"
});

// ===================================================================
// Layouts
// ===================================================================


App.Layout = new Backbone.Layout({
    // Attach the Layout to the main container.
    el: "body",
    views: {
        "header": new App.HeaderView(),
        "footer": new App.FooterView()
    }
});

App.Router = Backbone.Router.extend({
    //collection: App.Modules,
    initialize: function() { 
    },
    routes: {
        '': 'start',
        '*default': 'defaultRoute'
    },
    start: function() {
        App.Layout.render();
    }
});

$(function() {
    // Initialize the Backbone router.
    App.router = new App.Router();
    // TODO change to PushState
    Backbone.history.start();
});
