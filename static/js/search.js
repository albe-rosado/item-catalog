
var client = algoliasearch("DWCAC7LUJZ", "1bb62fb76043db09505a5171a0e59dfb");
var index = client.initIndex('ItemCatalog');
//initialize autocomplete on search input (ID selector must match)

template = Hogan.compile('<span><a  href="'+'/category/{{belong_to_category}}' +
          '/item/{{id}}">' +
          '{{{_highlightResult.title.value}}} ' + 
          '</a></span><span>{{{_highlightResult.description.value}}}</span>');


autocomplete('#aa-search-input',
{ hint: false }, {
    source: autocomplete.sources.hits(index, {hitsPerPage: 7}),
    //value to be displayed in input control after user's suggestion selection
    displayKey: 'title',
    //hash of templates used when rendering dataset     

    templates: {
        //'suggestion' templating function used to render a single suggestion
        suggestion: function(suggestion) {
          return template.render(suggestion);          
        }
    }
});
