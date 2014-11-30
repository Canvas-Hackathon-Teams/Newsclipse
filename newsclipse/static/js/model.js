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
    comparator: 'created_at'
});

App.Stories = new App.StoriesCollection(STORIES);

App.StoryCardsCollection = Backbone.Collection.extend({
    model: App.Card,
    //url: "/api/stories/" + storyId + "/cards",
    comparator: 'offset' // Order of appearance in the story
});

App.StoryCards = new App.StoryCardsCollection({

});
