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
    collection: '',
    initialize: function(options) {
        console.log('Card editor view initalized...');
        this.collection = options.cards;
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

