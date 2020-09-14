from orageojson.log.flogger import loginfo, logexcep, logcrit

def validate_SDO2 (p_conn, p_cursor, p_ftable):
    #loginfo('--- BO - validate_SDO2 ---')

    cntErrors = None

    # -- drop & create feature error table
    err_cursor = p_conn.cursor()
    try:
        drp_ftable = f"drop table {p_ftable}_errors "
        err_cursor.execute(drp_ftable)
    except Exception as e:
        None

    try:
        ferrtable = f"CREATE TABLE {p_ftable}_errors " \
                    f"  AS SELECT * FROM {p_ftable} "
        err_cursor.execute(ferrtable)
        ferrtable = f"TRUNCATE TABLE {p_ftable}_errors "
        err_cursor.execute(ferrtable)
        err_cursor.execute('''COMMIT''')
    except Exception as e:
        logexcep('$$$ Error validate(create <tab>_errors) : {}')#.format(e))
        raise

    #loginfo('--- BEFORE TABLE - LOOP ---')

    # verify the Feature Table
    for row in p_cursor.execute('''SELECT Table_name, Column_name 
                                     FROM user_tab_columns
                                        WHERE Data_type like 'SDO_GEOMETRY' AND Table_name=:i_table
                                        ORDER BY Table_name ''',
                                i_table=p_ftable):

        try:
            val_cursor = p_conn.cursor()

            val_block = f"  DECLARE \n" \
                        f"       l_geometry_fixed SDO_GEOMETRY; \n" \
                        f"       -- Declare a custom exception for uncorrectable geometries \n" \
                        f"       -- 'ORA-13199: the given geometry cannot be rectified ' \n" \
                        f"       cannot_rectify exception; \n" \
                        f"       pragma exception_init(cannot_rectify, -13199); \n" \
                        f"    BEGIN \n" \
                        f"       EXECUTE IMMEDIATE 'DROP TABLE {p_ftable}_errors'; \n" \
                        f"       EXECUTE IMMEDIATE 'CREATE TABLE {p_ftable}_errors AS SELECT * from {p_ftable}'; \n" \
                        f"       EXECUTE IMMEDIATE 'TRUNCATE TABLE {p_ftable}_errors'; \n" \
                        f"       FOR g IN ( SELECT fid, f.rowid, f.{row[1]}, sdo_geom.validate_geometry_with_context({row[1]}, 0.005) result \n" \
                        f"          FROM {p_ftable} f \n" \
                        f"            WHERE sdo_geom.validate_geometry_with_context({row[1]}, 0.005) != 'TRUE' \n" \
                        f"        ) \n" \
                        f"       LOOP \n" \
                        f"         BEGIN  \n" \
                        f"           l_geometry_fixed := sdo_util.rectify_geometry (g.{row[1]}, 0.005); \n" \
                        f"           -- Update the base table with the rectified geometry  \n" \
                        f"           UPDATE {p_ftable} u SET geometry = l_geometry_fixed  \n" \
                        f"              WHERE u.rowid = g.rowid;  \n" \
                        f"           COMMIT;  \n" \
                        f"         EXCEPTION WHEN cannot_rectify THEN  \n" \
                        f"            -- Move error_record from `tab` to `tab_errors`, \n" \
                        f"            -- set status in `tab_errors`  \n" \
                        f"            -- delete error_record in `tab` \n" \
                        f"           INSERT INTO {p_ftable}_errors  \n" \
                        f"             SELECT * FROM {p_ftable} i  \n" \
                        f"                WHERE i.rowid = g.rowid;  \n" \
                        f"           UPDATE {p_ftable}_errors eu SET status = g.result  \n" \
                        f"               WHERE eu.rowid = g.rowid;  \n" \
                        f"           DELETE FROM {p_ftable} d WHERE d.rowid = g.rowid;  \n" \
                        f"           COMMIT;  \n" \
                        f"         END;  \n" \
                        f"       END LOOP validate_rectify;  \n" \
                        f"  END validate; \n"


            val_cursor.execute(val_block)

            val_cursor.execute('commit')

        except Exception as e:
            logexcep('$$$ Error validate: {}'.format(e))
            raise

        #loginfo("--- Get Count1 ---")
        # if no valid SDO data then sense .
        try:
            _cursor = p_conn.cursor()
            # get one
            _sql = f"SELECT count(*) " \
                   f"   FROM  {row[0]} s"
            _cursor.execute(_sql)
            count = _cursor.fetchone()[0]

        except Exception as e:
            logexcep('$$$ Error validate: {}'.format(e))
            raise

        if (count == 0):
            logcrit('$$$ Error NO VALIDATED SDO data : Sense . $$$')
            raise

        cnterrors = 5
        #loginfo("--- Get Count2 ---")
        # get one
        try:
            _sql = f"SELECT count(*) " \
                   f"   FROM  {row[0]}_errors"
            _cursor.execute(_sql)
            cnterrors = _cursor.fetchone()[0]
        except Exception as e:
            logexcep('$$$ Error validate: {}'.format(e))
            raise

        #loginfo("--- EO - counts. ---")

    loginfo('--- EO - validate_SDO . Number of Records: {a} / Errors: {b}'.format(a=count, b=cnterrors) )

    return
# ------------------------------------