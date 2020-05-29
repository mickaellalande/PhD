# MODIS/Terra Snow Cover 8-Day L3 Global 0.05Deg CMG, Version 6

Oroginal files are in HDF format at 0.05° without coordinates. So I added the coordinate and time to netcdf files + I made a regrid towards 0.5° for easier manipulation.

https://nsidc.org/data/MOD10CM

Grid
The MODIS CMG consists of 7200 columns by 3600 rows. Each cell has a resolution of 0.05 degrees (approximately 5 km). The upper-left corner of the upper-left cell is -180.00 degrees longitude, 90.00 degrees latitude. The lower-right corner of the lower right cell is -180.00 degrees longitude, -90.00 degrees latitude. For additional details about the MODIS Climate Modeling Grid, see the NASA MODIS Lands | MODIS Grids Web page.

The following resources can help you select and work with gridded MODIS data:

HDF-EOS to GeoTIFF Conversion Tool (HEG)

Other products: https://modis.gsfc.nasa.gov/data/dataprod/mod10.php  
More info on grids: https://modis-land.gsfc.nasa.gov/MODLAND_grid.html