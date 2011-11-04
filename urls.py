from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    (r'^/?$', 'gis_asset.views.search'),
    (r'^autocomplete/?$', 'gis_asset.views.autocomplete'),
    (r'^asset/(\d+)/?$', 'gis_asset.views.asset'),
    (r'^drives/?$', 'gis_asset.views.drives'),

)
