// ===================================================================
// Models
// ===================================================================

App.Card = Backbone.Model.extend({ 
  attributeId: '_id'
});

App.Story = Backbone.Model.extend({ 
  attributeId: '_id',
  url: function() {
    //console.log(this);
    return '/api/stories/' + this.get('_id');
  }
});
