select product_name, 
round(y.plates_purchased,2) as 'boxes per week (3Q2014)',
round(z.plates_purchased,2) as 'boxes per week (4Q2015)',
round(x.plates_purchased,2) as 'boxes per week (1Q2015)', 
round(y.plates_purchased*50,2) as 'plates per week (3Q2014)', 
round(z.plates_purchased*50,2) as 'boxes per week (4Q2015)',
round(x.plates_purchased*50,2) as 'plates per week (1Q2015)'
from orders_supplies 
left join 
(select product_name as 'pn', sum(units_purchased)/13 as 'plates_purchased' from orders_supplies os
where year(date) = 2015
and quarter(date) = 1 
group by product_name) x on (x.pn = orders_supplies.product_name)
left join 
(select product_name as 'pn', sum(units_purchased)/13 as 'plates_purchased' from orders_supplies os
where year(date) = 2014
and quarter(date) = 3
group by product_name) y on (y.pn = orders_supplies.product_name)
left join
(select product_name as 'pn', sum(units_purchased)/13 as 'plates_purchased' from orders_supplies os
where year(date) = 2014
and quarter(date) = 4
group by product_name) z on (z.pn = orders_supplies.product_name)
where product_id in (1,2,3)
group by product_name
