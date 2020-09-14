from orageojson.log.flogger import loginfo, logexcep

def crindex4SDO (p_conn, p_cursor, p_table):
    #loginfo('--- BO - crindex4SDO ---')

    # verify the Feature Table
    for row in p_cursor.execute('''select Table_name, Column_name 
                                        from user_tab_columns
                                        where Data_type like 'SDO_GEOMETRY' AND Table_name=:i_table
                                        order by Table_name''',
                                i_table=p_table):
        try:
            _cursor = p_conn.cursor()

            for _row in _cursor.execute('''select Index_name from user_sdo_index_info 
                                            where Table_name= :i_table''',
                                        i_table=p_table):
                try:
                    _drpix = f'drop index IX_SDO_{_row[0]} '
                    drpix_cursor = p_conn.cursor()
                    drpix_cursor.execute(_drpix)
                    drpix_cursor.close
                except Exception as e:
                    logexcep('$$$ Error drop SDO index: {}'.format(e))
                    raise

            _cursor.close

            try:
                defindex = f'create index IX_SDO_{row[0]} on {row[0]}' \
                           f'  ( {row[1]} ) indextype is mdsys.spatial_index_V2'

                ix_cursor = p_conn.cursor()
                ix_cursor.execute(defindex)
                ix_cursor.close

            except Exception as e:
                logexcep('$$$ Error create SDO index: {}'.format(e) + ' : ' + f'IX_SDO_{row[0]}')
                raise

        except Exception as e:
            logexcep('$$$ Error crindex4SDO: {}'.format(e))
            raise

    loginfo('--- EO - crindex4SDO. ---')

    return
#-------------------------------------------------