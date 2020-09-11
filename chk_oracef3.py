#--------------------------------------------------
# --- Test the cx_Oracle connection and cefpython 3
#     Friedhold Matz 2020-sept
# -------------------------------------------------
import base64
import cx_Oracle
from cefpython3 import cefpython as cef

def chk_ora_connect():
    try:
        conn = cx_Oracle.connect('<uname>/<password>@<db-SID',
                                 encoding="UTF-8", nencoding="UTF-8")
        cursor = conn.cursor()
        for row in cursor.execute("select to_char(sysdate, 'YYYY-MM-DD HH24:MI:SS') from dual"):
            res_ = 'Successful ! '+ row[0]
    except Exception as e:
        res_ = '`$$$ Error db.connet() : {}'.format(e)+'`'
    return res_

def html_to_data_uri(html, js_callback=None):
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    return ret

def chk_oracef3():
    html_ = '<!DOCTYPE html>  ' \
            '<html lang="en">  ' \
            '<head>  ' \
            '<title>Bootstrap 4 Blog Template For Developers</title>  ' \
            '</head>  ' \
            '<body>  ' \
            '<h2> Oracle cx_Oracle test: {res} </h2>  ' \
            '</body>  ' \
            '</html>  '

    settings = {
        # "product_version": "MyProduct/10.00",
        # "user_agent": "MyAgent/20.00 MyProduct/10.00",
    }
    cef.Initialize(settings=settings)

    x = html_.replace('{res}', chk_ora_connect())
    browser = cef.CreateBrowserSync(url=html_to_data_uri(x),
                                    window_title="Checks Oracle ATP connection."
                                   )
    cef.MessageLoop()
    cef.Shutdown()
    return

if __name__ == '__main__':
    chk_oracef3()
