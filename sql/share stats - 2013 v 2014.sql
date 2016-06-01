select tbl_tags.tag_name,
x.precount as 'no. of articles (2014)', 
round(x.pre_views,2) as 'views/article (2014)', 
round(x.pre_shares,2) as 'shares/article (2014)',
y.post as 'no. of articles (2013)', 
round(y.post_views,2) as 'view/articles(2013)',
round(y.post_shares,2) as 'shares/article (2013)'
from tbl_tags
left join
(select tags.tag_id as 'hello', 
count(tags.tag_id) as 'precount', 
sum(articles.views)/count(tags.tag_id) as 'pre_views', 
sum(articles.total_share_count)/count(tags.tag_id) as 'pre_shares' 
from tbl_page_assets articles
Inner JOIN tbl_page_assets_tags tags ON articles.pa_id = tags.pa_id
where year(articles.pa_live_date) = 2014
group by tags.tag_id) x
on (x.hello = tbl_tags.tag_id)
left join
(select tags.tag_id as 'again', 
count(tags.tag_id) as 'post', 
sum(articles.views)/count(tags.tag_id) as 'post_views', 
sum(articles.total_share_count)/count(tags.tag_id) as 'post_shares'
from tbl_page_assets articles
Inner JOIN tbl_page_assets_tags tags ON articles.pa_id = tags.pa_id
where year(articles.pa_live_date) = 2013
group by tags.tag_id) y
on (y.again = tbl_tags.tag_id) 
where tbl_tags.tag_type = 'university'
and (x.precount or y.post) is not null
order by tbl_tags.tag_name