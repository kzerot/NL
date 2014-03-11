var _OPTION = "<div class='option_field'><span>{0}</span><input value='{1}'></div>";
var _OPTION_CHILD = "<div class='option_field option_child'><span>{0}</span><input value='{1}'><div class='delete' {2}</div>";

function deleteItem(id){
    alert("delete item " + id);
}

$(function () { 
    $('#tree')
    .on('changed.jstree', function (e, data) {
        var i, j, r = [];
        for(i = 0, j = data.selected.length; i < j; i++) {
          r.push(data.instance.get_node(data.selected[i]));
        }
        r = data.instance.get_node(data.selected[data.selected.length - 1])
        req = { "itemId": r.id };
        //console.log(r);
        $.ajax({
              url: "/getitems",
              type: "POST",
              data: JSON.stringify(req),
              dataType: "json",
            })
          .done(function( itemData ) {
            $('#items_data').html('');
            console.log(itemData);
            for (var item in itemData.data) {
                var key = item;
                var value = itemData.data[item];
                var formatter = _OPTION;
                var script = "";
                if(!(key in itemData.init_data)){
                    formatter = _OPTION_CHILD;
                    script = "onclick='deleteItem({0})'".format(r.id);
                }
                $('#items_data').append(formatter.format(key, value, script));
            };
          });
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
