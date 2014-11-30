// ===================================================================
// Collections
// ===================================================================

App.StoriesCollection = Backbone.Collection.extend({
    model: App.Story,
    url: "/api/stories",
    comparator: 'created_at'
});

App.Stories = new App.StoriesCollection(STORIES);

App.StoryCardsCollection = Backbone.Collection.extend({
    model: App.Card,
    storyId: '',
    url: '',
    initialize: function(options) {
        this.storyId = options.storyId; 
        this.url = "/api/stories/" + this.storyId + "/cards";
    },
    comparator: 'offset', // Order of appearance in the story
});
