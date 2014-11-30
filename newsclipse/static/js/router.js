
App.Router = Backbone.Router.extend({
    collection: App.Stories,
    initialize: function() { 
    },
    routes: {
        '': 'start',
        'story(/:id)': 'displayStory',
        '*default': 'defaultRoute'
    },
    displayStory: function(id) {
        console.log('Navigating to story...');
        var story = this.collection.findWhere({
            "_id": id 
        });
        if (story) {
            App.Layout.setView("#content", new App.StoryView({
                model: story
            }));
            App.Layout.render();
        } else {
            this.defaultRoute();
        }
    },
    start: function() {
        console.log('App starting...');
        App.Layout.setView("#content", new App.StoryListView());
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
