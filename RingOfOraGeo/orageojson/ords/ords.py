#-------------------------------------------------
#  Create ORDS as native GeoJSON service
#  Friedhold Matz - 2020-aug
#-------------------------------------------------
from orageojson.log.flogger import loginfo, logexcep, flog
from orageojson.ords.get_ords_base_url import get_ords_base_url

def createords(p_conn, p_cursor, p_schema, p_table):
    #loginfo('--- BO - crgeojsonords. ---:' + p_table)

    c_ords_module_name = 'geo_api'

    # create the GeoJSON Feature Collection View and the Oracle RESTful Data Service
    for row in p_cursor.execute('''select Table_name, Column_name 
                                         from user_tab_columns
                                         where Data_type like 'SDO_GEOMETRY' AND Table_name=:i_table
                                         order by Table_name''',
                                i_table=p_table):

        _cursor = p_conn.cursor()
        _colist = ['']
        _coldefs = str

        # get the property column names of the Feature Table
        for _row in _cursor.execute('''select '\'''||Column_name||'\'' value '|| Column_name 
                                            from user_tab_columns
                                            where Data_type NOT like 'SDO_GEOMETRY' AND Table_name=:j_table
                                    ''', j_table=p_table):

            _colist.append(_row[0] + ',')

        #print(_colist)
        _coldefs = ''.join(_colist)

        _coldefs = _coldefs[:-1:] + '),'
        #print(_coldefs)

        # change last , with )
        _cursor.close()

        try:
            # create the native GeoJSON Feature Collection view
            defview = f"create or replace view v_feature_{row[0]} as " \
                      f"  select json_object( " \
                      f"             'type' value 'FeatureCollection', " \
                      f"             'features' value json_arrayagg( " \
                      f"                 json_object( " \
                      f"                     'fid' value c.FID, " \
                      f"                     'type' value 'Feature', " \
                      f"                     'properties' value json_object( " \
                      f"                         {_coldefs} " \
                      f"                     'geometry' value c.{row[1]}.get_geojson() format json " \
                      f"                 returning clob " \
                      f"             ) returning clob " \
                      f"         ) returning clob " \
                      f") as feature " \
                      f"  from {row[0]} c"

            view_cursor = p_conn.cursor()
            view_cursor.execute(defview)
            view_cursor.close()

        except Exception as e:
            logexcep('$$$ Error ords.createords(create view): {}'.format(e))
            raise

        try:
            # create the native GeoJSON ORDS
            plsql = f"BEGIN " \
                    f"        ORDS.ENABLE_SCHEMA( " \
                    f"            p_enabled             => TRUE, " \
                    f"            p_schema              => upper(\'{p_schema}\'), " \
                    f"            p_url_mapping_type    => 'BASE_PATH', " \
                    f"            p_url_mapping_pattern => \'{p_schema}\', " \
                    f"            p_auto_rest_auth      => FALSE); " \
                    f"    END; "

            plsql2 = f"BEGIN " \
                     f"       ORDS.DEFINE_MODULE( " \
                     f"           p_module_name => \'{c_ords_module_name}\', " \
                     f"           p_base_path => '/geojson/', " \
                     f"           p_items_per_page => 25, " \
                     f"           p_status => 'PUBLISHED', " \
                     f"           p_comments => 'Module for schema.FeatureTable'); " \
                     f"  END; "

            plsql3 = f"BEGIN " \
                     f"       ORDS.DEFINE_TEMPLATE( " \
                     f"           p_module_name => \'{c_ords_module_name}\', " \
                     f"           p_pattern => 'media', " \
                     f"           p_priority => 0, " \
                     f"           p_etag_type => 'HASH', " \
                     f"           p_etag_query => NULL, " \
                     f"           p_comments => 'Template for schema.FeatureTable'); " \
                     f"  END; " \

            plsql4 = f"BEGIN " \
                     f"     ORDS.DEFINE_HANDLER( " \
                     f"         p_module_name => \'{c_ords_module_name}\', " \
                     f"         p_pattern => 'media', " \
                     f"         p_method => 'GET', " \
                     f"         p_source_type => 'resource/lob', " \
                     f"         p_items_per_page => 25, " \
                     f"         p_mimes_allowed => '', " \
                     f"         p_comments => 'Media Handler for schema.FeatureTable', " \
                     f"         p_source => 'select ''application/json; charset=utf-8'', feature from v_feature_{p_table}' " \
                     f"       ); " \
                     f"END; "

            commit = '''COMMIT'''

            ords_cursor = p_conn.cursor()

            ords_cursor.execute(plsql)
            ords_cursor.execute(plsql2)
            ords_cursor.execute(plsql3)
            ords_cursor.execute(plsql4)
            ords_cursor.execute(commit)

            # get the ORDS common base url
            for _row in ords_cursor.execute( '''  SELECT             
                                                name,         
                                                uri_prefix,   
                                                uri_template, 
                                                method,       
                                                source_type,  
                                                SOURCE        
                                            FROM                       
                                                user_ords_modules a,   
                                                user_ords_templates b, 
                                                user_ords_handlers c   
                                             WHERE                     
                                                 a.id = b.module_id    
                                                 AND   b.id = c.template_id 
                                                 AND   a.name=:l_module
                                            ''', l_module=c_ords_module_name):

                ords_url_ = get_ords_base_url() +p_schema+ '/' +_row[1]+_row[2]

                flog(ords_url_, 'ORDS')  # => `./flog-ORDS.log`

            ords_cursor.close

        except Exception as e:
            logexcep('$$$ Error ords.createords(create ords): {}'.format(e))
            raise

    loginfo('--- EO - crgeojsonords. ---')

    # return url
    return ords_url_
#-------------------------------------------------
