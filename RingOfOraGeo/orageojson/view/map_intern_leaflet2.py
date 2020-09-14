#-------------------------------------------------
#  LeafLet 0.6 Mapping : CEFPYTHON3
#  Friedhold Matz - 2020-aug
#-------------------------------------------------

from string import Template

from cefpython3 import cefpython as cef
import base64
from orageojson.log.flogger import flog
from orageojson.log.flogger import loginfo

# Leaflet embedded into CEFpython3
from orageojson.view.get_leaflet06_css import get_css
from orageojson.view.get_leaflet06_js import get_js

# pre-defined for test with landkreis.geojson

m_url = None

m_props = None

def get_script4end(p_url, p_props):

    t =Template('<BODY> \n' \
                 '<div id="map"></div> \n' \
                 '<!-- Friedhold Matz - 2020-aug --> \n' \
                 '<script> \n' \
                 '    var ORDS_uri = \'${l_uri}\' \n' \
                 '    async function getORDSdata() { \n' \
                 '       // --- get ORDS JSON data from my AlwaysFree OracleCloud ATP --- \n' \
                 '       let response; \n' \
                 '       let vanillaGeoJSON; \n' \
                 '       try { \n' \
                 '           response = await fetch(ORDS_uri); // <<< OracleCloud ORDS <<< \n' \
                 '           console.info(response)  \n' \
                 '       } catch (e) { \n' \
                 '          console.error(`??? Error(fetch): ` + e) \n' \
                 '       } \n' \
                 '       if (response.ok) { \n' \
                 '          console.info("--- BO DATA OK.") \n' \
                 '          try {  \n' \
                 '             vanillaGeoJSON = await response.json() // parse JSON  \n' \
                 '          } catch (e) {  \n' \
                 '             console.error("??? Error(parse): " + e)  \n' \
                 '          }  \n' \
                 '        }  \n' \
                 '        // --- get from ORDS vanilla GeoJSON ---  \n' \
                 '        return vanillaGeoJSON;  \n' \
                 '    }  \n' \
                 '    // -- BO define leaflet base map -------  \n' \
                 '    // -- 51.5708975, 14.37940836], // BB Control Point in Spremberg  \n' \
                 '    bounds = new L.LatLngBounds(new L.LatLng(51.5708975, 14.37940836), new L.LatLng(52, 14));  \n' \
                 '    var map = L.map("map", {  \n' \
                 '        center: bounds.getCenter(),  \n' \
                 '        zoom: 12,  \n' \
                 '        scrollWheelZoom: "center", // zoom to center regardless where mouse is  \n' \
                 '        doubleClickZoom: "center"  \n' \
                 '    });  \n' \
                 '    L.tileLayer("http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png", {  \n' \
                 '       maxZoom: 18,  \n' \
                 '       attribution: `<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>` \n' \
                 '    }).addTo(map);  \n' \
                 '    // -- EO define leaflet base map ------  \n' \
                 '    //bounds = new L.LatLngBounds(new L.LatLng(49.5, -11.3), new L.LatLng(61.2, 2.5));  \n' \
                 '    // -- BO define geoJSON vector layer --  \n' \
                 '    let centerBounds  \n' \
                 '    (async function() {  \n' \
                 '        const geoJSON = await getORDSdata(); \n' \
                 '        console.info(geoJSON)  \n' \
                 '        let centerBounds \n' \
                 '        L.geoJSON(geoJSON, {  \n' \
                 '           style: {  \n' \
                 '               color: "green",  \n' \
                 '               weight: 3,  \n' \
                 '               opacity: 0.3,  \n' \
                 '               fillColor: "lightgreen",  \n' \
                 '               fillOpacity: 0.4,  \n' \
                 '           },  \n' \
                 '           onEachFeature: function (feature, layer) {  \n' \
                 '              let popupContent =  ${l_prop} \n' \
                 '              layer.bindPopup(popupContent) \n' \
                 '          if (centerBounds==null) {  \n' \
                 '             centerBounds = layer.getBounds() // init  \n' \
                 '          } else {  \n' \
                 '             _centerBounds = layer.getBounds()  \n' \
                 '          if (_centerBounds._northEast.lat > centerBounds._northEast.lat) {  \n' \
                 '             centerBounds._northEast.lat = _centerBounds._northEast.lat  \n' \
                 '          }  \n' \
                 '          if (_centerBounds._northEast.lng > centerBounds._northEast.lng) {  \n' \
                 '             centerBounds._northEast.lng = _centerBounds._northEast.lng  \n' \
                 '          }  \n' \
                 '          if (_centerBounds._southWest.lat < centerBounds._southWest.lat) {  \n' \
                 '             centerBounds._southWest.lat = _centerBounds._southWest.lat  \n' \
                 '          }  \n' \
                 '          if (_centerBounds._southWest.lng < centerBounds._southWest.lng) {  \n' \
                 '             centerBounds._southWest.lng = _centerBounds._southWest.lng }  \n' \
                 '          }  \n' \
                 '          // console.dir(centerBounds)  \n' \
                 '       }  \n' \
                 '       }).addTo(map);  \n' \
                 '      //console.log("Bounding Box: " + L.geoJSON.getBounds().toBBoxString());  \n' \
                 '      map.fitBounds(centerBounds)  \n' \
                 '    })()  \n' \
                 '    // -- EO define geoJSON vector layer --  \n' \
                 '    // -- Fine & Happy :-)))             --  \n' \
                 ' </script>  \n' \
                 ' </BODY>  \n' \
                 ' </HTML>')

    html_res = t.substitute(l_uri=p_url,
                            l_prop=p_props)

    return html_res

def get_HTML(p_url, p_props):
    return (''' <!DOCTYPE html> \
                <HTML> \
                <HEAD> \
            ''' + get_css() + get_js()
            + '''
                <STYLE> \
                    html, body { \
                        height: 100%; \
                    } \
                    #map { \
                        height: 100%; \
                        width: 100%; \
                        border: solid 1px black; \
                    } \
                </STYLE> \
                </HEAD> \
            '''
            + get_script4end(p_url, p_props))

def run_map(p_url, p_props):
    loginfo("--- BO - run_map() ---")
    settings = {
        # "product_version": "MyProduct/10.00",
        # "user_agent": "MyAgent/20.00 MyProduct/10.00",
    }
    cef.Initialize(settings=settings)

    flog(get_HTML(p_url, p_props), 'HTML', 'html') # => `./flog-HTML.html`

    browser = cef.CreateBrowserSync(url=html_to_data_uri(get_HTML(p_url, p_props)),
                                    window_title="GeoJSON in Oracle Spatial and GeoJSON Oracle RESTful Data Service for Mapping"
                                   )
    cef.MessageLoop()
    cef.Shutdown()
    loginfo("--- EO - run_map() ---")
    return

def html_to_data_uri(html, js_callback=None):
    html = html.encode("utf-8", "replace")
    b64 = base64.b64encode(html).decode("utf-8", "replace")
    ret = "data:text/html;base64,{data}".format(data=b64)
    return ret

class External(object):
    def __init__(self, browser):
        self.browser = browser

def map_intern_leaflet(p_url, p_props):
    m_url = p_url
    m_props = p_props
    run_map(p_url, p_props)
    return

if __name__ == '__main__':
    map_intern_leaflet(m_url, m_props)
