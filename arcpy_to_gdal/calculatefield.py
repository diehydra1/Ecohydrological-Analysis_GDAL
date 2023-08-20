from config import *


class CalculateField:
    def __init__(self, input_shapefile, field_name, expression):
        """
        Author: Siyuan Niu

        Description: The function of Class CalculateField it to add a value to the given field of the selected shapefile.

        :param input_shapefile: the input shapefile containing the field that will be updated
        :param field_name: the field that will be updated with the new value
        :param expression: the value that will be added to the chosen field
        """
        self.input_shapefile = input_shapefile
        self.field_name = field_name
        self.expression = expression
        self.calculate_field()

    def calculate_field(self):
        # get layer of the shapefile
        in_shp_lyr = self.input_shapefile.GetLayer()
        logging.info('layer is got')

        # create Feature as child of the layer
        feature = ogr.Feature(in_shp_lyr.GetLayerDefn())
        logging.info('feature is created')

        # define value of expression in the given field
        feature.SetField(self.field_name, self.expression)
        logging.info('value is defined')

        # append the new feature to the layer
        in_shp_lyr.CreateFeature(feature)

        # release files by overwriting lyr with None
        in_shp_lyr = None
        logging.info('expression is added to the field')
        print("Success: Expression:\"" + str(self.expression) + "\" is added to the field \""
              + str(self.field_name) + "\".")
