var _OPTION = "<div id='data_{2}' class='option_field'><span>{0}</span><input id='text_{2}' type='text' value='{1}'><div class='icon delete' {3}></div></div>";

var _OPTION_CHILD = "<div id='data_{2}' class='option_field option_child'><span>{0}</span><input id='text_{2}' type='text' value='{1}'><div class='icon undo' {3}></div></div>";

var current = {}
var parent = {}
var mode = null;
var dialog = null;

//Autocomplete
var availableTags = [
      "SKILL",
	"LVL",
	"PATK",
	"MATK",
	"ARP",
	"MARP",
	"CRIT",
	"HIT",
	"TARGET_INSTANT", "TARGET_ENTITY", "TARGET_COORD", "TARGET_BULLET", "TARGET_DIRECTION",
	"SHAPE_SELF",
	"SHAPE_SINGLE",
	"SHAPE_SECTOR",
	"SHAPE_CIRCLE",
	"DAM_LVL",
	"DAM_HEAL",
	"DAM_FIRE",
	"DAM_ICE",
	"DAM_DARK",
	"DAM_ELECTRO",
	"DAM_PHYS",
	"DAM_PIERCE",
	"DAM_BLUNT",
	"DAM_FIRE_P",
	"DAM_ICE_P",
	"DAM_DARK_P",
	"DAM_ELECTRO_P",
	"DAM_PHYS_P",
	"DAM_PIERCE_P",
	"DAM_BLUNT_P",
	"DAM_CUSTOM",
	"TYPE.BULLET", "TYPE.AOE", "TYPE.AFFECT", "TYPE.POINT", "TYPE.SHAPED",
    ];

$(function () {
    $('#tree')
    .on('changed.jstree', function (e, data) {
        var i, j, r = [];
        for(i = 0, j = data.selected.length; i < j; i++) {
          r.push(data.instance.get_node(data.selected[i]));
        }
        r = data.instance.get_node(data.selected[data.selected.length - 1])
        req = { "itemId": r.id, "table": table };
        //console.log(r);
        $.ajax({
              url: "/getitems",
              type: "POST",
              data: JSON.stringify(req),
              dataType: "json",
            })
          .done(function( itemData ) {
            current = itemData.data;
            parent = itemData.init_data;
            $('#items_data').html('');
            console.log(itemData);
            for (var item in itemData.data) {
                var key = item;
                var value = itemData.data[item];
                var formatter = _OPTION;
                var script = "";
                if(itemData.init_data && key in itemData.init_data){
                    formatter = _OPTION_CHILD;
                    script = "onclick='undoProp(\"{0}\")'".format(key);
                } else{
                    script = "onclick='deleteProp(\"{0}\")'".format(key);
                }
                $('#items_data').append(formatter.format(key, value, key, script));
                $('#text_'+key).autocomplete({
                  source: availableTags,
                  change: function( event, ui ) {
                  var txt_id = $(this)[0].id.replace('text_','');
                    current[txt_id] = $(this).val();
                    $('#data_'+txt_id + ' span').css('background-color', 'rgb(252, 180, 180)');
                    }
                });
            };
          });
      })
    .on('ready.jstree', function (e, data) {
        dialog = $( "#input_dialog" ).dialog({
          autoOpen: false,
          height: 150,
          width: 300,
          modal: true,
          buttons: {
            "Ok": confirmInput,
            Cancel: function() {
              dialog.dialog( "close" );
            }
          },
          close: function() {
            console.log("Input canceled");
          }
        });

        $('#btn_refresh').click(function(){
            $('#tree').jstree(true).refresh();
        });

        $('#btn_add').click(function(){
            mode = "add_prop";
            dialog.dialog( "open" );
        });
        $('#btn_add_base').click(function(){
            mode = "add_base";
            dialog.dialog( "open" );
        });
        $('#btn_del').click(function(){
        });
        $('#btn_save').click(function(){
            save();
        });
        $('#btn_del_all').click(function(){
            deleteItem($('#tree').jstree(true).get_selected()[0]);
        });


        function confirmInput(){
            var name = $('#name').val();
            if(mode === "add")
                addNode(name, true);
            else if (mode === "add_base")
                addNode(name, false);
            else if (mode === "add_prop")
                addProp(name);
            dialog.dialog('close');
        }

    })
    .jstree({
        'core' : {
            "check_callback" : true,
            'data' : {
                'url' : '/getitems',
                'data' : function (node) {
                    return JSON.stringify( { 'id' : node.id, 'table': table });
                },
                "type" : "POST",
                "dataType" : "json",
                "contentType" : "application/json; charset=utf-8",
            },
            'multiple' : false
        },
        "contextmenu": {
        "items": function ($node) {
            return {
                "Add child": {
                    "label": "Create child item",
                    "action": function (obj) {
                        mode = "add";
                        dialog.dialog( "open" );
                    }
                },
                "Delete": {
                    "label": "Delete",
                    "action": function (obj) {
                        deleteItem($('#tree').jstree(true).get_selected()[0]);
                    }
                }
            };
        }},
        "plugins" : [
            "contextmenu", "state",
          ]
        });

});

function save(){
   me = $('#tree').jstree(true).get_selected()[0];

   $.ajax({
      url: "/getitems",
      type: "POST",
      data: JSON.stringify({"save":true, "itemId": me, "data": current, "table": table}),
      dataType: "json",
    })
  .done(function( itemData ) {
      console.log("Saved");
      console.log(itemData);
      $('.option_field span').css('background-color', '');
    });
}

function addNode(name, haveParent){
   var parent = '#';
   if(haveParent)
       parent = $('#tree').jstree(true).get_selected()[0];
          console.log("New Node with parent: ");
          console.log(parent);
   $.ajax({
      url: "/getitems",
      type: "POST",
      data: JSON.stringify({"add":true, "itemId": parent, "name": name, "table": table}),
      dataType: "json",
    })
  .done(function( itemData ) {
      console.log("New Node");
      console.log(itemData);
        $('#tree').jstree(true).create_node(parent, itemData);
  });
}

function undoProp(node){
    if(node in parent){
        $('#text_'+node).val(parent[node]);
        current[node] = parent[node];
    }
    else{
        $('#data_'+node).remove();
        delete current[node];
    }
}

function deleteProp(node){
    delete current[node];
    $('#data_'+node).remove();
}

function addProp(name){
    var key = name;
    var value = "";
    var formatter = _OPTION;
    var script = "";
    script = "onclick='deleteProp(\"{0}\")'".format(key);

    $('#items_data').append(formatter.format(key, value, key, script));
    $('#text_'+key).change(function(){
        var txt_id = $(this)[0].id.replace('text_','');
        current[txt_id] = $(this).val();
        $('#data_'+txt_id + ' span').css('background-color', 'rgb(252, 180, 180)');
    });
}

function deleteItem(id){
   $.ajax({
      url: "/getitems",
      type: "POST",
      data: JSON.stringify({"delete":true, "itemId": id, "table": table}),
      dataType: "json",
    })
  .done(function( itemData ) {
      console.log("deleted? ");
      console.log(itemData);

      $('#tree').jstree(true).delete_node(id);

      var newid = $('#tree').jstree(true).get_json()[0].id;
      $('#tree').jstree(true).deselect_all();
        $('#tree').jstree(true).select_node(newid);
    });
}

/* with love, Max */