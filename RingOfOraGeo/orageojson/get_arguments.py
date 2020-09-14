#----------------------------------------------------
#  Get arguments: > file -t table_name connect_string
#  Friedhold Matz - 2020-aug
#----------------------------------------------------

from orageojson.log.flogger import loginfo, logexcep
import argparse

def get_arguments():
    arg_parser = argparse.ArgumentParser(description='`Ring of Oracle GeoJSON`')

    msg = 'File of GeoJSON'
    arg_parser.add_argument('geojson',  help=msg)

    msg2 = 'Table Name (default: geojson)'
    arg_parser.add_argument('-t', '--table', default='geojson', help=msg2)

    msg3 = 'Connection : <username>/<password>@<OracleATP-SID> '
    arg_parser.add_argument('connection',  help=msg3)

    try:
        args = arg_parser.parse_args()

        file_ = args.geojson
        table_ = args.table
        connect_ = args.connection

        csp1_ = connect_.split('@')
        sid_ = csp1_[1]

        csp2_ = csp1_[0].split('/')
        un_ = csp2_[0]

    except Exception as e:
        logexcep("$$$ ERROR in connect string `<un>/<pw>@<Oracle-SID>`! Found: " + connect_)
        raise

    return file_, table_.upper(), connect_, un_, sid_

