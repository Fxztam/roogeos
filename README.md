RoOgeoS - Ring of Oracle GeoJSON Service.

# Introduction

The cooperation of modern, heterogeneous software systems can be achieved by interoperability of transparent data formats with standardized services. 
The GeoJSON data format for the exchange of geometry and attribute data has proven to be very assertive due to its transparency and efficiency. 

The following is a demonstration of the interoperability by low code and transparency in the data process, spatial data quality assurance, and service delivery.  
Every data processing begins with validation that means the quality assurance of the data, 
here the efficiency of Oracle Spatial should also be proven with the possibility of automatic data correction.

True to the definition of Geographical Information Systems (GIS)::

#### Input - Management - Analysis - Presentation  (I M A P principle)

is the following workflow with simple Python scripting as batch processing implemented:

1. GeoJSON File - Storage in the Feature Table (Input)
1. Validation and Indexing (Management / Analyzing)
1. GeoJSON RESTful Data Service & Map viewing (Viewing) .

I developed and checked the whole process on my _Always Free Oracle Autonomous Transaction Processing (ATP) Cloud Database_ in Frankfurt.

<img src="http://www.fmatz.com/Ring-Schema.png">

### Thank you Oracle for providing these awesome technologies - it gave me a lot of pleasure!


# Preferences

- Windows 10
- Oracle Autonomous Transaction Processing Cloud Database (also Always Free)
- Python 3.79 (not 3.8)
- Oracle Cx_Oracle
- Chromium Embedded Framework for Python3 cefpython3

# Installation

This 
## Configure Client Side for Oracle Autonomous Transaction Database

## Install Python 3.7

1. Download [Python 3.79, the latest security fix - Release Date: Aug. 17, 2020](https://www.python.org/downloads/release/python-379/) 
1. Install it in C:\Python37
2. Copy and rename the .\bin\python.exe to python37.exe
3. In the Windows System Environement `Set PATH=C:\Python37\bin;%PATH%`
4. Test the Python37 call:
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
   
## Install cefpython3

   ```dos
   dos> python37 -m pip install cefpython3
   
   ```
   
# Quick Starts

# Presentation - Video

# Modul Description

# Known Issues

# Development Agenda

on) .

<iframe width="560" height="315"
src="https://www.youtube.com/embed/MUQfKFzIOeU"
frameborder="0"
allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
allowfullscreen></iframe>
<iframe src="https://player.vimeo.com/video/167121552" width="700" height="400" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
