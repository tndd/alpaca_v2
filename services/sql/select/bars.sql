select
    `timeframe`,
    `symbol`,
    `time`,
    `open`,
    `high`,
    `low`,
    `close`,
    `volume`
from bars
where symbol = %s
    and timeframe = %s
;
