from orageojson.log.flogger import loginfo, logexcep

def setmetadata4SDO(p_conn, p_cursor, p_table):
    #loginfo('--- BO - setmetadata4SDO ---')

    # verify the Feature Table
    for row in p_cursor.execute('''select Table_name, Column_name 
                                        from user_tab_columns
                                        where Data_type like 'SDO_GEOMETRY' AND Table_name=:i_table
                                        order by Table_name''',
                                i_table=p_table):
        try:
            _cursor = p_conn.cursor()

            # delete metadata(table)
            _cursor.execute(''' delete from user_sdo_geom_metadata
                                    where Table_name = :i_tabname AND Column_name = :i_colname''',
                            i_tabname=row[0], i_colname=row[1])

            # get the SRID
            _sql = f"select s.geometry.sdo_srid " \
                   f"  from {row[0]} s" \
                   f"  where rownum<2 "
            _cursor.execute(_sql)
            _row = _cursor.fetchone()

            # set metadata: row[0]:table_name, row[1]:column_name, _row[0]:srid
            set_cursor = p_conn.cursor()
            defmeta = f"insert into user_sdo_geom_metadata (table_name,column_name,diminfo,srid)" \
                      f"  select '{row[0]}' as table_name, '{row[1]}' as column_name, " \
                      f"  mdsys.sdo_dim_array( " \
                      f"     mdsys.SDO_DIM_ELEMENT('X', minX, maxX, 0.05), " \
                      f"     mdsys.SDO_DIM_ELEMENT('Y', minY, maxY, 0.05)  " \
                      f") as diminfo, " \
                      f" {_row[0]} as srid " \
                      f"from ( " \
                      f"select trunc(min(t.x)-1.0) minX, round(max(t.x)+1.0) maxX, " \
                      f"       trunc(min(t.y)-1.0) minY, round(max(t.y)+1.0) maxY  " \
                      f"from {row[0]} b, table(sdo_util.getvertices(b.{row[1]})) t)"

            set_cursor.execute(defmeta)
            set_cursor.execute('commit')
            set_cursor.close

            _cursor.close

        except Exception as e:
            logexcep('$$$ Error setmetadata4SDO: {}'.format(e))
            raise

    loginfo('--- EO - setmetadata4SDO. ---')

    return
# ------------------------------------------------

