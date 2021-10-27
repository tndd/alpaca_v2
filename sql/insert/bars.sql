INSERT IGNORE INTO bars (`timeframe`, `symbol`, `time`, `open`, `high`, `low`, `close`, `volume`)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
