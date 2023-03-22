import argparse
import logging
import sys

import openai

from brain import MonitoredChatClient, Monitor

# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger("openai").setLevel(logging.INFO)
# logging.getLogger("urllib3").setLevel(logging.INFO)


def set_up_monitors(client: MonitoredChatClient):
    prohibited_topics_monitor = Monitor()
    prohibited_topics_monitor.topics.extend(["Anything involving birds"])
    # client.monitors.append(prohibited_topics_monitor)


def main():
    client = MonitoredChatClient()
    set_up_monitors(client)
    while True:
        try:
            user_input = input("Talk to me> ")
            if user_input in ['exit', 'quit']:
                client.save_memories()
                return
            output = client.get_monitored_response(user_input)
            print(output)
        except EOFError:
            client.save_memories()
            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key',
                        help='Your Open AI API key. Will override environment variable OPENAI_API_KEY.', required=False)
    args = parser.parse_args()
    if args.key:
        openai.api_key = args.key
    main()
