
from dotenv import load_dotenv
import os
import time

# Load the .env file
load_dotenv()
import multion

multion.login(use_api=True)


def try_multion_directives(command):
    INSTRUCTION_SET = [
        'press " " (space) in the command bar, then stop immediately',
        f'enter the text "{command}" into the command bar input, then stop immediately. Enter the exact text within the double quotes. The full string exactly.',
        "press enter after the text you just entered, then stop immediately",
        "press the last submit button"
    ]

    session_url = "http://localhost:9999"
    session = multion.new_session(
        {"input": 'press " " (space) in the command bar, then stop immediately',
         "url": session_url}
    )
    session_id = session["session_id"]
    current_url = session["url"]
    print(current_url)

    command_index = 1
    mode = "auto"
    current_status = "CONTINUE"
    while command_index < len(INSTRUCTION_SET):
        instruction = INSTRUCTION_SET[command_index].format(command=command)
        print(f"Executing command {command_index}: {instruction}")

        session = multion.update_session(
            session_id, {"input": instruction, "url": current_url}
        )

        time.sleep(3)

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


COMMANDS = [
    "tapOn search icon",
    "input text 'dolores park' into search bar",
    "tap on 'mission dolores park'",
    "scroll down",
    "take screenshot to /tmp/screenshot-o.png"
]

if __name__ == "__main__":
    for command in COMMANDS:
        try_multion_directives(command)
