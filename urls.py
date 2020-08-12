from django.conf.urls import include, url

import gis_asset_app.views

urlpatterns = [
    url(r'^$', gis_asset_app.views.search, name='search'),
    url(
        r'^autocomplete/?$',
        gis_asset_app.views.autocomplete,
        name='autocomplete',
    ),
    url(r'^asset/(\d+)/?$', gis_asset_app.views.asset, name='asset'),
    url(r'^drives/?$', gis_asset_app.views.drives, name='drives'),
]
