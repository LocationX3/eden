# -*- coding: utf-8 -*-

try:
    # Python 2.7
    from collections import OrderedDict
except:
    # Python 2.6
    from gluon.contrib.simplejson.ordered_dict import OrderedDict

from gluon import current, URL
from gluon.storage import Storage
from gluon.validators import IS_IN_SET
from gluon.html import *

from s3 import *

def config(settings):
    """
        Template settings for Services Locator
    """

    T = current.T

    # Pre-Populate
    settings.base.prepopulate = ("default", "default/users")

    # Theme
    settings.base.theme = "ServicesLocator"
    settings.ui.formstyle_row = "bootstrap"
    settings.ui.formstyle = "bootstrap"
    settings.ui.filter_formstyle = "table_inline"

    # Uncomment to disable responsive behavior of datatables
    # - Disabled until tested
    settings.ui.datatables_responsive = False

    # Message
    settings.msg.notify_email_format = "text"

    # Should users be allowed to register themselves?
    settings.security.self_registration = True
    settings.auth.registration_requires_verification = True
    settings.auth.registration_requires_approval = False

    # Uncomment this to set the opt in default to True
    #settings.auth.opt_in_default = True
    # Uncomment this to default the Organisation during registration
    settings.auth.registration_organisation_default = "Code for Seattle"

    # Always notify the approver of a new (verified) user, even if the user is automatically approved
    settings.auth.always_notify_approver = False

    # Base settings
    settings.base.system_name = T("Gimme Shelter")
    settings.base.system_name_short = T("Gimme Shelter")

    # L10n settings
    settings.L10n.languages = OrderedDict([
       ("ar", "العربية"),
       ("bs", "Bosanski"),
       ("en", "English"),
       ("fr", "Français"),
       ("de", "Deutsch"),
       ("el", "ελληνικά"),
       ("es", "Español"),
       ("it", "Italiano"),
       ("ja", "日本語"),
       ("km", "ភាសាខ្មែរ"),
       ("ko", "한국어"),
       ("ne", "नेपाली"),          # Nepali
       ("prs", "دری"), # Dari
       ("ps", "پښتو"), # Pashto
       ("pt", "Português"),
       ("pt-br", "Português (Brasil)"),
       ("ru", "русский"),
       ("tet", "Tetum"),
       ("tl", "Tagalog"),
       ("ur", "اردو"),
       ("vi", "Tiếng Việt"),
       ("zh-cn", "中文 (简体)"),
       ("zh-tw", "中文 (繁體)"),
    ])
    # Default language for Language Toolbar (& GIS Locations in future)
    settings.L10n.default_language = "en"
    # Display the language toolbar
    settings.L10n.display_toolbar = True
    # Default timezone for users
    settings.L10n.utc_offset = "UTC +0000"
    # Default timezone for users
    settings.L10n.utc_offset = "UTC +0000"

    # @ToDo: Move into gis_config?
    settings.gis.display_L0 = False
    # Duplicate Features so that they show wrapped across the Date Line?
    # Points only for now
    # lon<0 have a duplicate at lon+360
    # lon>0 have a duplicate at lon-360
    settings.gis.duplicate_features = False
    # Mouse Position: 'normal', 'mgrs' or 'off'
    settings.gis.mouse_position = "normal"
    # Do we have a spatial DB available? (currently unused. Will support PostGIS & Spatialite.)
    settings.gis.spatialdb = False

    # Use 'soft' deletes
    settings.security.archive_not_delete = True

    # AAA Settings

    # Security Policy
    # http://eden.sahanafoundation.org/wiki/S3AAA#System-widePolicy
    # 1: Simple (default): Global as Reader, Authenticated as Editor
    # 2: Editor role required for Update/Delete, unless record owned by session
    # 3: Apply Controller ACLs
    # 4: Apply both Controller & Function ACLs
    # 5: Apply Controller, Function & Table ACLs
    # 6: Apply Controller, Function, Table & Organisation ACLs
    # 7: Apply Controller, Function, Table, Organisation & Facility ACLs

    settings.security.policy = 3

    # Human Resource Management
    # Uncomment to hide the Staff resource
    settings.hrm.show_staff = False

    # Enable the use of Organisation Branches
    settings.org.branches = False

    # Project
    # Uncomment this to use emergency contacts in pr
    settings.pr.show_emergency_contacts = False

    # -----------------------------------------------------------------------------
    # Comment/uncomment modules here to disable/enable them
    settings.modules = OrderedDict([
        # Core modules which shouldn't be disabled
        ("default", Storage(
                name_nice = T("Home"),
                restricted = False, # Use ACLs to control access to this module
                access = None,      # All Users (inc Anonymous) can see this module in the default menu & access the controller
                module_type = None  # This item is not shown in the menu
            )),
        ("admin", Storage(
                name_nice = T("Administration"),
                #description = T("Site Administration"),
                restricted = True,
                access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
                module_type = None  # This item is handled separately for the menu
            )),
        ("appadmin", Storage(
                name_nice = T("Administration"),
                #description = T("Site Administration"),
                restricted = True,
                module_type = None  # No Menu
            )),
        ("errors", Storage(
                name_nice = T("Ticket Viewer"),
                #description = T("Needed for Breadcrumbs"),
                restricted = False,
                module_type = None  # No Menu
            )),
        ("sync", Storage(
                name_nice = T("Synchronization"),
                #description = T("Synchronization"),
                restricted = True,
                access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
                module_type = None  # This item is handled separately for the menu
            )),
        ("gis", Storage(
                name_nice = T("Map"),
                #description = T("Situation Awareness & Geospatial Analysis"),
                restricted = True,
                module_type = 6,     # 6th item in the menu
            )),
        ("pr", Storage(
                name_nice = T("People"),
                #description = T("People"),
                restricted = True,
                module_type = None
            )),
        ("org", Storage(
                name_nice = T("Organizations"),
                #description = T('Lists "who is doing what & where". Allows relief agencies to coordinate their activities'),
                restricted = True,
                module_type = 2
            )),
        ("cr", Storage(
               name_nice = T("Shelters"),
               #description = "Tracks the location, capacity and breakdown of victims in Shelters",
               restricted = True,
               module_type = 2
            )),
        ("hms", Storage(
               name_nice = T("Medical Facilities"),
               #description = "Helps to monitor status of hospitals",
               restricted = True,
               module_type = 2
            )),
        ("doc", Storage(
                name_nice = T("Documents"),
                #description = T("A library of digital resources, such as photos, documents and reports"),
                restricted = True,
                module_type = None,
            )),
        ("msg", Storage(
                name_nice = T("Messaging"),
                #description = T("Sends & Receives Alerts via Email & SMS"),
                restricted = True,
                # The user-visible functionality of this module isn't normally required. Rather it's main purpose is to be accessed from other modules.
                module_type = None,
            )),
    ])

# END =========================================================================
