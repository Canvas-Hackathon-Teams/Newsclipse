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
    collection: '',
    initialize: function() {
        console.log('Story view initalized...');
    },
    template: "story-editor",
    events: {
        "click #analyze": "runAnalyze"
    },
    runAnalyze: function() {
        console.log('yo!');
        //console.log(this);
        this.model.set('text', $('#text').val());
        //console.log(this.model);
        this.model.save();
    },
    beforeRender: function() {
        // Add the subviews to the view
           this.insertView("#card-editor", new App.CardEditorView({
               storyId: this.model.get('_id')
           }));
    },
    afterRender: function() {
    }
});
