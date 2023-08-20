from calculatefield import *
from congdal import *
from isnull import *
from addfield import *
from tabletonumpyarray import *
from rastertopolygon import *
from config import *
from fun import *
from fish import *  # used for the example

# load raster
input_raster = r"" + os.path.abspath("") + "/input_file/Fr1000cfs.tif"
input_raster1 = r"" + os.path.abspath("") + "/input_file/h001000.tif"
input_raster2 = r"" + os.path.abspath("") + "/input_file/h002000.tif"

# file location for saving the output rasters
output_file = r"" + os.path.abspath("") + "/output_file/"
output_file_1 = r"" + os.path.abspath("") + "/output_file/output_file_fish1"
output_file_2 = r"" + os.path.abspath("") + "/output_file/output_file_fish2"

# set saved shapefile path for raster2polygon
out_shp = r"" + os.path.abspath("") + "/output_file/h_poly_cls.shp"

# load shape file
shp_driver = ogr.GetDriverByName("ESRI Shapefile")
shp_path = shp_driver.Open(r"" + os.path.abspath("") + "/input_file/countries.shp", 1)  # update =1 for rewriting

# set variables for adding field and calculating field
fieldname = "Area"
fieldtype = "DOUBLE"
expression = 3 ** 2


# using as an example about how to use the functions we created
def fish_raster():
    ConGdal(input_raster, output_file_1, ">=", pacific_salmon.preferred_flow_velocity, input_raster, 0.0)
    ConGdal(input_raster1, output_file_2, ">=", pacific_salmon.preferred_flow_depth, input_raster1, 0.0)


# after isnull is applied to the raster it only gives 1 and 0, so to get back the original values for the empty cells
def fill_empty_cells():
    ConGdal(IsNull(input_raster).output_raster, output_file, ">=", 1.0, input_raster2, 0.0)


@log_actions
def main(shp_path, fieldname, fieldtype, expression):
    AddField(shp_path, fieldname, fieldtype)
    CalculateField(shp_path, fieldname, expression)
    RasterToPolygon(input_raster1, out_shp)
    TableToNumpyArray(shp_path, fieldname)
    fish_raster()
    fill_empty_cells()


if __name__ == '__main__':
    main(shp_path, fieldname, fieldtype, expression)
