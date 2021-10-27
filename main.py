from agent import AgentDB, AgentAlpacaApi, TimeFrame
from assistant import PublisherQuery


def main():
    agent_db = AgentDB()
    agent_alpaca = AgentAlpacaApi()
    payload = agent_alpaca.request_bars_payload(
        timeframe=TimeFrame.DAY_1,
        symbol='GLD',
        time_start='2016-01-01',
        time_end='2021-10-12'
    )
    query = PublisherQuery.insert_bars()
    # print(payload)
    # print(query)
    agent_db.insert_payload(query, payload)


if __name__ == '__main__':
    main()
