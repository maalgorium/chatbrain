from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Tuple
import logging

from fuzzywuzzy import fuzz

from client import ChatClient

logger = logging.getLogger(__name__)


@dataclass
class Subject:
    header: str
    body: str


def _get_subjects(response: str) -> List[Subject]:
    raw_subjects = [line.strip() for line in response.split("SUBJECT:") if line.strip() != '']
    subjects = []
    for subject in raw_subjects:
        lines = subject.split('\n')
        subjects.append(Subject(lines[0], subject))

    return subjects


class Memory:
    def __init__(self):
        self.client = ChatClient("You are a data storage device.")
        self._memory_location: Path = Path('.memory')
        if not self._memory_location.exists():
            self._memory_location.mkdir()
        self.current_memories: List[str] = self.list_memories()
        self.loaded_memories: List[str] = []

    def need_memory(self, message: str) -> bool:
        response = self.client.get_chat_response(
            f"""Does this sound like someone who was asked a question to which they did not know the answer, 
            or did they say something like, "I don't have the ability to remember":
            "{message}"
             If yes, say YES and only YES, otherwise say, NO and only NO""")
        return response.startswith("YES")

    def list_memories(self) -> List[str]:
        return list(map(lambda x: x.name, self._memory_location.glob('*')))

    def load_memory(self, memory_name: str) -> str:
        p = self._memory_location.joinpath(memory_name)
        text = p.read_text()
        self.loaded_memories.append(memory_name)
        return text

    def save(self, messages):
        print("saving memories...")
        message_list = '\n'.join([x['content'] for x in messages if x['role'] == 'user'])
        if len(message_list) == 0:
            logger.debug("Nothing to save.")
            return
        response = self.client.get_chat_response(
            f"""Please summarize the following text into a list of facts beneath a 
        subject heading. Preface the subject heading with SUBJECT:\n{message_list}""")
        subjects: List[Subject] = _get_subjects(response)
        for subject in subjects:
            if subject.header is None:
                logger.error("Unable to save memory. Will be saved to error.mem")
                subject.header = "error.mem"
            self._save_subject(subject)

    def _save_subject(self, subject: Subject):
        full_path = self._memory_location.joinpath(subject.header)
        if full_path.exists():
            subject.body = "\n" + subject.body
        with open(full_path, mode='a') as f:
            f.write(subject.body)
        print(f"Will remember {subject.header}")

    def find(self, memory: str) -> Optional[str]:
        logger.debug("Looking for memory")
        mem_list = '\n'.join(self.current_memories)
        logger.debug(f"Possible memories:\n{mem_list}")
        response = self.client.get_chat_response(
            f"""Which of the following subjects sounds like it contains information relevant to 
            the following message?  If any do, reply with the subject text and only the subject text.
            If none do, reply NONE and only NONE. Do not prefix the subject text with anything. Do not
            append any punctuation:
            Subjects:
            {mem_list}:
            Message:
            {memory}""")
        if response.startswith("NONE"):
            logger.debug("No relevant memories found")
            return None
        file_name = response
        if response in self.loaded_memories:
            logger.debug("Relevant memory already loaded")
            return None
        for m in self.list_memories():
            if fuzz.partial_ratio(response, m) > 90:
                file_name = m
                break
        logger.debug(f"Possible match: {file_name}")
        f = self._memory_location.joinpath(file_name)
        if f.exists():
            logger.debug(f"[Found possibly relevant memory '{response}']")
            return f.read_text()
        logger.debug("Something found, but file name is a problem")
        return None
