# Copyright (c) 2024, Sanskar and contributors
# For license information, please see license.txt


import frappe

def execute(filters=None):

    columns = [
        {'label': 'Project Name', 'fieldname': 'project', 'fieldtype': 'Data'},
        {'label': 'Client', 'fieldname': 'customer', 'fieldtype': 'Data'},
        {'label': 'Revenue/Expense', 'fieldname': 'R', 'fieldtype': 'Data'},
        {'label': 'Particulars', 'fieldname': 'item', 'fieldtype': 'Data'},
        {'label': 'Unit', 'fieldname': 'uom', 'fieldtype': 'Data'},
        {'label': 'Budgeted Qty', 'fieldname': 'qty', 'fieldtype': 'Float'},
        {'label': 'Budgeted Unit price', 'fieldname': 'rate', 'fieldtype': 'Currency'},
        {'label': 'Budgeted Amount', 'fieldname': 'amount', 'fieldtype': 'Currency'},
        {'label': 'Actual Qty', 'fieldname': 'pqty', 'fieldtype': 'Float'},
        {'label': 'Actual Unit price', 'fieldname': 'prate', 'fieldtype': 'Currency'},
        {'label': 'Actual Amount', 'fieldname': 'pamount', 'fieldtype': 'Currency'}
    ]
    sql = """
		SELECT 
			B.project,
			P.customer,
			BI.item,
			BI.qty,
			BI.rate,
			BI.amount,
			PII.uom,
			SUM(PII.qty) AS pqty,
			AVG(PII.rate) AS prate,
			SUM(PII.amount) AS pamount
		FROM `tabBudget` AS B
		JOIN `tabProject` AS P ON B.project = P.name
		JOIN `tabPurchase Invoice Item` AS PII ON PII.project = P.name
		JOIN `tabPurchase Invoice` AS PI ON PII.parent = PI.name AND PI.docstatus = 1
		JOIN `tabBudget Item Account` AS BI ON B.name = BI.parent AND BI.item = PII.item_code
		GROUP BY B.project, BI.item
		ORDER BY B.project, BI.item;
    """
    data = frappe.db.sql(sql, filters, as_dict=True)
    return columns, data
