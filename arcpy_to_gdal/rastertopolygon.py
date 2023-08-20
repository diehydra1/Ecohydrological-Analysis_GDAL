from config import *


class RasterToPolygon:

    def __init__(self, file_name, out_shp_fn):
        
        """
        Author: Chowdhury,Arif

        Description:
        Class RasterToPolygon converts a raster dataset to the polygon features where raster dataset
        is being provided as input and after the conversion it return a shapefile.

        :param file_name: STR of target file name, including directory; must end on ".tif"
        :param out_shp_fn: STR of a shapefile name
        """
        self.file_name = file_name
        self.out_shp_fn = out_shp_fn
        self.band_number = 1
        self.field_name = "values"
        self.raster2polygon()

    def raster2polygon(self):
        # ensure that the input raster contains integer values only and open the input raster
        a1 = geo.float2int(self.file_name)
        raster, raster_band = geo.open_raster(a1, band_number=self.band_number)

        # create new shapefile with the create_shp function
        new_shp = geo.create_shp(self.out_shp_fn, layer_name="raster_data", layer_type="polygon")
        logging.info('shapefile created')
        dst_layer = new_shp.GetLayer()

        # create new field to define values
        new_field = ogr.FieldDefn(self.field_name, ogr.OFTInteger)
        dst_layer.CreateField(new_field)

        # Polygonize(band, hMaskBand[optional]=None, destination lyr, field ID, papszOptions=[], callback=None)
        gdal.Polygonize(raster_band, None, dst_layer, 0, [], callback=None)

        # create projection file
        srs = geo.get_srs(raster)
        geo.make_prj(self.out_shp_fn, int(srs.GetAuthorityCode(None)))
        print("Success: Wrote %s" % str(self.out_shp_fn))
        return new_shp
