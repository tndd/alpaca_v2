from enum import Enum

class Order(Enum):
    CREATE = 'create'
    SELECT = 'select'
    INSERT = 'insert'


class PublisherQuery:
    @staticmethod
    def _get_path(order: Order, filename: str) -> str:
        return f"./services/sql/{order.value}/{filename}.sql"

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
        path = cls._get_path(Order.CREATE, 'bars')
        return cls._load_query_from_file(path)

    @classmethod
    def insert_bars(cls) -> str:
        path = cls._get_path(Order.INSERT, 'bars')
        return cls._load_query_from_file(path)

    @classmethod
    def select_bars_latest_time(cls) -> str:
        path = cls._get_path(Order.INSERT, 'bars_latest_time')
        return cls._load_query_from_file(path)
