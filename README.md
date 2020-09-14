RoOgeoS - _** Ring of Oracle GeoJSON **_ Service

# Introduction

The cooperation of modern, heterogeneous software systems can be achieved by interoperability of transparent data formats with standardized services. The GeoJSON data format and RESTful data service for the exchange of geometry and attribute data has proven to be very assertive due to its transparency and efficiency. 

The following is a demonstration of the interoperability by low code and transparency in the data process true to the definition of Geographical Information Systems (GIS) by modern Oracle Database Components ::

> _Input - Management - Analysis - Presentation  (I M A P principle*(\*)*)_

Every data processing begins with validation that means the quality assurance of the data, 
here the efficiency of **Oracle Spatial** should also be proven with the possibility of automatic data correction.

So there is this workflow implemented:

1. GeoJSON File - Storage in the Feature Table (_Input_)
1. Validation and Indexing (_Management / Analyzing_)
1. GeoJSON RESTful Data Service & Map viewing (_Viewing_) 

with following **Oracle Database components ** are used:

- **Oracle cx_Oracle** : Python extension tool for accessing the Oracle Database
- **Oracle RESTful Data Service (ORDS)** : Fast data service for CRUD applications on Oracle Databases
- **Oracle JSON** : JSON data storage and functions in Oracle DB
- **Oracle Spatial** : Spatial Service for CRUD geo data storage and a lot of *IMAP(\*) services* in the Oracle DB 

I developed and checked the whole process on my _Always Free **Oracle Autonomous Transaction Processing** (ATP) **Cloud** Database_ in Frankfurt.

***Thank you Oracle for providing these awesome technologies on my Always  Free Oracle ATP :*** 

***It gives me a lot of pleasure !***

# Overview

This workflow is with simple Python 3 scripting as batch processing implemented:

<img src="http://www.fmatz.com/Ring-Schema3.png">

# Preferences

- Windows 10
- Oracle Autonomous Transaction Processing Cloud Database (also Always Free)
- Oracle Instant Client 19.x
- Python 3.79  (not 3.8 !)
- Oracle Cx_Oracle
- Chromium Embedded Framework for Python3 cefpython3

# Installation

## Install Oracle Instant Client

1. Download the Oracle Instant Client
2. Unzip it 
3. Set the System Environment PATH to the Oracle Instant Client directory .\bin

## Client Side Configuration

1. Download the Wallet.zip from your Oracle ATP DB
2. Copy it to e.g. C:\etc  
3. Unzip it there
4. Set in sqlnet.ora the C:\etc directory:![img](file:///C:/Users/Fried/AppData/Local/Temp/SNAGHTML288366.PNG)
5. In System Environement : `Set TNS_NAMES=C:\etc`

## Install Python 3.7

1. Download [Python 3.79, the latest security fix - Release Date: Aug. 17, 2020](https://www.python.org/downloads/release/python-379/) 

2. Install it in C:\Python37

3. Copy and rename the .\bin\python.exe to python37.exe

4. In the Windows System Environement `Set PATH=C:\Python37\bin;%PATH%`

5. Test the Python37 call:

   ```dos
   dos> python37
    Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
   >>>
   ```

## Install Oracle Cx_Oracle

1. Cx_Oracle installing with pip from Python37 ([Pip installing from Python37](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html))

   ```dos
   dos> python37 -m pip install cx_Oracle
   
   dos> python37
   ..
   >>>import cx_Oracle
   >>>cx_Oracle.version
   '8.0.1'
   >>> ^Z       #`exit with <CTRL><Z>`
   dos>
   ```

## Install CefPython3

   ```dos
   dos> python37 -m pip install cefpython3
   ```

## Test the Components

```python
#--------------------------------------------------
# --- Test the cx_Oracle connection and cefpython 3
#     Friedhold Matz 2020-sept
# -------------------------------------------------
import base64
import cx_Oracle
from cefpython3 import cefpython as cef

def chk_ora_connect():
    try:
        conn = cx_Oracle.connect('<uname>/<password>@<db-SID>',
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

```

- Copy the Python test file from [github](https://raw.githubusercontent.com/Fxztam/roogeos/master/chk_oracef3.py?token=ABMJ7IAF42ZMVGZUZBF2VHC7LNDIK)

- Set your <uname>/<password>@<db-SID> in ***chk_oracef3.py***

  ```
  cx_Oracle.connect('<uname>/<password>@<db-SID>', ..
  ```

- Execute it from file's directory:

```
dos> python37 chk_oracef3.py
```

<img src="http://www.fmatz.com/Cx_OOra-CEF-OK.png">

Congratulations, you can now enter the **_`Ring of Oracle GeoJSON Service`_** !

# Quick Start Demos

## Get your GeoJSON data from layer editing

[map layer editing directly](https://geojson.io/)

![image-20200913220828448](https://github.com/Fxztam/roogeos/image-20200913220828448.png)

## Get your GeoJSON data from OSM shape files

1. You can download Open Streetmap Data (OSM) from e.g. the [Geodatafabrik](https://download.geofabrik.de/) in Shape File format.

2. Install [QGIS 3.14]( https://qgis.org/en/site/forusers/download.html)

3. Open QGIS, <New Project> , <Add Layer> , <Add Vector Layer> => `Source Type` - `File`

4. Select the  *<OSM.shp>*  file

5. Navigate in Layers to your layer activation e.g. `osm buildings`: 

   ![image-20200913233741535](C:\Users\Fried\AppData\Roaming\Typora\typora-user-images\image-20200913233741535.png)

6. Select Features on your layer activation : 

   ![image-20200913234406127](C:\Users\Fried\AppData\Roaming\Typora\typora-user-images\image-20200913234406127.png)

7. On the new  `..selected x` you can <Right Mouse Click> , <Export> , <Save Feature As...> 

   ![image-20200913235527807](C:\Users\Fried\AppData\Roaming\Typora\typora-user-images\image-20200913235527807.png)

8. Fill out for the GeoJSON export:

   ![image-20200913235504881](C:\Users\Fried\AppData\Roaming\Typora\typora-user-images\image-20200913235504881.png)

   

9. Congratulations !  You have created your GeoJSON file for `Ring of Oracle GeoJSON` now !

# Modul Description

- c
- c
- c
- c
- c
- c
- c
- c
- 

# Known Issues

- Large datasets
- GeoJSON property names not table column syntax conform

