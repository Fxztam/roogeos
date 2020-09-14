from orageojson.log.flogger import flog
from orageojson.log.flogger import loginfo, logexcep

def table2feature(p_cursor, p_ftable):
    #print('--- BO - table2feature. ---')

    try:
        drp_ftable = f'drop table {p_ftable} purge'
        p_cursor.execute(drp_ftable)
    except Exception as e:
        None

    try:
        None
    except Exception as e:
        None

    try:
        _colist = ['']
        _coldefs = str
        _proplist = ['"<p>" + ']
        _propdefs = str

        for row in p_cursor.execute('''SELECT column_name||'  '||column_type||'  PATH  \'''||xPATH||'\''' def, 
                                        'feature.properties.'||column_name||' + "</br>" ' from (
                                        WITH sel_ AS (
                                          SELECT JSON_DATAGUIDE(ldjson) js_guide
                                          FROM   ld_geojson
                                        )
                                            SELECT upper(substr(gj.jpath,23)) column_name,
                                              CASE upper(gj.type) 
                                                WHEN 'STRING' THEN 'VARCHAR2' ||'('||gj.tlength||')'
                                                WHEN 'NUMBER' THEN 'NUMBER'   ||'('||gj.tlength||')'
                                                WHEN 'OBJECT' THEN 'JSON'
                                                ELSE 'VARCHAR2(256)'
                                              END  column_type,
                                              upper(gj.type)||'('||gj.tlength||')' column_type2,
                                              '$.'||substr(gj.jpath,12) xPATH
                                            FROM   sel_,
                                                   json_table(js_guide, '$[*]'
                                                     COLUMNS
                                                       jpath   VARCHAR2(40) PATH '$."o:path"',
                                                       type    VARCHAR2(10) PATH '$."type"',
                                                       tlength NUMBER       PATH '$."o:length"') gj
                                            WHERE gj.jpath like '$.features.properties.%'
                                            ORDER BY gj.jpath
                                        )                                 
                                    '''):

            _colist.append(row[0]+', ')
            _proplist.append(row[1]+' + ')

        _coldefs = ''.join(_colist)

        _proplist.append('"</p>"')  #ok
        _propdefs = ''.join(_proplist)

    except Exception as e:
        logexcep('$$$ Error load.table2feature(_coldefs) : {}'.format(e))
        raise

    try:
        ftable = f"CREATE TABLE {p_ftable} AS " \
                 f"    SELECT  jt.* FROM ld_geojson,  " \
                 f"                json_table( ldjson, '$.features[*]'  " \
                 f"                    COLUMNS (  {_coldefs} " \
                 f"                               geometry SDO_GEOMETRY  PATH '$.geometry' )) jt "

        p_cursor.execute(ftable)

        # alter table including FID with automatic update it !
        alt_ftable = f"alter table {p_ftable} add " \
                     f"   fid NUMBER(10) GENERATED ALWAYS AS IDENTITY " \
                     f"   (START WITH 1 INCREMENT BY 1) NOT NULL"
        p_cursor.execute(alt_ftable)

        # alter table including status (e.g. geometries) !
        alt_ftable = f"alter table {p_ftable} add status VARCHAR2(1024) "
        p_cursor.execute(alt_ftable)

        # alter table including date of last change !
        alt_ftable = f"alter table {p_ftable} add dlastchange DATE "
        p_cursor.execute(alt_ftable)

    except Exception as e:
        logexcep('$$$ Error load.table2feature(create & alter): {}'.format(e))
        flog('$$$ Error load.table2feature(create & alter): {}'.format(e))
        flog(_coldefs)
        raise

    loginfo('--- EO - table2feature. ---')

    return _propdefs

# ------------------------------------------
