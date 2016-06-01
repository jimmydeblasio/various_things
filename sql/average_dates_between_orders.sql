SELECT DATEDIFF(MAX(date), MIN(date)) / (COUNT(date) - 1) FROM orders_supplies
where product_name = 'PF Chm 104a 55gl Inserts Wash';