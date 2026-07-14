from agent.session_manager import SessionManager

manager = SessionManager()

while True:

    host = input("LANForge IP : ")

    ok, msg = manager.connect(host)

    print()

    print(msg)

    if ok:

        session = manager.get_session()

        print()

        print("Connected :", session.connected)

        print("Host      :", session.host)

        print()

        print("Stations")

        print(session.inventory.get_stations())

        break