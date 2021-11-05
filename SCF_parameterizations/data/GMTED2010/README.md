#  GMTED2010 global digital elevation model

https://www.temis.nl/data/gmted2010/index.php (downloaded: 28 October 2021)

Elevation data sets at different resolutions have been compiled from the 15 arc-second resolution [GMTED2010 global digital elevation model](https://www.temis.nl/data/gmted2010.html), which was aggregated into one file (adding data over Greenland and the Southpole from the 90 arc-second dataset) by the team assembling the datasets needed for the TROPOMI data processing.
In the datasets given below an error in the GMTED2010 dataset over the Caspian Sea (a large area of that sea has zero elevation instead of -27 m) has been repaired.
Note that there is no special value for ocean waters in these files; the elevation of the ocean water is simply 0 (zero) metres.

The data is given in two formats:

- As netCDF-4 file
- As HDF-4 file

There are several programs around to read & view these datafile, e.g. [hdfview](https://www.hdfgroup.org/products/java/hdfview/index.html) (both file types), [ncview](http://meteora.ucsd.edu/~pierce/ncview_home_page.html) (netCDF only), [panoply](http://www.giss.nasa.gov/tools/panoply/) (strangely enough does not work on the netCDF files). For data processing, the files can be read with programs such as IDL, Matlab, Maple. Information sources, with examples, tools and software at the [The HDF Group](https://www.hdfgroup.org/):  [HDF-5](https://www.hdfgroup.org/HDF5/),  [netCDF-4](https://www.hdfgroup.org/projects/netCDF-4/),  [HDF-4](https://www.hdfgroup.org/products/hdf4/)

 

| *resolution* *                                               | `nlon` | `nlat` | *netCDF & HDF-4 data files*                                  |
| ------------------------------------------------------------ | ------ | ------ | ------------------------------------------------------------ |
| 0.0625 degrees                                               | 5760   | 2880   | [GMTED2010_15n015_00625deg.nc](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n015_00625deg.nc) [26MB][GMTED2010_15n015_00625deg.hdf](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n015_00625deg.hdf) [27MB] |
| 0.125 degrees                                                | 2880   | 1440   | [GMTED2010_15n030_0125deg.nc](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n030_0125deg.nc) [7.2MB][GMTED2010_15n030_0125deg.hdf](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n030_0125deg.hdf) [7.3MB] |
| 0.250 degrees                                                | 1440   | 720    | [GMTED2010_15n060_0250deg.nc](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n060_0250deg.nc) [2.1MB][GMTED2010_15n060_0250deg.hdf](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n060_0250deg.hdf) [2.0MB] |
| 0.500 degrees                                                | 720    | 360    | [GMTED2010_15n120_0500deg.nc](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n120_0500deg.nc) [605kB][GMTED2010_15n120_0500deg.hdf](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n120_0500deg.hdf) [568KB] |
| 1.000 degrees                                                | 360    | 180    | [GMTED2010_15n240_1000deg.nc](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n240_1000deg.nc) [206bK][GMTED2010_15n240_1000deg.hdf](https://d1qb6yzwaaq4he.cloudfront.net/data/gmted2010/GMTED2010_15n240_1000deg.hdf) [170KB] |
| *) a. A resolution of 0.5 degrees means about 50 kilometer at the equator.   b. If other resolutions (multiples of 15 arc-seconds = 1/240-th degree)     are needed, please contact [Jos van Geffen](mailto:geffen@knmi.nl). |        |        |                                                              |



 
Official citation of the GMTED2010 elevation data:

> Danielson, J.J., and Gesch, D.B., 2011,
> *Global multi-resolution terrain elevation data 2010 (GMTED2010)*:
> U.S. Geological Survey Open-File Report 2011-1073, 26 p.
> [ http://pubs.usgs.gov/of/2011/1073/pdf/of2011-1073.pdf ]

See [the official GMTED2010 webpage](http://topotools.cr.usgs.gov/gmted_viewer/) for more details and background information.
 

------

 

### The netCDF and HDF-4 data files

The netCDF data file provides the elevation data in the form of 2-dimensional arrays with the longitude and latitude coordinates given in separate arrays. Since netCDF is based on the HDF-5 format, netCDF files can also be read with HDF-5 readers. The HDF-4 data files give the same data sets (variables), but is organised slightly differently.

The following table gives an overview of the data sets (variables) in a data file.

 

| *variable*                                                   | *unit* | *dimension(s)* 1 | *description*                                      |
| ------------------------------------------------------------ | ------ | ---------------- | -------------------------------------------------- |
| longitude                                                    | deg    | `nlon`           | longitude of grid cell centr                       |
| latitude                                                     | deg    | `nlat`           | latitude of grid cell centre                       |
| longitude_bounds                                             | deg    | `nlon,nbounds`   | longitude of grid cell boundaries                  |
| latitude_bounds                                              | deg    | `nlat,nbounds`   | latitude of grid cell boundaries                   |
| elevation 2                                                  | m      | `nlat,nlon`      | altitude above the geoid                           |
| elevation_stddev 2                                           | m      | `nlat,nlon`      | standard deviation of the altitude above the geoid |
| elevation_max 2                                              | m      | `nlat,nlon`      | maximum elevation above the geoid in grid cell     |
| elevation_min 2                                              | m      | `nlat,nlon`      | minimum elevation above the geoid in grid cell     |
| 1) The dimensions `nlat` and `nlon` depend on the resolution;   viz. the table at the top of the page.   The dimension `nbounds` always equals 2. 2) These four evelation data sets have an attribute giving the   minimum and maximum value found in the set. |        |                  |                                                    |





Each of the variables has some attributes, while the file itself has some global attributes (the HDF-4 file has some extra global attributes, following earlier elevation data files provided via TEMIS).

The above data files have been created from a single high-resolution netCDF file created within the TROPOMI project. Attributes from that original input file, used to generate the above files, are given as attributes to a group 'Original_attributes' in the netCDF file and to an otherwise empty variable 'original_attributes' in the NDF-4 file.

