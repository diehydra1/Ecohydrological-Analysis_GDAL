from config import *


class IsNull:
    def __init__(self, raster_file_name):
        """
        Author: Siyuan Niu

        Description: The function of IsNull is to determine which values from the input raster are NoData.
        It will return a value of 1 if the input value is NoData and 0 for cells that are not.

        :param raster_file_name: input raster file
        """
        self.raster_file_name = raster_file_name
        self.output_raster = self.isnull()  # output raster file

    def isnull(self):
        # load raster as array
        load_raster, load_raster_array, load_raster_geo_info = geo.raster2array(self.raster_file_name)
        logging.info('raster file is loaded as array:')
        logging.info(load_raster_array)

        # determine NoData values
        output_array = pd.isnull(load_raster_array)
        logging.info('output array in Boolean value:')
        logging.info(output_array)

        # convert Boolean value to Integer(True = 1, False = 0)
        output_array_int = np.array(output_array).astype(int)
        logging.info('output array in Integer:')
        logging.info(output_array_int)

        # create raster from array
        geo.create_raster(file_name=r"" + os.path.abspath("") + "/output_file/outputIsNull.tif",
                          raster_array=output_array_int, epsg=6418, geo_info=load_raster_geo_info)
        logging.info('output raster is saved')
        print("Success: Raster saved " + os.path.abspath("") + "/output_file/outputIsNull.tif")

        # return a raster file
        return r"" + os.path.abspath("") + "/output_file/outputIsNull.tif"
