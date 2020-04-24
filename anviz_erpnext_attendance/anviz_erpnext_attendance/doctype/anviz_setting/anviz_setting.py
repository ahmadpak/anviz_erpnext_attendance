# -*- coding: utf-8 -*-
# Copyright (c) 2019, Havenir and contributors
# For license information, please see license.txt
# TODO Migrate code to use pyodbc instead of pymssql
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, get_datetime,today,add_days, add_to_date, date_diff, format_datetime, time_diff, time_diff_in_seconds
import pymssql


class AnvizSetting(Document):
    def validate(self):
        self.get_employees()

    def get_employees(self):
        # Setting Database Parameters
        server = str(self.server)
        user = str(self.user)
        password = str(self.password)
        port = str(self.port)
        database = str(self.database)

        # Connecting to Database
        conn = pymssql.connect(server, user, password, database, port=port)
        cursor = conn.cursor()

        # Running SQL query
        cursor.execute(
            '''SELECT TOP 100000 [Userid],[UserCode],[Name],[Sex],[Telephone] \
                FROM dbo.Userinfo \
                ORDER BY Userid'''
        )

        # Saving result from the query
        row = cursor.fetchall()

        # Looping through query results
        for user in row:
            employee = frappe.get_list("Employee",
                                       filters={
                                           'attendance_device_id': str(user[0])
                                       })
            if employee:
                pass
            else:
                new_employee = frappe.new_doc('Employee')
                new_employee.first_name = str(user[2])
                new_employee.gender = str(user[3])
                new_employee.date_of_birth = add_days(today(),-1)
                new_employee.date_of_joining = today()
                new_employee.cell_number = str(user[4])
                new_employee.attendance_device_id = str(user[0])
                new_employee.save()
                frappe.msgprint("Userid: {0} | Name: {1} Created".format(user[0], user[2]))
