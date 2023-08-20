import tkinter as tk  # standard widgets (Label, Button, etc.)
from tkinter import ttk  # for Combobox widget
from tkinter.messagebox import askokcancel, showinfo  # infoboxes
from tkinter.filedialog import askopenfilename, askdirectory  # select files or folders
import os
import arcpy_to_gdal as arc2gdal
from fun import log_actions


class Arc2GdalApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Arc2Gdal App")
        self.master.iconbitmap("img/icon.ico")
        ww = 800  # width
        wh = 650  # height

        # screen position
        wx = (self.master.winfo_screenwidth() - ww) / 2
        wy = (self.master.winfo_screenheight() - wh) / 2

        # assign geometry
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        self.padx = 5
        self.pady = 5
        self.input_raster = "SELECT"
        self.input_shapefile = "SELECT"
        self.out_folder = "SELECT"
        self.compared_value_raster = "SELECT"
        self.in_true_raster = "SELECT"
        self.field_entry = tk.StringVar()
        self.field_name = self.field_entry.get()
        self.out_folder = "SELECT"
        self.out_shp_fn = r"" + os.path.abspath("") + "/output_file/out_ras2poly.shp"

        # assign space holders around widgets
        self.dx = 5
        self.dy = 5

        # input raster file button
        tk.Button(master, text="Select input raster", width=30,
                  command=lambda: self.set_raster_file()).grid(column=0, row=0,
                                                               padx=self.padx, pady=self.pady,
                                                               sticky=tk.W)
        # select raster file label
        self.raster_label = tk.Label(master, text="Raster file (tif): " + self.input_raster)
        self.raster_label.grid(column=0, columnspan=3, row=1, padx=self.padx, pady=self.pady, sticky=tk.W)

        # input shapefile button
        tk.Button(master, text="Select input shapefile", width=30,
                  command=lambda: self.set_shape_file()).grid(column=1, row=0,
                                                              padx=self.padx, pady=self.pady,
                                                              sticky=tk.W)
        # select raster file label
        self.shapefile_label = tk.Label(master, text="Shapefile (shp): " + self.input_shapefile)
        self.shapefile_label.grid(column=1, columnspan=3, row=1, padx=self.padx, pady=self.pady, sticky=tk.W)

        # output folder button
        tk.Button(master, text="Select output folder", width=30,
                  command=lambda: self.select_out_directory()).grid(column=2, row=0,
                                                                    padx=self.padx, pady=self.pady,
                                                                    sticky=tk.W)
        # select output folder label
        self.output_folder_label = tk.Label(master, text="Output folder: " + self.out_folder)
        self.output_folder_label.grid(column=2, columnspan=3, row=1, padx=self.padx, pady=self.pady, sticky=tk.W)

        # Field Name Entry
        tk.Label(master, text="Enter field name : ", bg="powder blue", fg="medium blue").grid(
            column=0, row=2, padx=self.padx, pady=self.pady, sticky=tk.W)
        tk.Entry(master, bg="alice blue", width=20, textvariable=self.field_entry).grid(column=1, row=2, padx=self.padx,
                                                                                        pady=self.pady, sticky=tk.W)
        # Combobox for field type
        tk.Label(master, text="Choose field type: ", bg="powder blue", fg="medium blue").grid(
            column=0, row=3, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.cbx_field_type = ttk.Combobox(master, width=10)
        self.cbx_field_type.grid(column=1, row=3, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.cbx_field_type['state'] = 'readonly'
        self.cbx_field_type['values'] = ["TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE"]

        self.expression_entry = tk.DoubleVar()
        tk.Label(master, text="Enter expression : ", bg="powder blue", fg="medium blue").grid(
            column=0, row=4, padx=self.padx, pady=self.pady, sticky=tk.W)
        tk.Entry(master, bg="alice blue", width=20, textvariable=self.expression_entry).grid(column=1, row=4,
                                                                                             padx=self.padx,
                                                                                             pady=self.pady,
                                                                                             sticky=tk.W)
        self.expression = self.expression_entry.get()

        # Combobox for operator
        tk.Label(master, text="Choose operator: ", bg="powder blue", fg="medium blue").grid(
            column=0, row=9, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.cbx_operator = ttk.Combobox(master, width=5)
        self.cbx_operator.grid(column=1, row=9, padx=self.padx, pady=self.pady, sticky=tk.W)
        self.cbx_operator['state'] = 'readonly'
        self.cbx_operator['values'] = ["==", "!=", "<=", ">=", "<", ">"]

        # compared value Entry
        self.compared_value_constant_entry = tk.DoubleVar()
        tk.Label(master, text="Enter compared value : ", bg="powder blue", fg="medium blue").grid(
            column=0, row=10, padx=self.padx, pady=self.pady, sticky=tk.W)

        tk.Entry(master, bg="alice blue", width=20, textvariable=self.compared_value_constant_entry).grid(column=1,
                                                                                                          row=10,
                                                                                                          padx=self.padx,
                                                                                                          pady=self.pady,
                                                                                                          sticky=tk.W)
        self.compared_value_constant = self.compared_value_constant_entry.get()

        # input compared value button
        tk.Button(master, text="Select compared value ", width=30,
                  command=lambda: self.set_compared_raster()).grid(column=0, row=11,
                                                                   padx=self.padx, pady=self.pady,
                                                                   sticky=tk.W)

        # define a Checkbutton to use either constant value input or raster as compared value
        self.check_variable_compare = tk.BooleanVar()
        self.cbutton_compare = tk.Checkbutton(master, text="Check this box to use a raster file as compared value",
                                              variable=self.check_variable_compare)
        self.cbutton_compare.grid(sticky=tk.E, column=1, columnspan=2, row=11, padx=5, pady=5)
        self.check_variable_compare.set(False)

        # in_true_raster entry
        self.in_true_raster_value_entry = tk.DoubleVar()
        tk.Label(master, text="in_true_raster : ", bg="powder blue", fg="medium blue").grid(
            column=0, row=12, padx=self.padx, pady=self.pady, sticky=tk.W)
        tk.Entry(master, bg="alice blue", width=20, textvariable=self.in_true_raster_value_entry).grid(column=1, row=12,
                                                                                                       padx=self.padx,
                                                                                                       pady=self.pady,
                                                                                                       sticky=tk.W)
        self.in_true_raster_value = self.in_true_raster_value_entry.get()

        # input in_true_raster button
        tk.Button(master, text="Select in_true_raster ", width=30,
                  command=lambda: self.set_in_true_raster()).grid(column=0, row=13,
                                                                  padx=self.padx, pady=self.pady,
                                                                  sticky=tk.W)

        # define a Checkbutton to use either constant value or raster as in_true_raster value
        self.check_variable_in_true = tk.BooleanVar()
        self.cbutton_in_true = tk.Checkbutton(master,
                                              text="Check this box to use a raster file as in_true_raster value",
                                              variable=self.check_variable_in_true)
        self.cbutton_in_true.grid(sticky=tk.E, column=1, columnspan=2, row=13, padx=5, pady=5)
        self.check_variable_in_true.set(False)

        # in_false_raster entry
        self.in_false_raster_value_entry = tk.DoubleVar()
        tk.Label(master, text="in_false_raster : ", bg="powder blue", fg="medium blue").grid(
            column=0, row=14, padx=self.padx, pady=self.pady, sticky=tk.W)
        tk.Entry(master, bg="alice blue", width=20, textvariable=self.in_false_raster_value_entry).grid(column=1,
                                                                                                        row=14,
                                                                                                        padx=self.padx,
                                                                                                        pady=self.pady,
                                                                                                        sticky=tk.W)
        self.in_false_raster_value = self.in_false_raster_value_entry.get()

        # input in_false_raster button
        tk.Button(master, text="Select in_false_raster ", width=30,
                  command=lambda: self.set_in_false_raster()).grid(column=0, row=15,
                                                                   padx=self.padx, pady=self.pady,
                                                                   sticky=tk.W)

        # define a Checkbutton to use either constant value or raster as in_false_raster value
        self.check_variable_in_false = tk.BooleanVar()
        self.cbutton_in_false = tk.Checkbutton(master,
                                               text="Check this box to use a raster file as in_false_raster value",
                                               variable=self.check_variable_in_false)
        self.cbutton_in_false.grid(sticky=tk.E, column=1, columnspan=2, row=15, padx=5, pady=5)
        self.check_variable_in_true.set(False)

        # define Button to call isnull
        self.is_run = tk.Button(master, bg="white", text="Run IsNull", width=30,
                                command=lambda: self.run_isnull())
        self.is_run.grid(sticky=tk.W, row=7, column=0, padx=self.padx, pady=self.pady)

        # define Button to call raster2poly
        self.ras2poly_run = tk.Button(master, bg="white", text="Run Raster2Polygon", width=30,
                                      command=lambda: self.run_raster2polygon())
        self.ras2poly_run.grid(sticky=tk.W, row=7, column=1, padx=self.padx, pady=self.pady)

        # define Button to call table2array
        self.tab2array_run = tk.Button(master, bg="white", text="Run Table2Array", width=30,
                                       command=lambda: self.run_table2array())
        self.tab2array_run.grid(sticky=tk.W, row=7, column=2, padx=self.padx, pady=self.pady)

        # define Button to call congdal
        self.con_run = tk.Button(master, bg="white", text="Run ConGdal", width=30,
                                 command=lambda: self.run_congdal())
        self.con_run.grid(sticky=tk.W, row=16, column=0, padx=self.padx, pady=self.pady)

        # define Button to call addfield
        self.add_run = tk.Button(master, bg="white", text="Run AddField", width=30,
                                 command=lambda: self.run_add_field())
        self.add_run.grid(sticky=tk.W, row=8, column=0, padx=self.padx, pady=self.pady)

        # define Button to call calculatefield
        self.cal_run = tk.Button(master, bg="white", text="Run CalculateField", width=30,
                                 command=lambda: self.run_calculate_field())
        self.cal_run.grid(sticky=tk.W, row=8, column=1, padx=self.padx, pady=self.pady)


        # Label for info
        self.run_label = tk.Label(master, fg="forest green", text="")
        self.run_label.grid(column=0, columnspan=3, row=18, padx=self.padx, pady=self.pady, sticky=tk.W)

    def select_file(self, description, file_type):
        return askopenfilename(filetypes=[(description, file_type)],
                               initialdir=os.path.abspath(""),
                               title="Select a %s file" % file_type,
                               parent=self)

    def set_raster_file(self):
        self.input_raster = self.select_file("raster file", "tif")
        # update raster file label
        self.raster_label.config(text="Raster file(tif) selected")

    def set_compared_raster(self):
        self.compared_value_raster = self.select_file("raster file", "tif")

    def set_in_true_raster(self):
        self.in_true_raster = self.select_file("raster file", "tif")

    def set_in_false_raster(self):
        self.in_false_raster = self.select_file("raster file", "tif")

    def set_shape_file(self):
        shp_driver = arc2gdal.ogr.GetDriverByName("ESRI Shapefile")
        self.input_shapefile = shp_driver.Open(self.select_file("shapefile", "shp"),
                                               1)  # update =1 for rewriting
        # update shape file label
        self.shapefile_label.config(text="Shapefile(shp) selected")

    def select_out_directory(self):
        self.out_folder = askdirectory()
        # update output folder label
        self.output_folder_label.config(text="Output folder: " + self.out_folder)

    @log_actions
    def run_isnull(self):
        # ensure that user selected the necessary input
        if not self.valid_selections_raster():
            return -1
        if askokcancel("Start operation?", "Click OK to start the operation."):
            arc2gdal.IsNull(self.input_raster)
            self.is_run.config(fg="forest green")
            self.run_label.config(text="Success: Raster saved " + os.path.abspath("") + "/output_file/outputIsNull.tif")

    @log_actions
    def run_congdal(self):
        # ensure that user selected the necessary input
        if not self.valid_selections_raster():
            return -1
        self.operator = str(self.cbx_operator.get())
        self.compared_value_constant = self.compared_value_constant_entry.get()
        self.in_true_raster_value = self.in_true_raster_value_entry.get()
        self.in_false_raster_value = self.in_false_raster_value_entry.get()

        if askokcancel("Start operation?", "Click OK to start the operation."):
            if not self.check_variable_compare.get():
                if not self.check_variable_in_true.get():
                    if not self.check_variable_in_false.get():
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_constant,
                                         self.in_true_raster_value,
                                         self.in_false_raster_value)
                    else:
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_constant,
                                         self.in_true_raster_value,
                                         self.in_false_raster)
                else:
                    if not self.check_variable_in_false.get():
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_constant,
                                         self.in_true_raster,
                                         self.in_false_raster_value)
                    else:
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_constant,
                                         self.in_true_raster,
                                         self.in_false_raster)
            else:
                if not self.check_variable_in_true.get():
                    if not self.check_variable_in_false.get():
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_raster,
                                         self.in_true_raster_value,
                                         self.in_false_raster_value)
                    else:
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_raster,
                                         self.in_true_raster_value,
                                         self.in_false_raster)
                else:
                    if not self.check_variable_in_false:
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_raster,
                                         self.in_true_raster,
                                         self.in_false_raster_value)
                    else:
                        arc2gdal.ConGdal(self.input_raster, self.out_folder, self.operator, self.compared_value_raster,
                                         self.in_true_raster,
                                         self.in_false_raster)
            self.con_run.config(fg="forest green")
            self.run_label.config(text="Success: Raster saved " + self.out_folder + "/Con_out_raster.tif")

    @log_actions
    def run_raster2polygon(self):
        # ensure that user selected the necessary input
        if not self.valid_selections_raster():
            return -1
        if askokcancel("Start operation?", "Click OK to start the operation."):
            arc2gdal.RasterToPolygon(self.input_raster, self.out_shp_fn)
            self.ras2poly_run.config(fg="forest green")
            self.run_label.config(text="Success: Wrote %s" % str(self.out_shp_fn))

    @log_actions
    def run_table2array(self):
        # ensure that user selected the necessary input
        if not self.valid_selections_shapefile():
            return -1
        self.field_name = self.field_entry.get()
        if askokcancel("Start operation?", "Click OK to start the operation."):
            arc2gdal.TableToNumpyArray(self.input_shapefile, self.field_name)
            self.tab2array_run.config(fg="forest green")
            self.run_label.config(text="Success: Array created")

    @log_actions
    def run_add_field(self):
        # ensure that user selected the necessary input
        if not self.valid_selections_shapefile():
            return -1

        self.field_name = self.field_entry.get()
        self.field_type = str(self.cbx_field_type.get())

        if askokcancel("Start operation?", "Click OK to start the operation."):
            arc2gdal.AddField(self.input_shapefile, self.field_name, self.field_type)
            self.add_run.config(fg="forest green")
            self.run_label.config(text="Success: New field \"" + str(self.field_name)
                                       + "\" is added to the input shapefile.")

    @log_actions
    def run_calculate_field(self):
        # ensure that user selected the necessary input
        if not self.valid_selections_shapefile():
            return -1

        self.field_name = self.field_entry.get()
        self.expression = self.expression_entry.get()
        if askokcancel("Start operation?", "Click OK to start the operation."):
            arc2gdal.CalculateField(self.input_shapefile, self.field_name, self.expression)
            self.cal_run.config(fg="forest green")
            self.run_label.config(
                text="Success: expression:\"" + str(self.expression) + "\" is added to the field \"" + str(
                    self.field_name) + "\".")


    def valid_selections_raster(self):
        if "SELECT" in self.input_raster:
            showinfo("ERROR", "Select raster file.")
            return False
        return True

    def valid_selections_shapefile(self):
        if "SELECT" in self.input_shapefile:
            showinfo("ERROR", "Select shape file.")
            return False
        return True


if __name__ == '__main__':
    Arc2GdalApp().mainloop()
