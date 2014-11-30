
// ===================================================================
// Views
// ===================================================================

App.CardListItemView = Backbone.View.extend({
    model: App.Card,
    cardId: '',
    initialize: function() {
        console.log('Card list item view initalized...');
        this.cardId = this.model.get('_id');
    },
    template: "card-list-item",
    events: {
        // Listen for a click anywhere on the sub-view
        "click": "viewCardDetail"
    },
    viewCardDetail: function() { 
        App.router.navigate("card/" + this.cardId, {
            trigger: true
        });
    }
});

App.CardEditorView = Backbone.View.extend({
    collection: App.StoryCards,
    initialize: function() {
        console.log('Card editor view initalized...');
    },
    template: "card-editor",
    events: {
    },
    beforeRender: function() {
        // Add the subviews to the view
        this.collection.each(function(card) {
            this.insertView("#card-list", new App.CardListItemView({
                model: card
            }));
        }, this);
    }
});

App.CardsView = Backbone.View.extend({
    initialize: function() {
        console.log('Cards view initialized...');
    },
    template: "card-editor",
    events: {
    }
});


App.StoryListItemView = Backbone.View.extend({
    model: App.Story,
    storyId: '',
    initialize: function() {
        console.log('Story list item view initalized...');
        this.storyId = this.model.get('_id');
    },
    template: "story-list-item",
    events: {
        // Listen for a click anywhere on the sub-view
        "click": "viewStoryDetail"
    },
    viewStoryDetail: function() { 
        App.router.navigate("story/" + this.storyId, {
            trigger: true
        });
    }
});

App.StoryListView = Backbone.View.extend({
    collection: App.Stories,
    initialize: function() {
        console.log('Story list view initalized...');
    },
    serialize: function() {
        return {
            stories: this.collection
        };
    },
    template: "story-list",
    events: {
    },
    beforeRender: function() {
        // Add the subviews to the view
        this.collection.each(function(story) {
            this.insertView("#stories-list", new App.StoryListItemView({
                model: story
            }));
        }, this);
    },
});

App.StoryView = Backbone.View.extend({
    initialize: function() {
        console.log('Story view initalized...');
    },
    views: {
        "#card-editor": new App.CardEditorView(),
    },
    template: "story-editor",
    events: {
    }
});
,
    events: {
    },
    beforeRender: function() {
        // Add the subviews to the view
        this.collection.each(function(story) {
            this.insertView("#stories-list", new App.StoryListItemView({
                model: story
            }));
        }, this);
    },
});

App.StoryView = Backbone.View.extend({
    initialize: function() {
        console.log('Story view initalized...');
    },
    views: {
        "#card-editor": new App.CardEditorView(),
    },
    template: "story-editor",
    events: {
    }
});
