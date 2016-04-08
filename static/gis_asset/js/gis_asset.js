
if (typeof(jQ) == 'undefined') {
    jQ = jQuery;
    
}
jQ(init);
function init() {

    var autos = ['attr_name', 'asset_name', 'path_txt'];
    for (var i in autos) {
        var name = autos[i];
        source = function(name) { return function(query, response) {
            jQ.ajax(
              GIS_ASSET_URL+'/autocomplete?all=y&context='+name+'&query='+query.term,
              {
                dataType: 'json',
                success: function(data) { response(data); }
              });
        }}(name);
                
        jQ('.'+name).autocomplete({source: source});
    }
    
    jQ('#id_min_date').datepicker();
    jQ('#id_max_date').datepicker();
    jQ('#dialog').hide();
    jQ('.helptext').hide();
    jQ('a.asset_info').click(show_info);
    
    jQ('#help_toggle').click(function(){
        jQ('.helptext').toggle('medium');
    });

}

function show_info(event) {

    event.preventDefault();
    event.stopPropagation();
    jQ('#dialog').load(jQ(event.target).closest('a').attr('href'), 
        show_info_dialog);
    return false;

}

function show_info_dialog(title) {

    var title = jQ('#dialog h1').text();
    jQ('#dialog h1').remove();

    jQ('#dialog').dialog({
        modal: true,
        width: 800,
        height: 600,
        title: title
    });

}

