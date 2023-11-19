import os
import re
import subprocess
from dotenv import load_dotenv

load_dotenv()

from lib.fs_helpers import (
    get_script_cwd,
    extract_path,
    find_first_fext,
    find_first_png
)

OUTPUT_BASE_DIR = get_script_cwd("../output")


def run_maestro_test(run_id, test_filename, host='localhost'):
    """
    Run a single test with the given host and port, and return the result.
    """
    test_file_path = os.path.join(OUTPUT_BASE_DIR, run_id, test_filename)
    output_file_path = os.path.join(OUTPUT_BASE_DIR, run_id, "output.xml")
    debug_output_path = os.path.join(OUTPUT_BASE_DIR, run_id, "debug")
    cmd = f"maestro --host {host} test {test_file_path} --format junit --output={output_file_path} --debug-output={debug_output_path}"
    print(cmd)
    print(f"Running test {test_file_path}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
    )
    stdout = result.stdout.decode("utf-8")
    stderr = result.stderr.decode("utf-8")

    print(result)
    print("STDOUT")
    print(stdout)
    print("\n\nSTDERR")
    print(stderr)

    result_success = True if result.returncode == 0 else False

    if "No running emulator found" in stderr:
        return {"success": False, "message": "No running emulator found"}

    if "Flow Failed" in stdout:
        default_debug_folder = extract_path(stdout)
        if default_debug_folder:  # moves the debug folder to a more readable name "latest"
            cmd = f"rm {debug_output_path}/latest; cp -r {default_debug_folder} {debug_output_path}/latest"
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
            )

            return {"success": False, "output_xml": output_file_path, "debug_folder": f"{debug_output_path}/latest"}

    return {"success": result_success, "output_xml": output_file_path}


if __name__ == "__main__":
    # on windows the host is not localhost
    host = os.environ.get("MAESTRO_HOST", "localhost")
    print(run_maestro_test("run-1", "example-launch-success.yaml", host=host))
    print(run_maestro_test("run-1", "example-fail.yaml", host=host))
