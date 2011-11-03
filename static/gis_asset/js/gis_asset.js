
if (typeof(jQ) == 'undefined') {
    jQ = jQuery;
}
jQ(init);

function init() {

    var autos = ['attr_name', 'asset_name', 'path_txt'];
    for (var i in autos) {
        var name = autos[i];
        var options = {
            serviceUrl: GIS_ASSET_URL+'/autocomplete?context='+name,
            delimiter: ','
        }
        if (name == 'path_txt') {
            options.serviceUrl = (
                GIS_ASSET_URL+'/autocomplete?all=y&context='+name);
        }

        jQ('.'+name).autocomplete(options)
    }

}
