$(function () { 
    $('#tree').jstree({
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
