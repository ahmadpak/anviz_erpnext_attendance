# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "anviz_erpnext_attendance"
app_title = "Anviz Erpnext Attendance"
app_publisher = "Havenir"
app_description = "Connects with anviz sql database and pulls attendance according to the status 0 for IN 1 for Out 2 for Break"
app_icon = "octicon octicon-desktop-download"
app_color = "grey"
app_email = "info@havenir.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/anviz_erpnext_attendance/css/anviz_erpnext_attendance.css"
# app_include_js = "/assets/anviz_erpnext_attendance/js/anviz_erpnext_attendance.js"

# include js, css files in header of web template
# web_include_css = "/assets/anviz_erpnext_attendance/css/anviz_erpnext_attendance.css"
# web_include_js = "/assets/anviz_erpnext_attendance/js/anviz_erpnext_attendance.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_js = {
    'Attendance': [
        'utils/attendance.js'
        ]
}

fixtures = [{
    'dt': 'Custom Field', 'filters': [
        [
            'name','in',[
                'Attendance-attendance_device_id',
                'Attendance-in_time',
                'Attendance-out_time'
            ]
        ]
    ]
}]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "anviz_erpnext_attendance.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "anviz_erpnext_attendance.install.before_install"
# after_install = "anviz_erpnext_attendance.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "anviz_erpnext_attendance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"anviz_erpnext_attendance.tasks.all"
# 	],
# 	"daily": [
# 		"anviz_erpnext_attendance.tasks.daily"
# 	],
# 	"hourly": [
# 		"anviz_erpnext_attendance.tasks.hourly"
# 	],
# 	"weekly": [
# 		"anviz_erpnext_attendance.tasks.weekly"
# 	]
# 	"monthly": [
# 		"anviz_erpnext_attendance.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "anviz_erpnext_attendance.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "anviz_erpnext_attendance.event.get_events"
# }

