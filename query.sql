select a.plyr_name, a.p_score, b.avg_score 
from (select plyr_name,p_score from pga.score_prediction where p_score > 0 order by p_score limit 40) a 
join (select plyr_name, avg(finposnum) as avg_score from pga.tournsum where t_id = '490' and year > 2013 and finposnum<999 group by 1 having count(*)=2) b 
on a.plyr_name = b.plyr_name order by 3;

