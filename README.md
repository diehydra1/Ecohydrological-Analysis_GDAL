# Arcpy2Gdal

Arcpy is a python package providing an effective way to perform geographic data analysis, data conversion, data management and map automation. Arcpy can only be used with a license, not freely. Therefore, the aim of this project was to create few useful functions from the arcpy library using GDAL as an open source so that it can be used without having any problem of license.
We selected six functions that are used in [cConnectivityAnalysis.py](https://github.com/RiverArchitect/program/blob/master/StrandingRisk/cConnectivityAnalysis.py) of the StrandingRisk module, namely: Con; IsNull; RasterToPolygon_conversion; AddField_management; CalculateField_management and TableToNumPyArray.



## Table of content

- [Code description](#Code-description)
- [Getting Started](#Getting-Started)
  - [Prerequisites](#Prerequisites)
  - [Installing](#Installing)
- [Usage](#Usage)
- [Authors](#Authors)
- [License](#license)
- [Acknowledgements](#acknowledgements)



## Code description

### Class Con

**Con** is part of Conditional toolset of ArcGIS Pro, whose function is to perform conditional if/else evaluation on each of the input cells of an input raster.

The syntax of the con function in arcpy is as following:

```python
Con(in_conditional_raster, in_true_raster_or_constant, {in_false_raster_or_constant}, {where_clause})
```

We changed the syntax a little, as there were few problems concerned with using the same syntax of arcpy
in gdal. These problems will also occur in arcpy **con** function, but to bypass those arcpy has another function for it. By changing the syntax that does not mean that the inputs are different. If in some already written code one wants to use congdal rathe than the arcpy con function, there will be no need to create new variables to run it.

The syntax for con in gdal that we have created would be as following:

```python
con_gdal(in_con_raster, output_folder, operator, compared_value, in_true_raster, in_false_raster=np.nan):
```

Using a less than or greater then operator between a string and a value causes an error, as the computer can not evaluate between these two types. Therefore, we used the comparison operator as a separate argument in the syntax to bypass the error.

`in_con_raster`: The raster file whose cells will be evaluated with con function. It needs to be a raster file.

`output_folder`: This is an additional argument that we have provided to allow the user to select the folder by choice where to store/save the output of the function.

`operator`:It needs to be a string type, so it needs to be in `""`. The options availabe are `">"`, `">="`, `"<"`, `"<="`, `"=="`, `"!="`.

`compare_vale`: It can be a constant float value or a raster file, which will be compared by the operator with the `in_con_raster`.

`in_true_raster`: It can be a constant float value or a raster file, this value will be used when the condition is True in that specific cell.

`in_false_raster`: It can be a constant float value or a raster file, this value will be used when the condition is False in that specific cell. This argument has a default value of 'np.nan', so if the value is not provided the default value will take action.


The `congdal` uses `geo.raster2array` for converting raster to an array, so that the comparison is being done by applying if/else statments. Once that is being done `geo.creat_raster` is used to change the final array back into a raster. The output raster will have the same size and ESPG code as of `in_con_raster`.

The following picture shows how the function provides the output raster:





![](/img/congdal_func.PNG)








```python
con_gdal(in_con_raster, output_folder, ">=", 3.0, 1.0, 0.0):
```




### Class IsNull

The function of IsNull in arcpy is to determine which values from the input raster are NoData. It will return a value of 1 if the input value is NoData and 0 for cells that are not.

The syntax of the **IsNull** function in arcpy is as following:

```python
IsNull(in_raster)
```

`in_raster` is the input raster being tested to identify the cells that are NoData (null).

The `out_raster` is the return value of IsNull. The output identifies with an integer value of 1 which cells in the input are NoData. If the input is any other value, the output is 0.

Since in gdal, it's not possible to do the calculation of raster directly as in arcpy. The idea of this class is to first read the input raster as an array, then the `pandas.isnull` is used to do the same calculation on array. Later the `numpy.array().astype(int)` is used to convert the Boolean number to Integer. Finally the array is written back to the raster. The functions in geo_utils package are used to open and create rasters.

The syntax of the **IsNull** function in gdal is as following:

```python
IsNull(raster_file_name)
```

`raster_file_name` is the input raster. 

`IsNull(input_raster).output_raster` is the output raster.

The Class **IsNull** contains two methods, one `__init__` method and one class method `isnull`.

In `__init__`, the arguments of input raster and output raster are defined,  the class method`isnull` is called to run the operation.

In method `isnull`, the `geo.raster2array` is used to load the raster array and geo info, then the NoData value is determined by `pd.isnull`, `numpy.array().astype(int)` then convert the Boolean value to Integer(True = 1, False = 0), and finally `geo.create_raster` use the raster array and geo info loaded before to create a new raster file. The output raster file is saved at output_file folder. And the return value of this method is the output raster file.

The difference of raster after Isnull operation looks like this:

![](/img/Isnull_conparison.png)



### Class RasterToPolygon

Raster to Polygon conversion in arcpy converts a raster dataset to the polygon features where raster dataset is being provided as input. 
In commercial arcpy, with the compulsory parameters- in_raster and out_polygon_features to provide flexibility in the output polygon features. 

The syntax of the **RasterToPolygon** Conversion in arcpy is as following:

```python
arcpy.conversion.RasterToPolygon(in_raster, out_polygon_features, {simplify}, {raster_field}, {create_multipart_features}, {max_vertices_per_feature})
```

The Syntax for the conversion of **RasterToPolygon** in gdal as following:

```python
raster2polygon(file_name, out_shp_fn, band_number=1, field_name="values")
```
Within the **RasterToPolygon** class, to make the conversion process easier from raster dataset to polygon shapefile, in gdal the powerful tool named `Polygonize` is offered that helps to write a simple `raster2polygon` function. `gdal.Polygonize` function strictly limited to the integer data type only. To resolve the basic drawback, we use `float2int` function as prerequisite. As it also attributes randomly, to store the original value range, `float2int` function is being required which convert any given raster `file_name` into `float2int` purely integer values. The required relevant functions for `float2int` have been imported from `geo_utils` folder and the function itself. `create_shp` function has been used to create a new shape file named `out_shp_fn`. To open raster band number, `band_number` is set as input argument which is 1. Optional input argument `field_name` is set to "values" which is used to store raster pixel values.Upon successfully running of **RasterToPolygon** class it will print a succces message with the directory of the shapefile and returns the shapefile.

`file_name` This is targeted raster file name, including directory; must end on ".tif"

`out_shp_fn` This is the shapefile name; must be end on .shp

Inside the `raster2polygon` function `gdal.Polygonize` produces vector polygon for all connected regions through sharing a common pixel values in the raster dataset. The created output layer will contain the respective polygon features. The polygon geometries will be in the georeferenced coordinate system according to the source dataset.This function features the following parameters:

`hSrcBand`: the source raster band to be processed.

`hMaskBand`: an optional mask band. All pixels in the mask band with a value other than zero will be considered suitable for collection as polygons.For this parameter the value is set to `None` in the code.

`destination Layer`: the vector feature layer to which the polygons should be written.

`field ID`: the attribute field index indicating the feature attribute which is set to 0.

`papszOptions`: a name/value list of additional options

`pfnProgress`: callback for reporting algorithm progress matching the GDALProgressFunc() semantics where the value is set to `None`.

`gdal.Polygonize` function also creates a `.prj` projection file using the spatial reference system of the input raster with the `get_srs` function which is imported from `geo_utils` folder.

The converted shapfile from raster after **RasterToPolygon** operation looks as follows:

![](/img/RasterToPolygon_Conversion.jpg)



### Class TableToNumpyArray

In arcpy, **TableToNumpyArray** converts a given table to NumPy structured array where `in_table` and `field_name` act as compulsory parameters.

Syntax of **TableToNumPyArray** in arcy is as following: 

```python
arcpy.da.TableToNumPyArray (in_table, field_names, {where_clause}, {skip_nulls}, {null_value})
```
The syntax for **TableToNumpyArray** in gdal is as following:

```python
TableToNumpyArray(shp_file, field_name)
```
`shp_file`: is the provided input shapefile for which specific field will be added.

`field_name`: is the name of the field of the shapefile feature.

To be precise, a shapefile cannot be converted, but can be burned onto a raster. For that reason, the values stored in a field of a shapefile feature are used (burned) for pixel values in a new raster. Here, `gdal.RasterizeLayer`comes with a powerful option that easily converts a shapefile into a raster which is identical to `gdal.Polygonize` as well.
This `gdal.RasterizeLayer` features the following parameters:

`target_ds`:This is targeted raster dataset.

`bands`:The value of the band is integer datatype. It can be increased to define more raster bands and assign other values like from other fields of the source shapefile. The value is set to `[1]`.

`source_lyr`:It gives the layer with the features to burn to the raster.

`options=["ATTRIBUTE=" + self.field_name]`: This parameter defines the field name with values to burn.

Finally, after formulating spatial references, the new raster converted into a structed array and returns the new array.

The converted array from the shapefile after **TableToNumpyArray** operation looks as follows:

![](/img/tabletonumpyarray_conversion.jpg)


### Class AddField

In arcpy, the function of Add Field is to add a new field to a table or the table of a feature class or feature layer, as well as to rasters with attribute tables.

The syntax of the **AddField**  in arcpy is as following:

```python
arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
```

The syntax for **AddField** in gdal  is simplified as following:

```python
AddField(shp_path, fieldname, fieldtype)
```

`shp_path` is the input shapefile to which the specified field will be added. 

`fieldname` is the name of the field that will be added to the input table.

The `fieldtype` that can be chosen are:

- TEXT —Any string of characters.
- FLOAT — Fractional numbers between -3.4E38 and 1.2E38.
- DOUBLE — Fractional numbers between -2.2E308 and 1.8E308.
- SHORT — Whole numbers between -32,768 and 32,767.
- LONG — Whole numbers between -2,147,483,648 and 2,147,483,647.
- DATE —Date and/or time.

The Class Addfield contains two methods, one `__init__ `method and one class method `add_field`.

In `__init__`, the arguments of input shapefile, field name and field type are defined. The class method`add_field` is called to run the operation.

In method `add_field`, the `ogr` module of  gdal is used to handle the shapefile.

The shapefile layer object is instantiated with `GetLayer()`.

The `if/elif` is used to determine the field type.

Different field types are assigned by `ogr.OFTString`, `ogr.OFSTFloat32`, `ogr.OFTReal`, `ogr.OFSTInt16`, `ogr.OFTInteger`, `ogr.OFTDate`.

A new field is added with `ogr.FieldDefn(self.field_name, field_type)` and created with `CreateField()`.

The operations are written to the shapefile by overwriting the layer object with `None`.

**Note:** The method `add_field` has no return value, the changes are directly made to the `shp_path`.

The following line provides an example of calling the `add_field` method :

```python
AddField(shp_path, fieldname = "Area", fieldtype = "DOUBLE")
```

After a successful running, the new field "Area" with type "DOUBLE" can be seen in QGIS.

![](/img/add_field.png)





### Class Calculate Field

The function of **Calculate Field** in acrpy is to calculate the values of a field for a feature class, feature layer, or raster.

The syntax of the **Calculate Field** in arcpy is as following:

```python
arcpy.management.AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
```

Due to the limitations, the syntax for **Calculate Field** in gdal is simplified as following:

```python
CalculateField(shp_path, fieldname, expression)
```

`shp_path `  is the input shapefile containing the field that will be updated with the new value.

`fieldname` is the field that will be updated with the new value.

`expression` is the value that will be added to the chosen field.

The Class **CalculatedField**  contains two methods, one `__init__ `method and one class method calculate_field.

In `__init__`, the arguments of input shapefile, field name and expression are defined. The class method `calculate_field` is called to run the operation.

In method `calculate_field`, the `ogr` module of  gdal is used to handle the shapefile.

The shapefile layer object is instantiated with `GetLayer()`.

A feature is created with `ogr.Feature(in_shp_lyr.GetLayerDefn())` as child of the layer.

The expression value is defined to the given field with `feature.SetField(self.field_name, self.expression)`.

The new feature is appended to the layer with `in_shp_lyr.CreateFeature(feature)`.

The operations are written to the shapefile by overwriting the layer object with `None`.

**Note:** The method `calculate_field` has no return value, the changes are directly made to the `shp_path`.

The following line provides an example of calling the `calculate_field` method :

```python
CalculateField(shp_path, fieldname ="Area", expression="3 ** 2")
```

After a successful running, the expression `3 ** 2` is added to the existing field `"Area"`.

![](/img/calculate_field.png)


### Main()
In `main.py` we import all the classes that we have created as stated above along with `config.py` and `fun.py` for logging purposes.
We have also imported another class called `fish.py` which is just examplery purposes taken from the lecture notes provided for the course by Dr. Sc. Sebastian Schwindt. 
Required input files and arguments are defined in it as well, which can be changed to however the user wants to use it. 
There are two functions in the `main.py` called `fish_raster` and  `fill_empty_cells`. These are part of the example which we wanted to show.
In `fish_raster` we just compare depth and velocity preffered by a specific fish species with the raster of a section of river provided in the input_file. The results are saved in output_file/output_file_fish1 and output_file/output_file_fish2.
In `fill_empty_cells` we have used both `IsNull` and `ConGdal`. As `IsNull` gives an output raster with True(1) and False(0), we try to put the original cell values of that raster back where the cell is False(0). The output result is saved in output_file.

### Code Structure of Arc2GdalApp

![](/img/final_flowchart.jpg)

The diagram above demonstrates how the interconnected classes and features are contributing to the **Arc2GdalApp**


## Getting Started

### Prerequisites

To run **Arcpy2Gdal** the following needs to be installed into the environment.

1. Open anaconda prompt.

2. Activate the environment you want to work with.

   ```
   conda activate [enviornment name] 
   ```

3. Install the following by using given commands.

   -osgeo

   ```
   conda install -c conda-forge gdal
   ```

   -NumPy 

   ```
   conda install numpy
   ```

   -pandas

   ```
   conda install pandas
   ```

   -Urllib

   ```
   conda install -c anaconda urllib3
   ```

   

### Installing 

First, Open git bash. Navigate to the directory, where one intends to clone the folder to by using

``` 
cd "[E:\.......]"
```

Type the following:

```
git clone https://github.tik.uni-stuttgart.de/st168552/swan.git
```



## Usage

After cloning, open Pycharm, choose File--Open, find the directory where the project is cloned. Click "OK".

Choose the python(hypy) interpreter.

Mark the `arcpy_to_gdal` folder as source root:

![](/img/directory.png)


Then run  `main.py`, a successful run of the script `main.py` should look like this (in *PyCharm*):

![](/img/main.png)







### GUI

To run the gdal functions separately, a GUI is created.


![gui](/img/gui.png)




The usage of different gdal functions are explained as followings:

- [IsNull]

  - Click `select input raster` to load the input raster file.
  - Then, click  `Run isnull` , the output file is saved at the output_folder.
- [Raster2Polygon]
  - Click `select input raster` to load the raster file.
  - Click `Run Raster2Polygon` , the output shapefile is saved at the output_folder.
- [Table2Array]

  - Click `select input shapefile` to load the input shape file.
  - Click `Run Table2Array` , the Array is printed in the Pycharm console.
- [AddField]
  - Click `select input shapefile` to load the input shape file.
  - Enter the field name in the entry box.
  - Choose the field type in the combo box.
  - Click `Run Addfield`, the new field is added to the selected input shape file.
- [CalculatedField]
  - Click `select in input shapefile` to load the input shape file.
  - Enter the field name in the entry box.
  - Enter the expression in the entry box.(Note: due to the limitation, this gui can only accept float number as expression now, further development will be brought to the project in the future.)
  - Click `Run CalculateField`, the expression is added to the given field of the selected shapefile.
- [ConGdal]
  - Click `select input raster` to load the input raster file.
  - Click `select output folder`, to specify the location for saving the output results of the functions.
  - Click on the `drop down` option for choosing operator.
  - Enter a constant float value in the `Enter compared value` or use a raster by clicking on `Select compared value` and checking the small box given opposite to the button.
  - Enter a constant float value in the `True raster` or use a raster by clicking on `Select true raster` and checking the small box given opposite to the button.
  - Enter a constant float value in the `False raster` or use a raster by clicking on `Select false raster` and checking the small box given opposite to the button.
  - Click `Run congdal`, the ouput raster file would be saved in the specified location.



## Authors

* **Siyuan Niu** 
  - -_Class Isnull_-  [Isnull](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/IsNull.py)
  - -_Class AddField_-  [AddField](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/addfieldmanagement.py)
  - -_Class CalculateField_-  [CalculateField](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/calculatefield.py)
  - -_GUI_- [GUI](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/gui.py)
  - -_Readme_- [Readme](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/README.md)
  - -_fun_- [fun](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/fun.py)
  - -_main_- [main](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/main.py)
* **Baibrus** 
  - -_Class Con_-  [ConGdal](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/congdal.py)
  - -_GUI_- [GUI](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/gui.py)
  - -_Readme_- [Readme](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/README.md)
  - -_main_- [main](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/main.py)
  - -_config_- [config](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/config.py)
  - -_fun_- [fun](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/fun.py)
* **Arif** 
  - -_Class RasterToPolygon_-  [RasterToPolygon](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/RasterToPolygon.py)
  - -_Class TableToNumpyArray_- [TableToNumpyArray](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/TableToNumpyArray.py)
  - -_config_- [config](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/config.py)
  - -_Readme_- [Readme](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/README.md)
  - -_main_- [main](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/main.py)
  - -_Code Structure of Arc2GdalApp_- [Code Structure of Arc2GdalApp](https://github.tik.uni-stuttgart.de/st168552/swan/img/final_flowchart.jpg)
  


## License

[GNU General Public License](https://github.tik.uni-stuttgart.de/st168552/swan/blob/master/LICENSE)

## Acknowledgements

This project is finalized under the supervision of **Dr. Sc. Sebastian Schwindt**, Institute for Modeling Hydraulic and Environmental Systems as a part of the course- Python Programming for Water Resources Engineering and Research, Winter' 20/21 at Universität Stuttgart.

