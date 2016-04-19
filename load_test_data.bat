
d:
cd \local\gis_asset_ws
python d:/repo/gis_asset/src/gispider.py d:\repo\gis_asset\test_data >test_data.json

python gis_asset_app/load_data.py 1 test_data.json
