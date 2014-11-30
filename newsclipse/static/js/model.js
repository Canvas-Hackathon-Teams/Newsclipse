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

App.StoryCardsCollection = Backbone.Collection.extend({
    model: App.Card,
    //url: "/api/stories/id/cards",
    comparator: '' // Order of appearance in the story
});

App.StoryCards = new App.StoryCardsCollection({

});

App.StoryCards = new App.StoryCardsCollection({

});

App.StoriesCollection = Backbone.Collection.extend({
    model: App.Story,
    url: "/api/stories",
    comparator: 'title'
});

App.Stories = new App.StoriesCollection(STORIES);

App.CardsCollection = Backbone.Collection.extend({
    model: App.Card,
    url: "/api/cards",
    comparator: 'title'
});
