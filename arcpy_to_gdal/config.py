try:
    import os
    import logging
except ImportError:
    print("ERROR: Cannot import basic Python libraries.")

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("ERROR: Cannot import SciPy libraries.")

try:
    from gdal import *
    import gdal
except ImportError:
    print("ERROR: Cannot import gdal library.")

try:
    import geo_utils as geo
except ImportError:
    print("ERROR: Cannot import geo_utils.")



