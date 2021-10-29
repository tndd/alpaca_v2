select `symbol`, max(time) as 'latest_time' from bars
where timeframe = %s
group by symbol;
