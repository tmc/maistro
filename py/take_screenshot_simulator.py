import subprocess
import datetime


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


# Usage
take_ios_simulator_screenshot(".")  # Replace with your desired path
