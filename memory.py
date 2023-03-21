from pathlib import Path
from typing import Optional, List
import logging

from client import ChatClient

logger = logging.getLogger(__name__)


def _get_subject(response: str) -> Optional[str]:
    lines = response.split('\n')
    for l in lines:
        if l.startswith("SUBJECT:"):
            return l.replace("SUBJECT:", "").strip()

    return None


class Memory:
    def __init__(self):
        self.client = ChatClient("You are a data storage device.")
        self._memory_location: Path = Path('.memory')
        if not self._memory_location.exists():
            self._memory_location.mkdir()

    def already_remember(self, message: str) -> bool:
        logger.debug("Do you already remember this?")
        response = self.client.get_chat_response(
            f"""Does it sound like the person talking in this message has all possible information 
            about the topic in question? If yes, say YES and only YES, otherwise say, NO and only NO:\n{message}""")
        return response.startswith("YES")

    def list_memories(self) -> List[str]:
        return list(map(lambda x: x.name, self._memory_location.glob('*')))

    def load_memory(self, memory_name: str) -> str:
        p = self._memory_location.joinpath(memory_name)
        return p.read_text()

    def save(self, messages):
        print("saving memories...")
        message_list = '\n'.join([x['content'] for x in messages if x['role'] == 'user'])
        if len(message_list) == 0:
            return
        response = self.client.get_chat_response(
            f"""Please summarize the following text into a list of facts beneath a 
        subject heading. Preface the subject heading with SUBJECT:\n{message_list}""")
        subject = _get_subject(response)
        if subject is None:
            logger.error("Unable to save memory. Will be saved to error.mem")
            subject = "error.mem"
        full_path = self._memory_location.joinpath(subject)
        if not full_path.exists():
            full_path.write_text(response)
            print(f"Will remember {subject}")

    def find(self, memory: str) -> Optional[str]:
        logger.debug("Looking for memory")
        mem_list = '\n'.join(self.list_memories())
        logger.debug(f"Possible memories:\n{mem_list}")
        response = self.client.get_chat_response(
            f"""Which of the following subjects sounds like it contains information relevant to 
            the following message?  If any do, reply with the subject text and only the subject text.
            If none do, reply NONE and only NONE. Do not prefix the subject text with anything. Do no
            append any punctuation:
            Subjects:
            {mem_list}:
            Message:
            {memory}""")
        if response.startswith("NONE"):
            logger.debug("No relevant memories found")
            return None
        possible_path = self._memory_location.joinpath(response)
        logger.debug(f"Possible match: {possible_path}")
        if possible_path.exists():
            logger.debug(f"[Found possibly relevant memory '{response}']")
            return possible_path.read_text()
        logger.debug("Something found, but file name is a problem")
        return None
