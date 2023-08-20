from config import *


class ConGdal:

    def __init__(self, in_con_raster, output_folder, operator, compared_value, in_true_raster, in_false_raster=np.nan):
        """
        Author: Baibrus Khan
        
        Description:
        Class ConGdal takes a raster and compare it with any other raster or a constant float value and apply if it the comparison operator is true or flase and which
        value should be added to the cell if it is true or false. It provides a raster as an output to show the result.
        
        
        :param in_con_raster: Raster file which would be evaluated according to the other arguments. Must be a raster file. 
        :param output_folder: Location needs to be specified as a directory path to save the output raster.
        :param operator: This needs to be in string form "". Any comparison operator can be used.
        :param compared_value: This can either be a raster or a constant float value, to compare it with the in_con_raster.
        :param in_true_raster: This can either be a raster or a constant float value, this value will be used for the cells that are true after applying
                               between in_con_raster and compared_value.
        :param in_false_raster: This can either be a raster or a constant float value, this value will be used for the cells that are false after applying
                                between in_con_raster and compared_value. If nothing is provided by default it uses np.nan.
        """
        self.in_con_raster = in_con_raster
        self.output_folder = output_folder
        self.operator = operator
        self.compared_value = compared_value
        self.in_true_raster = in_true_raster
        self.in_false_raster = in_false_raster
        self.output_raster = self.con_gdal()

    def con_gdal(self):

        # get the raster information for the condition raster.
        raster, array, geo_info = geo.raster2array(self.in_con_raster)

        logging.info('raster file loaded as array:')
        logging.info(array)

        # get the raster information for the raster used for comparison, else the constant.
        if type(self.compared_value) == float:
            c_array = self.compared_value
        else:
            c_raster, c_array, c_geo_info = geo.raster2array(self.compared_value)

        logging.info('array or constant value loaded to compared_value:')
        logging.info(c_array)

        # get the raster information for the raster used for the true value, else the constant.
        if type(self.in_true_raster) == float:
            t_array = self.in_true_raster
        else:
            t_raster, t_array, t_geo_info = geo.raster2array(self.in_true_raster)

        logging.info('array or constant value loaded to in_true_raster:')
        logging.info(t_array)

        # get the raster information for the raster used for the false value, else the constant or default "np.nan".
        if type(self.in_false_raster) == float:
            f_array = self.in_false_raster
        elif os.path.isfile(self.in_false_raster):
            f_raster, f_array, f_geo_info = geo.raster2array(self.in_false_raster)
        else:
            f_array = self.in_false_raster

        logging.info('array or constant loaded to in_false_raster:')
        logging.info(f_array)

        # According to different operator different comparison is made.
        if "==" in self.operator:
            out_array = np.where(array == c_array, t_array, f_array)
        elif "!=" in self.operator:
            out_array = np.where(array != c_array, t_array, f_array)
        elif "<=" in self.operator:
            out_array = np.where(array <= c_array, t_array, f_array)
        elif ">=" in self.operator:
            out_array = np.where(array >= c_array, t_array, f_array)
        elif "<" in self.operator:
            out_array = np.where(array < c_array, t_array, f_array)
        elif ">" in self.operator:
            out_array = np.where(array > c_array, t_array, f_array)

        logging.info('output array loaded to out_array:')
        logging.info(out_array)

        # Create raster from array.
        geo.create_raster(file_name=self.output_folder + "/Con_out_raster.tif",
                          raster_array=out_array, epsg=6418, geo_info=geo_info)
        logging.info('output raster saved')
        print("Success: Raster saved " + self.output_folder + "/Con_out_raster.tif")

        return r"" + self.output_folder + "/Con_out_raster.tif"
