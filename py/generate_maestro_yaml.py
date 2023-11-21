import base64
import re
import shutil
import os
from openai import OpenAI
from dotenv import load_dotenv
from run_maestro_test import OUTPUT_BASE_DIR, run_maestro_test
from lib.fs_helpers import get_script_cwd, get_now_string

load_dotenv()
client = OpenAI()

INPUT_TASKS = [
    "Tap on the 'Search' tab at the bottom right corner",
    "Tap on the 'Search Wikipedia' bar at the top",
    "Type 'Mission Dolores Park'",
    "Tap on the 'Mission Dolores Park' item in the search result list",
    "Tap on the 'Save' icon, usually a star or bookmark symbol, to add to saved places",
    "Tap on the 'Places' tab at the bottom to go to saved places",
    "Verify that 'Mission Dolores Park' is listed under saved places",
]


def extract_last_triple_backticks(text):
    # Extract content within triple backticks
    results = re.findall(r'```(.*?)```', text, re.DOTALL)
    return results[-1] if results else None



def take_new_screenshot() -> str:
    # take screenshot of ios emulator:
    # xcrun simctl io booted screenshot --type=png last-screen.png
    # save last screen to last-screen.png 
    os.system("xcrun simctl io booted screenshot --type=png last-screen.png")
    return get_script_cwd("last-screen.png")

def convert_instruction_to_maestro_yaml_fragment(instruction, context="", screenshot_path="./initial-screenshot.jpg"):
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
    - swipe
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
    host = os.environ.get("MAESTRO_HOST", "localhost")
    print("Converting instructions to YAML")
    run_name = f"run-{get_now_string()}"
    base_dir = os.path.join(OUTPUT_BASE_DIR, run_name)
    os.makedirs(base_dir, exist_ok=True)

    tpl_test_file_path = get_script_cwd(
        "../maestro-tests/example-launch.yaml")
    base_test_file_path = os.path.join(base_dir, "example-launch.yaml")
    shutil.copy(tpl_test_file_path, base_test_file_path)

    for index, task in enumerate(INPUT_TASKS):
        test_file_name = f"example-launch-step-{index + 1}.yaml"
        base_test_file_path = os.path.join(base_dir, test_file_name)

        # Copy the template file or the last successful step file
        if index == 0:
            shutil.copy(tpl_test_file_path, base_test_file_path)
        else:
            shutil.copy(previous_step_file_path, base_test_file_path)

        context = ""
        screenshot_path = get_script_cwd(
            "../maestro-tests/initial-screen.png")

        for attempt in range(1, 4):  # Retry up to 3 times
            with open(base_test_file_path, "a") as f:  # Open in append mode
                result = convert_instruction_to_maestro_yaml_fragment(
                    task, context, screenshot_path=screenshot_path)
                new_instruction = result["output_yaml"]  or ''
                # Append the new instruction
                f.write("\n" + new_instruction)

            test_result = run_maestro_test(run_name, test_file_name, host=host)

            if test_result["status"] == "TEST_SUCCEEDED":
                print(f"Test succeeded on attempt {attempt}")
                previous_step_file_path = base_test_file_path  # Save for next step
                screenshot_path = take_new_screenshot()  # Save for next step
                break  # Break out of the retry loop if test succeeds
            elif test_result["status"] == "TEST_FAILED":
                print(f"Test failed on attempt {attempt}. Retrying...")
                # Provide context of failure for the next attempt
                # Read the contents of the current YAML file
                with open(base_test_file_path, "r") as f:
                    yaml_contents = f.read()

                # Prepare context with YAML file contents
                context = (f'Last iteration failed on step {task}.'
                           f'Transcript of failed test yaml is {yaml_contents}. The last line generated was {new_instruction}, test was successful upto there. So revise that line'
                           f'See screenshot of failure. Provide an alternate step instead.')
                screenshot_path = test_result["screenshot"]

                # Reset the test file for a fresh attempt
                if index == 0:
                    shutil.copy(tpl_test_file_path, base_test_file_path)
                else:
                    shutil.copy(previous_step_file_path, base_test_file_path)
            else:
                print(f"Test wasn't attempted on attempt {attempt} due to unexpected failure. Looping ...")

        # Check if all attempts failed
        if test_result["status"] != "TEST_SUCCEEDED":
            print(f"All retry attempts failed for task {index + 1}")

