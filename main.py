import logging

from brain import MonitoredChatClient, Monitor

# logging.basicConfig(level=logging.DEBUG)


def set_up_monitors(client: MonitoredChatClient):
    prohibited_topics_monitor = Monitor()
    prohibited_topics_monitor.topics.extend(["Anything involving birds"])
    client.monitors.append(prohibited_topics_monitor)


def main():
    client = MonitoredChatClient()
    set_up_monitors(client)
    while True:
        try:
            user_input = input("Talk to me> ")
            if user_input in ['exit', 'quit']:
                return
            output = client.get_monitored_response(user_input)
            print(output)
        except EOFError:
            return


if __name__ == '__main__':
    main()
