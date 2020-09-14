#------------------------------------------------------------------------------------------------
# Oracle GeoJSON Feature Service
# Input:        Load GeoJSON-file
# Management:   Convert from GeoJSON to SDO Feature <Table>
# Analyze:      Validate & rectify the SDO's
# Presentation: Get GeoJSON data from Oracle RESTful Data Service
#               Create the GeoJSON Vector layer in LeafLet
# Usage > python37 orageojson.py -t <TableName> <username>/password>@<db-SID>
#
# Friedhold Matz - 2020-aug
#
# PYTHONIOENCODING=UTF-8
#------------------------------------------------------------------------------------------------
from orageojson.db.action import *
from orageojson.get_arguments import get_arguments
from orageojson.load.load2table import load2table
from orageojson.load.table2feature import table2feature
from orageojson.ords.ords import createords
from orageojson.sdo.index import crindex4SDO
from orageojson.sdo.qualify import setmetadata4SDO
from orageojson.sdo.validate2 import validate_SDO2
from orageojson.view.map_intern_leaflet2 import map_intern_leaflet
from orageojson.log.flogger import flog, init_logging, loginfo, logexcep

def print_hi(name):
    loginfo(f"§§§  Hey Greetings from {name} here to Frankfurt Clouds (555 km) ! §§§")
#.............................

if __name__ == '__main__':

    try:
        init_logging('--- BO - File logging. ---')
        print_hi('Fried Spremberger')
        table_, connect_, un_, sid_ = get_arguments()
        conn_, cursor_, schema_ = dbopen(connect_)
        validate_SDO2(conn_, cursor_, table_)
        setmetadata4SDO(conn_, cursor_, table_)
        crindex4SDO(conn_, cursor_, table_)
        ords_url_ = createords(conn_, cursor_, schema_, table_)
        # map_intern_leaflet(ords_url_, properties_)

    except Exception as e:
        logexcep('$$$ Error main : {}'.format(e))

    finally:
        dbclose()
        loginfo('§§§ --- Fine. --- §§§')

    #---------------------------- Fried.Matz --------------------------------
