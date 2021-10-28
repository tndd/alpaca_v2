select `time` from bars
where timeframe = %s and symbol = %s
order by `time` desc
limit 1;
