from config import *


class TableToNumpyArray:

    def __init__(self, shp_file, field_name):
        
        """
        Author: Chowdhury,Arif

        Description:
        Class TableToNumpyArray converts a given table to NumPy structured array where it takes a shapefile and field name
        as input and after the conversion returns the new array

        :param shp_file: This is the provided input shapefile for which specific field will be added.
        :param field_name: This  is the name of the field of the shapefile feature.
        """

        self.shp_file = shp_file
        self.field_name = field_name
        self.table_to_numpy_array()

    def table_to_numpy_array(self):
        # Get the basemap layer of the shape file
        source_layer = self.shp_file.GetLayer()
        #
        raster_path = r"" + os.path.abspath("") + "/output_file/temp.tif"

        # Creating the destination raster data source
        pixelWidth = pixelHeight = 1  # depending how fine you want your raster
        x_min, x_max, y_min, y_max = source_layer.GetExtent()
        cols = int((x_max - x_min) / pixelHeight)
        rows = int((y_max - y_min) / pixelWidth)
        target_ds = gdal.GetDriverByName('GTiff').Create(raster_path, cols, rows, 1, gdal.GDT_Byte)
        target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_min, 0, pixelHeight))
        band = target_ds.GetRasterBand(1)
        NoData_value = 255
        band.SetNoDataValue(NoData_value)
        band.FlushCache()

        # Rasterize
        gdal.RasterizeLayer(target_ds, [1], source_layer, options=["ATTRIBUTE=" + self.field_name])

        # add spatial reference
        srs = geo.get_srs(self.shp_file)
        b1 = srs.ImportFromEPSG(int(srs.GetAuthorityCode(None)))
        target_dsSRS = osr.SpatialReference()
        target_dsSRS.ImportFromEPSG(b1)
        target_ds.SetProjection(target_dsSRS.ExportToWkt())
        target_ds = None

        # print the new array
        new_array = gdal.Open(raster_path).ReadAsArray()
        logging.info("created new array")
        print(new_array)
        return new_array
