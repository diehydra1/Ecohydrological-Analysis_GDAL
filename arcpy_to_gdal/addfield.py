from config import *


class AddField:
    def __init__(self, input_shapefile, field_name, infield_type):
        """
        Author: Siyuan Niu

        Description: The function of Class AddField it to add a new field to the given shapefile.

        :param input_shapefile: the input shapefile to which the specified field will be added
        :param field_name: the name of the field that will be added to the input shapefile
        :param infield_type: the type of the added field
        """
        self.input_shapefile = input_shapefile
        self.field_name = field_name
        self.infield_type = infield_type
        self.add_field()  # perform the add field operation

    def add_field(self):
        # get layer of the shapefile
        in_shp_lyr = self.input_shapefile.GetLayer()
        logging.info('layer is got')

        # determine field type
        if self.infield_type == "TEXT":
            field_type = ogr.OFTString
        elif self.infield_type == "FLOAT":
            field_type = ogr.OFSTFloat32
        elif self.infield_type == "DOUBLE":
            field_type = ogr.OFTReal
        elif self.infield_type == "SHORT":
            field_type = ogr.OFSTInt16
        elif self.infield_type == "LONG":
            field_type = ogr.OFTInteger
        elif self.infield_type == "DATE":
            field_type = ogr.OFTDate
        logging.info('field type = :')
        logging.info(self.infield_type)

        # add new field
        new_field_defn = ogr.FieldDefn(self.field_name, field_type)
        in_shp_lyr.CreateField(new_field_defn)
        logging.info('new field is created with the input field name')

        # release files by overwriting lyr with None
        in_shp_lyr = None
        logging.info('new field is added to the shapefile')

        print("Success: New field \"" + str(self.field_name) + "\" is added to the input shapefile.")
