SELECT x.job_id, 
x.price,
x.job_no,
x.plate_costs,
Round(z.total_ink_costs,2) as total_ink_costs, 
IFNULL(Round(y.paper_cost,2),0) as paper_cost, 
Round(convert(x.price,unsigned integer)-x.plate_costs-ifnull(y.paper_cost,100)-ifnull(z.total_ink_costs,0),2) as total from 
(select *,
case 
when press = 1 then (convert(Num_Plates, unsigned integer)*3.93)
when press = 2 then (convert(Num_Plates, unsigned integer)*3.98)
when press = 3 then (convert(Num_Plates, unsigned integer)*4.35)
end as 'plate_costs'
from tbl_projects_job 
where press in (1,2,3) 
order by job_id desc) x
left JOIN 
(select *, 
case 
when paper_orders.department_id = 2 then (sum(paper_orders.price)/100)*paper_orders.no_of_sheets_pounds
when paper_orders.department_id = 3 then sum(paper_orders.price)*(paper_orders.no_of_sheets_pounds/1000)
end as 'paper_cost' 
from paper_orders 
group by job_no
) y
ON 
(y.job_no = x.Job_no)
left JOIN
(select *,
case 
when press in (1,2) then (jc.k*1.38)+(jc.b*1.83)+(jc.r*2.02)+(jc.y*1.65)
when press = 3 then ((17.65/5)*jc.k)+((20.35/5)*jc.b)+((21.15/5)*jc.r)+((20.25/5)*jc.y)
end as total_ink_costs
from offset_job_costs jc
) z
on (x.job_no = z.job_no)