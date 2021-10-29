from agent import AgentDB, AgentAlpacaApi, TimeFrame
from assistant import PublisherQuery


def test_insert_payload():
    agent_db = AgentDB()
    agent_alpaca = AgentAlpacaApi()
    payload = agent_alpaca.request_bars_payload(
        timeframe=TimeFrame.DAY_1,
        symbol='GLD',
        time_start='2016-01-01',
        time_end='2021-10-12'
    )
    query = PublisherQuery.insert_bars()
    agent_db.insert_payload(query, payload)


def main():
    agent_db = AgentDB()
    query = PublisherQuery.select_bars_latest_times()
    print(query)
    print(agent_db.execute(query, ('1Day',)))


if __name__ == '__main__':
    main()
