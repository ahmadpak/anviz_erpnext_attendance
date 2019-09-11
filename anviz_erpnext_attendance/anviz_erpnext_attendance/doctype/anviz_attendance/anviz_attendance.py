# -*- coding: utf-8 -*-
# Copyright (c) 2019, Havenir and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import pymssql
from frappe.model.document import Document
from frappe.utils import flt, get_datetime,today,add_days, add_to_date, date_diff, format_datetime, time_diff, time_diff_in_seconds

class AnvizAttendance(Document):
	def validate(self):
		if not self.department:
			frappe.throw('Please enter the department!')

	def on_submit(self):
		self.generate_attendance()
	
	def generate_attendance(self):
		employee_doc = frappe.get_doc('Employee',self.employee)
		if self.fetch_all == 0:
			anviz = frappe.get_single('Anviz Setting')
			server = str(anviz.server)
			user = str(anviz.user)
			password = str(anviz.password)
			port = str(anviz.port)
			database = str(anviz.database)
			conn = pymssql.connect(server, user, password, database,port=port)
			cursor = conn.cursor()
			cursor.execute(
				"SELECT TOP 100 [Logid],[Userid],[CheckTime],[CheckType],\
								[Sensorid],[WorkType],[AttFlag],[Checked],\
								[Exported],[OpenDoorFlag] \
								FROM dbo.Checkinout \
								WHERE Userid = {0} AND CheckTime >= '{1} 00:00:00.000' AND CheckTime <= '{2} 23:59:59.000' \
								ORDER BY CheckTime ASC".format(self.attendance_device_id,self.from_date,self.to_date)
			)
			row = cursor.fetchone()
			row_date = ''
			row_in_time = ''
			row_out_time = ''
			row_last_date = None
			while row:
				row_next_date = parse_date(row[2])
				if row_next_date!=row_date and row[3]==0:
					#if row_date != '':
						#frappe.msgprint('date: {0}, intime: {1}, outtime: {2}'.format(row_date,row_in_time,row_out_time))
					attendance_list = frappe.get_list('Attendance',filters= {'attendance_date':row_next_date},fields = '*')
					if not attendance_list:
						new_att = frappe.new_doc('Attendance')
						new_att.update({
							'employee':self.employee,
							'attendance_device_id': self.attendance_device_id,
							'attendance_date': row_next_date,
							'status': 'Present',
							'shift': employee_doc.default_shift
						})
						new_att.save()
						new_att.submit()
					
					row_in_time = parse_time(row[2])
					row_date = row_next_date
					row_out_time = ''
				elif row_next_date==row_date and row[3]==1:
					row_out_time = parse_time(row[2])

				row = cursor.fetchone()

			conn.close()
		else:
			frappe.throw('fetch all')

def parse_date(datetime):
	datetime = str(datetime)
	date = datetime[:10]
	return date

def parse_time(datetime):
	datetime = str(datetime)
	time = datetime[11:]
	return time
@frappe.whitelist()
def get_employee_details(employee):
	employee_doc = frappe.get_doc('Employee',employee)
	return {'employee_name':employee_doc.employee_name,'attendance_device_id':employee_doc.attendance_device_id}