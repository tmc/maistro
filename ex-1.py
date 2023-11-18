import base64
import multion
from multion import MultionToolSpec
from langchain.llms.openai import OpenAI as LangchainOpenAI
from langchain.agents import initialize_agent, AgentType

from langchain.tools import StructuredTool
import subprocess
import datetime
from openai import OpenAI

client = OpenAI()


def take_ios_simulator_screenshot(save_path):
    # Get current timestamp to create a unique file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_path}/ios_simulator_screenshot_{timestamp}.png"

    # Command to take screenshot of the iOS Simulator
    command = f"xcrun simctl io booted screenshot {filename}"

    try:
        # Execute the command
        subprocess.run(command, shell=True, check=True)
        print(f"Screenshot saved as {filename}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    # return contents of the file as a base64 encoded string:
    image_data = open(filename, "rb").read()
    base64_encoded_data = base64.b64encode(image_data).decode("utf-8")
    return base64_encoded_data


CANNED_RESULT="""
Save the location of Union Square, San Francisco to a list of favorite places.
Share the directions to Union Square, San Francisco with a contact.
Save the location of Union Square, San Francisco to a list of favorite places.
Share the directions to Union Square, San Francisco with a contact.
"""

def call_gpt_vision():
    return CANNED_RESULT
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are a GPT4 Vision assitant bot - you will be given a screenshot of the iOS simulator, please generate 2 high level tasks to test for, write each task on a newline",
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    # "text": "According to the screenshot, what is the next step so that I can listen to the same song at the same time with a friend?",
                    "text": """Give me 2 high level tasks to test for. Write them similar to below:
                    Find the day Sam Altman was removed from OpenAI.
                    Find how many first link clicks will get to "Philosophy" from the page "OpenAI"
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{take_ios_simulator_screenshot('.')}"
                    },
                },
            ],
        },
    ]
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=500,
    )

    reply = response.choices[0].message.content
    print(reply)
    return reply


multion_toolkit = MultionToolSpec(use_api=True, mode="auto")
browser = StructuredTool.from_function(multion_toolkit.browse)

multion.login()
multion.set_remote(False)
# multion.login(true, multion_api_key="01e57befda43447fafce549a5333f876")

llm = LangchainOpenAI()


agent = initialize_agent(
    tools=[browser],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

goals = call_gpt_vision()
goals = goals.split("\n")
print(call_gpt_vision())

MAESTRO_URL = "http://localhost:9999/interact"
# pass the image to GPT to generate a list of example features to test?


PROMPT1 = f"""
You are an AI Agent whose job is to use the search bar to enumerate all possible click actions. Here is the link to start from: {MAESTRO_URL}. DO NOT guess or make up any user information, instead ask user to provide any missing info. Do not use any placeholders.

Here are the high-level steps:
1. Go to {MAESTRO_URL}
2. Input the high level goal: {goals[0]} into the search bar starting with typing in " "
3. Print the output on screen
"""

PROMPT2 = f"""
You are an AI Agent whose job is to write high level UI automation tests using the Maestro framework. Here is the link to start from: {MAESTRO_URL}. Do not use any placeholders.

The high level goals are as follows:
{goals}

Here are the high-level steps:
1. Go to {MAESTRO_URL}
2. For each high level goal, develop a list of commands to build up to achieve the goal.
"""

print(PROMPT2)

response = agent(
    inputs={
        "input": PROMPT2,
    }
)
