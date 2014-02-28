$(function () { 
    $('#tree')
    .on('changed.jstree', function (e, data) {
        var i, j, r = [];
        for(i = 0, j = data.selected.length; i < j; i++) {
          r.push(data.instance.get_node(data.selected[i]));
        }
        r = data.instance.get_node(data.selected[data.selected.length - 1])
        console.log(r);

        $('#items_data').html('');
        for (var item in r.data) {
            var key = item;
            var value = r.data[item]
            $('#items_data').append('<div>' + key + ': ' + value+'</div>')
        };
      })
    .jstree({
        'core' : {
            'data' : {
                'url' : '/getitems',
                'data' : function (node) {
                    return JSON.stringify( { 'id' : node.id });
                },
                "type" : "POST",
                "dataType" : "json",
                "contentType" : "application/json; charset=utf-8",
            }
        }});
});
