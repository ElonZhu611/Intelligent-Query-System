$( "#add_table_btn" ).click(function() {
    var add_table_area = $("#add_table_area");

    var curValue = add_table_area.val();

    if (curValue=="") {
        var new_add = $( "#table_name option:selected" ).val();        
    } else {
        var new_add = "\n" + $( "#table_name option:selected" ).val();
    }

    var newValue = curValue + new_add;

    add_table_area.val(newValue);

});


$("#gentable_btn").click(function() {
    var add_table_area = $("#add_table_area").val();
    $.ajax({
      type: 'POST',
      url: "/gentable",
      data: JSON.stringify({ add_table_area}),
      dataType: "json"
    }).done(function(data) {
        var cols = $.map(data, function(value, key) { return value });
        for(var i=0; i<cols.length; i++){
            var col = cols[i]
            $("#table1_col").append($('<option>').val(col).text(col));
            $("#table2_col").append($('<option>').val(col).text(col));
            $("#feature_col").append($('<option>').val(col).text(col));
            $("#filter_col").append($('<option>').val(col).text(col));
            $("#group_col").append($('<option>').val(col).text(col));
            $("#agg_col").append($('<option>').val(col).text(col));
        };
    });
});

$("#clear_table_btn").click(function() {
    window.location.href=window.location.href;
});


$("#join_btn").click(function() {
    var join_table_area = $(" #join_table_area ");

    var key1 = $( "#table1_col option:selected" ).val();
    var key2 = $( "#table2_col option:selected" ).val();
    var join_type = $( "#select_join option:selected" ).val();

    var table_keys = [key1, key2];

    var curValue = join_table_area.val();

    if (curValue=="") {
        var new_add = key1 + "\n" + join_type + "\n" + key2;
    } else {
        var new_add = "\n" + key1 + "\n" + join_type + "\n" + key2;
    }

    var newValue = curValue + new_add;
    join_table_area.val(newValue);
});

$("#clear_join_btn").click(function() {
    $(" #join_table_area ").val("");
});


$( "#add_feature_btn" ).click(function() {
    var add_feature_area = $("#add_features_area");

    var curValue = add_feature_area.val();

    var curfunc = $( "#agg_func option:selected" ).val();
    var curcol = $( "#feature_col option:selected" ).val();

    if (curfunc=="") {
        var fea = curcol;
    } else {
        var fea = curfunc + "(" + curcol + ")";
    }

    if (curValue=="") {
        var new_add = fea;
    } else {
        var new_add = "\n" + fea;
    }

    var newValue = curValue + new_add;

    add_feature_area.val(newValue);
});

$("#clear_feature_btn").click(function() {
    $(" #add_features_area ").val("");
});


$( "#add_filter_btn" ).click(function() {
    var add_filters_area = $("#add_filters_area");

    var curValue = add_filters_area.val();

    var new_add_col = $( "#filter_col option:selected" ).val();
    var new_add_opr = $( "#filter_func option:selected" ).val();
    var new_add_equal = $( "#filter_equal" ).val();

    if (curValue=="") {
        var new_add = new_add_col + new_add_opr + new_add_equal;
    } else {
        var new_add = "\n" + new_add_col + new_add_opr + new_add_equal;
    }

    var newValue = curValue + new_add;

    add_filters_area.val(newValue);
});

$("#clear_filter_btn").click(function() {
    $(" #add_filters_area ").val("");
});


$( "#add_group_btn" ).click(function() {
    var add_group_area = $("#add_group_area");

    var curValue = add_group_area.val();

    if (curValue=="") {
        var new_add = $( "#group_col option:selected" ).val();
    } else {
        var new_add = "\n" + $( "#group_col option:selected" ).val();
    }

    var newValue = curValue + new_add;

    add_group_area.val(newValue);
});

$("#clear_group_btn").click(function() {
    $(" #add_group_area ").val("");
});


$("#preview_btn").click(function() {
    var tables = $(" #add_table_area ").val();
    var joins = $(" #join_table_area ").val();
    var features = $("#add_features_area").val();
    var filters = $(" #add_filters_area ").val();
    var groups = $(" #add_group_area ").val();

    if (tables=="") {
        alert("Please choose tables!");
    } else if (features=="") {
        alert("Please choose features!");
    } else {
        $.ajax({
        type: 'POST',
        url: "/query",
        data: JSON.stringify({ tables, joins, features, filters, groups }),
        dataType: "json"
        }).done(function(data) {
            window.open("preview");
        });       
    };
});


$("#download_btn").click(function() {
    var tables = $(" #add_table_area ").val();
    var joins = $(" #join_table_area ").val();
    var features = $("#add_features_area").val();
    var filters = $(" #add_filters_area ").val();
    var groups = $(" #add_group_area ").val();
    var down_name = $(" #download_area" ).val();

    if (tables=="") {
        alert("Please choose tables!")
    } else if (features=="") {
        alert("Please choose features!")
    } else if (down_name=="") {
        alert("Please input file name");
    } else {
        $.ajax({
          type: 'POST',
          url: "/download",
          data: JSON.stringify({ tables, joins, features, filters, groups, down_name }),
          dataType: "json"
        }).done(function(data) {
            alert("File saved!");
        });        
    };
});


$("#import_btn").click(function() {
    var name = $(" #macro_name option:selected ").val();

    if (name=="") {
        alert("Please select a record!")
    } else {
        $.ajax({
          type: 'POST',
          url: "/import",
          data: JSON.stringify({ name }),
          dataType: "json"
        }).done(function(data) {
            var tables = data["macrotable"];
            var joins = data["macrojoin"];
            var features = data["macrofeature"];
            var filters = data["macrofilter"];
            var groups = data["macrogroup"];

            $("#add_table_area").val(tables);
            $("#join_table_area").val(joins);
            $("#add_features_area").val(features);
            $("#add_filters_area").val(filters);
            $("#add_group_area").val(groups);

            alert("Import the record!");

            var cols = $.map(data["columns"], function(value, key) { return value });
            for(var i=0; i<cols.length; i++){
                var col = cols[i]
                $("#table1_col").append($('<option>').val(col).text(col));
                $("#table2_col").append($('<option>').val(col).text(col));
                $("#feature_col").append($('<option>').val(col).text(col));
                $("#filter_col").append($('<option>').val(col).text(col));
                $("#group_col").append($('<option>').val(col).text(col));
                $("#agg_col").append($('<option>').val(col).text(col));
            };
        });        
    };
});


$("#record_btn").click(function() {
    var tables = $(" #add_table_area ").val();
    var joins = $(" #join_table_area ").val();
    var features = $("#add_features_area").val();
    var filters = $(" #add_filters_area ").val();
    var groups = $(" #add_group_area ").val();

    var name = $(" #macro_area ").val();

    if (name=="") {
        alert("Please input record name!")
    } else {
        $.ajax({
          type: 'POST',
          url: "/record",
          data: JSON.stringify({ name, tables, joins, features, filters, groups }),
          dataType: "json"
        }).done(function(data) {
            alert("Record!");
            location.reload(true);
        });        
    };
});


$("#delete_btn").click(function() {
    var name = $(" #macro_name option:selected ").val();

    if (name=="") {
        alert("Please select a record!")
    } else {
        $.ajax({
          type: 'POST',
          url: "/delete",
          data: JSON.stringify({ name }),
          dataType: "json"
        }).done(function(data) {
            alert("Delete the record!");
            location.reload(true);
        });        
    };
});



