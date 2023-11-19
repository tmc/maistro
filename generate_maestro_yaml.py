import base64
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

INPUT_TASKS = [
    "Tap on the 'Search' tab at the bottom right corner",
    "Tap on the 'Search Wikipedia' bar at the top",
]


def extract_last_triple_backticks(text):
    # Extract content within triple backticks
    results = re.findall(r'```(.*?)```', text, re.DOTALL)
    return results[-1] if results else None


def convert_instruction_to_maestro_yaml(instruction, context="", screenshot_path="./initial-screenshot.jpg"):
    BASE_PROMPT = """
    Maestro is a tool that allows you to create a YAML file that can be used to automate a task.

    In this task we are composing valid YAML fragments based on input statements. Please enter the YAML fragment that corresponds to the input statement in the Current Task section. Enclose your new YAML fragment in triple backticks. Do not add the ```yaml modifier, just vanilla ```.

    ## Examples ##

    ex1:
    Input: "Press Create New Contact"

    Output:
    ```
    - tapOn: "Create new contact"
    ```

    ex2:
    Input: "Enter first name 'Jar Jar'"

    Output:
    ```
    - tapOn: "First name"
    - inputText: "Jar Jar"
    ```

    ex3:
    Input: "Enter last name 'Binks'"

    Output:
    ```
    - tapOn: "Last name"
    - inputText: "Binks"
    ```

    ex4:
    Input: "Tap on the 'Search' tab at the bottom right corner"

    Output:
    ```
    - tapOn: "Search"
    ```

    ex5:
    Input: "Enter text 'Golden Gate Bridge' into the search bar"

    Output:
    ```
    - tapOn: "Search"
    - enterText: "Golden Gate Bridge"
    ```

    ## Commands dump from manual##

    - clearState
    - inputText: "Hello World"
    - openLink: https://example.com
    - pressKey: Enter
    - swipe:
        direction: LEFT
    - swipe:
        direction: RIGHT
    - swipe:
        direction: DOWN
    - swipe:
        direction: UP
    - scrollUntilVisible:
        element:
          id: "viewId" # or any other selector
          direction: DOWN # DOWN|UP|LEFT|RIGHT (optional, default: DOWN)
          timeout: 50000 # (optional, default: 20000) ms
          speed: 40 # 0-100 (optional, default: 40) Scroll speed. Higher values scroll faster.
          visibilityPercentage: 100 # 0-100 (optional, default: 100 Percentage of element visible in viewport
          centerElement: false # true|false (optional, default: false)


      ## Current task ##

      {context}

      Input: "{instruction}"
      Output:
    """

    current_prompt = BASE_PROMPT.format(
        context=context, instruction=instruction)

    image_data = open(screenshot_path, "rb").read()
    base64_encoded_data = base64.b64encode(image_data).decode("utf-8")

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": """
You are a GPT4 Vision assistant bot - you will be given a screenshot of a mobile simulator, running a chosen app, and a few next actions for testing. Please generate valid YAML for the testing framework to evaluate as per the instructions in your prompt.
                    """,
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": current_prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_encoded_data}"
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
    output_yaml = extract_last_triple_backticks(reply)
    return {"success": True, "output_yaml": output_yaml}


if __name__ == "__main__":
    print("Converting instructions to YAML")
    for task in INPUT_TASKS:
        print(task)
        result = convert_instruction_to_maestro_yaml(task)
        print(result)
