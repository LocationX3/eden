# -*- coding: utf-8 -*-

try:
    import json # try stdlib (Python 2.6)
except ImportError:
    try:
        import simplejson as json # try external module
    except:
        import gluon.contrib.simplejson as json # fallback to pure-Python module

from os import path

from gluon import current, URL
from gluon.html import *
from gluon.storage import Storage
from gluon.sqlhtml import SQLFORM

from s3 import S3FilterForm, S3CustomController, S3OptionsFilter, S3Request, \
               S3SQLCustomForm

THEME = "ServicesLocator"

# =============================================================================
class index(S3CustomController):
    """ Custom Home Page """

    def __call__(self):

        response = current.response
        settings = current.deployment_settings
        request = current.request
        s3 = response.s3
        db = current.db
        s3db = current.s3db
        T = current.T

        output = {}
        output["title"] = response.title = current.deployment_settings.get_system_name()

        view = path.join(current.request.folder, "modules", "templates",
                         THEME, "views", "index.html")
        try:
            # Pass view as file not str to work in compiled mode
            response.view = open(view, "rb")
        except IOError:
            from gluon.http import HTTP
            raise HTTP(404, "Unable to open Custom View: %s" % view)

        shelter_url = URL(c="cr", f="shelter", extension="geojson")
        org_url = URL(c="org", f="organisation", extension="geojson")
        hospital_url = URL(c="hms", f="hospital", extension="geojson")

        mtable = s3db.gis_marker
        query = (mtable.name == "shelter") | (mtable.name == "office") | (mtable.name == "hospital")

        markers = db(query).select(mtable.name,
                                   mtable.image,
                                   mtable.height,
                                   mtable.width,
                                   cache=s3db.cache,
                                   limitby=(0, 3)
                                   )

        shelter_marker = None
        org_marker = None
        hospital_marker = None
        for marker in markers:
            if marker.name == "shelter":
                shelter_marker = marker
            if marker.name == "office":
                org_marker = marker
            if marker.name == "hospital":
                hospital_marker = marker

        layers = [{"name"      : T("Organizations"),
                   "id"        : "organisations",
                   "tablename" : "org_organisation",
                   "url"       : org_url,
                   "active"    : True,
                   "marker"    : org_marker,
                   },
                  {"name"      : T("Shelters"),
                   "id"        : "shelters",
                   "tablename" : "cr_shelter",
                   "url"       : shelter_url,
                   "active"    : True,
                   "marker"    : shelter_marker,
                   },
                  {"name"      : T("Clinics"),
                   "id"        : "hospitals",
                   "tablename" : "hms_hospital",
                   "url"       : hospital_url,
                   "active"    : True,
                   "marker"    : hospital_marker,
                   },
                  ]

        output["map"] = current.gis.show_map(collapsed = True,
                                             feature_resources = layers,
                                             legend="float",
                                             )

        return output

# =============================================================================
