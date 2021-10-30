CREATE TABLE IF NOT EXISTS `bars` (
    `timeframe` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    `symbol` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    `time` datetime NOT NULL,
    `open` double NOT NULL,
    `high` double NOT NULL,
    `low` double NOT NULL,
    `close` double NOT NULL,
    `volume` int unsigned NOT NULL,
    PRIMARY KEY (`timeframe`,`symbol`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
