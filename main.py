from agent import AgentDB, AgentAlpacaApi, TimeFrame


def main():
    # agent_db = AgentDB()
    agent_alpaca = AgentAlpacaApi()
    d = agent_alpaca.request_bars_all(
        timeframe=TimeFrame.DAY_1,
        symbol='GLD',
        time_start='2021-10-01',
        time_end='2021-10-12'
    )
    print(d)


if __name__ == '__main__':
    main()
