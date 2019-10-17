// Copyright (c) 2019, Havenir and contributors
// For license information, please see license.txt

frappe.ui.form.on('Anviz Attendance', {
	onload: function(frm){
		var doc = cur_frm.doc;
		var todays_date = frappe.datetime.get_today();
		var new_date = frappe.datetime.add_days(todays_date,-1);
		if (doc.__islocal){
			doc.from_date = new_date;
			doc.to_date = new_date;
			cur_frm.refresh_field('from_date');
			cur_frm.refresh_field('to_date');
		}
	},
	 department: function(frm) {
		frm.set_query('employee',function(){
			return{
				filters: {
					'department': cur_frm.doc.department
				}
			};
		});
	 },
	 employee: function(frm){
		 var doc = cur_frm.doc;
		 frm.call({
			 method: 'anviz_erpnext_attendance.anviz_erpnext_attendance.doctype.anviz_attendance.anviz_attendance.get_employee_details',
			 args: {
				 employee:doc.employee
			 },
			 callback: function(r){
				 doc.employee_name = r.message.employee_name;
				 doc.attendance_device_id = r.message.attendance_device_id;
				 cur_frm.refresh_field('employee_name');
				 cur_frm.refresh_field('attendance_device_id');
				 
			 }
		 });
	 },
	 from_date: function(frm){
		 var doc = cur_frm.doc;
		 var dif_in_days = frappe.datetime.get_day_diff(doc.to_date,doc.from_date);
		 if (dif_in_days<0){
			 doc.from_date = doc.to_date;
			 cur_frm.refresh_field('from_date');
			 frappe.msgprint('From Date cannot be after To Date');
		 }
	 },
	 to_date: function(frm){
		 var doc = cur_frm.doc;
		 var todays_date = frappe.datetime.get_today();
		 var new_date = frappe.datetime.add_days(todays_date,-1);
		 var dif_in_days = frappe.datetime.get_day_diff(doc.to_date,doc.from_date);
		 var not_today = frappe.datetime.get_day_diff(frappe.datetime.get_today(),doc.to_date);
		 if (not_today<=0 ){
			 doc.to_date = new_date;
			 cur_frm.refresh_field('to_date');
			 frappe.msgprint('To Date cannot be set as todays or later date');
		 }
		 if (dif_in_days<0){
			 doc.to_date = doc.from_date;
			 cur_frm.refresh_field('to_date');
			 frappe.msgprint('To Date cannot be before From Date');
		 }
	 }
});
