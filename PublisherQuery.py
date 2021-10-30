class PublisherQuery:
    @staticmethod
    def _load_query_from_file(path: str) -> str:
        try:
            with open(path, 'r') as f:
                query = f.read()
        except IOError as e:
            print(e)
        return query

    @classmethod
    def create_bars(cls) -> str:
        path = './sql/create/bars.sql'
        return cls._load_query_from_file(path)

    @classmethod
    def insert_bars(cls) -> str:
        path = './sql/insert/bars.sql'
        return cls._load_query_from_file(path)

    @classmethod
    def select_bars_latest_time(cls) -> str:
        path = './sql/select/bars_latest_time.sql'
        return cls._load_query_from_file(path)
