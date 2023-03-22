from __future__ import annotations
from typing import List, Literal, Tuple, Dict
import os
import openai
import logging

from client import ChatClient
from memory import Memory

logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")


class ResponseNotPermittedException(Exception):
    ...


def _get_unfiltered_response(message) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}])
    return response['choices'][0]['message']['content'].strip()


class Monitor(ChatClient):
    def __init__(self, prefix: str = None):
        prefix = prefix or """Look at the list of topics below. If the following text discusses any of those topics
        rewrite the text so that it does not discuss those topics or minimizes discussion of them if not discussing
        them isn't possible. Only output the rewritten text. Do not preface the text with any notice that the text 
        was changed in any way."""
        super().__init__(prefix)
        self.topics = []

    def _build_query(self, response: str) -> str:
        query = f"{self.prefix}\nTopics:\n"
        for r in self.topics:
            query += f"- {r}\n"
        query += f"Text to evaluate:\n{response}"
        return query

    def evaluate_response(self, response: str) -> str:
        if not self.topics:
            return "OK"
        logger.debug(f"Unfiltered response: [{response}]")
        query = self._build_query(response)
        logger.debug(f"Checking rules: {query}")
        evaluation = _get_unfiltered_response(query)
        logger.debug(f"Evaluated response is: {evaluation}")
        return evaluation
            
            
class MonitoredChatClient(ChatClient):
    def __init__(self, prefix: str = None):
        super().__init__(prefix)
        self.memory = Memory()
        self.monitors: List[Monitor] = []
            
    def add_monitor(self, brain: Monitor):
        self.monitors.append(brain)

    def get_monitored_response(self, message: str):
        response = self.get_chat_response(message)
        need_mem = self.memory.need_memory(response)
        logger.debug(f"Need memory? {need_mem}")
        if need_mem:
            logger.debug("Will try to look up memory")
            mem_text = self.memory.find(message)
            logger.debug(f"Found memory text: {mem_text}")
            if mem_text:
                self.get_chat_response(f"Remember this: {mem_text}.")
                # Now try again.
                response = self.get_chat_response(message)

        for monitor in self.monitors:
            response = monitor.evaluate_response(response)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def save_memories(self):
        self.memory.save(self.messages)
