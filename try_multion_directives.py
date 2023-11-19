
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

import multion

multion.login(use_api=True)

INSTRUCTION_SET = [
    'press " " (space) in the command bar, then stop immediately',
    'enter the text "tapOn search icon", then stop immediately',
    "press enter after the text you just entered, then stop immediately",
    "press the submit button"
]


def try_multion_directives():
    session_url = "http://localhost:9999"
    session = multion.new_session(
        {"input": 'press " " (space) in the command bar, then stop immediately', "url": session_url}
    )
    session_id = session["session_id"]
    current_url = session["url"]
    print(current_url)

    command_index = 1
    mode = "auto"
    current_status = "CONTINUE"
    while command_index < len(INSTRUCTION_SET):
        instruction = INSTRUCTION_SET[command_index]
        print(f"Executing command {command_index}: {instruction}")

        session = multion.update_session(
            session_id, {"input": instruction, "url": current_url}
        )

        print(session)
        current_status = session["status"]
        current_url = session["url"]
        session_details = {
            "command_index": command_index,
            "status": current_status,
            "url": current_url,
            "action_completed": session["message"],
            # "content": self._read_screenshot(session["screenshot"]),
        }
        command_index += 1


if __name__ == "__main__":
    try_multion_directives()
