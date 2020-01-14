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
		if self.fetch_all == 0 and self.department != 'All Departments':
			if(self.employee):
				employee_doc = frappe.get_doc('Employee',self.employee)
			else:	# Validating Employee Value
				frappe.throw('Please select employee')
			# Setting Database Parameters
			anviz = frappe.get_single('Anviz Setting')
			server = str(anviz.server)
			user = str(anviz.user)
			password = str(anviz.password)
			port = str(anviz.port)
			database = str(anviz.database)
			# Connecting to Database
			conn = pymssql.connect(server, user, password, database,port=port)
			cursor = conn.cursor()
			# Running SQL query 
			cursor.execute(
				'''SELECT TOP 100000 [logid],[Userid],[CheckTime],[CheckType] \
								FROM dbo.Checkinout \
								WHERE Userid = {0} AND CheckTime >= '{1} 00:00:00.000' AND CheckTime <= '{2} 23:59:59.000' \
								ORDER BY CheckTime ASC'''.format(self.attendance_device_id,self.from_date,self.to_date)
			)
			row = cursor.fetchall()
			last_date = None
			# Looping through query results
			for att in row:
				row_date = parse_date(att[2])
				row_time = parse_time(att[2])
				# For Entry
				if row_date!=last_date:
					attendance_list = frappe.get_list('Attendance',filters= {'attendance_date':row_date,'attendance_device_id':self.attendance_device_id})
					if not attendance_list:
						# Creating new attendance doc
						new_att = frappe.new_doc('Attendance')
						new_att.update({
							'employee':self.employee,
							'attendance_device_id': self.attendance_device_id,
							'attendance_date': row_date,
							'status': 'Present',
							'in_time': row_time,
							'out_time': '',
							'shift': employee_doc.default_shift
						})
						new_att.save()
						new_att.submit()
				# For Exit
				elif row_date==last_date:
					attendance_list = frappe.get_list('Attendance',filters= {'attendance_date':row_date,'attendance_device_id':self.attendance_device_id})
					if attendance_list:
						#  Updating already created attendance doc
						frappe.db.set_value('Attendance',attendance_list[0].name,'out_time',row_time)
				last_date = row_date
			conn.close()
		else:
			if self.department:
				employee_list = None
				# Getting active employee list
				if self.department == 'All Departments':
					employee_list = frappe.get_list('Employee',filters= {'status':'Active'},page_length= 100000)
				else:	
					employee_list = frappe.get_list('Employee',filters= {'status':'Active','department':self.department},page_length= 100000)
				# Setting database parameters
				anviz = frappe.get_single('Anviz Setting')							
				server = str(anviz.server)
				user = str(anviz.user)
				password = str(anviz.password)
				port = str(anviz.port)
				database = str(anviz.database)
				for employee in employee_list:
					employee_doc = frappe.get_doc('Employee',employee.name)					# Getting employee doc
					conn = pymssql.connect(server, user, password, database,port=port)	# Connecting to Database
					cursor = conn.cursor()
					# Executing SQL query
					cursor.execute(
						'''SELECT TOP 100000 [logid],[Userid],[CheckTime],[CheckType] \
										FROM dbo.Checkinout \
										WHERE Userid = {0} AND CheckTime >= '{1} 00:00:00.000' AND CheckTime <= '{2} 23:59:59.000' \
										ORDER BY CheckTime ASC'''.format(employee_doc.attendance_device_id,self.from_date,self.to_date)
					)
					row = cursor.fetchall()
					last_date = None
					# Looping throw the query results
					for att in row:
						row_date = parse_date(att[2])
						row_time = parse_time(att[2])
						# For Entry
						if row_date!=last_date:
							attendance_list = frappe.get_list('Attendance',filters= {'attendance_date':row_date,'attendance_device_id':employee_doc.attendance_device_id})
							if not attendance_list:
								# Creating new attendance doc
								new_att = frappe.new_doc('Attendance')
								new_att.update({
									'employee':employee_doc.name,
									'attendance_device_id': employee_doc.attendance_device_id,
									'attendance_date': row_date,
									'status': 'Present',
									'in_time': row_time,
									'out_time': '',
									'shift': employee_doc.default_shift
								})
								new_att.save()
								new_att.submit()
						# For Exit
						elif row_date==last_date:
							attendance_list = frappe.get_list('Attendance',filters= {'attendance_date':row_date,'attendance_device_id':employee_doc.attendance_device_id})
							# Updating already created attendance doc
							if attendance_list:
								frappe.db.set_value('Attendance',attendance_list[0].name,'out_time',row_time)
						last_date = row_date
					conn.close()

# Function for Date
def parse_date(datetime):
	datetime = str(datetime)
	date = datetime[:10]
	return date
# Function for Time
def parse_time(datetime):
	datetime = str(datetime)
	time = datetime[11:]
	return time

# Methods to be called from JS	
@frappe.whitelist()
def get_employee_details(employee):
	employee_doc = frappe.get_doc('Employee',employee)
	return {'employee_name':employee_doc.employee_name,'attendance_device_id':employee_doc.attendance_device_id}