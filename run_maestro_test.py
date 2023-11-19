import os
import subprocess
from lib.fs_helpers import get_script_cwd

OUTPUT_BASE_DIR = get_script_cwd("../output")


def run_maestro_test(run_id, test_filename, host='localhost'):
    """
    Run a single test with the given host and port, and return the result.
    """
    test_file_path = os.path.join(OUTPUT_BASE_DIR, run_id, test_filename)
    output_file_path = os.path.join(OUTPUT_BASE_DIR, run_id, "output.xml")
    debug_output_path = os.path.join(OUTPUT_BASE_DIR, run_id, "debug")
    cmd = f"maestro --host {host} test {test_file_path} --format junit --output={output_file_path} --debug-output={debug_output_path}"
    print(f"Running test {test_file_path}")
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
    )
    print(result)
    print("STDOUT")
    print(result.stdout.decode("utf-8"))
    print("\n\nSTDERR")
    print(result.stderr.decode("utf-8"))


if __name__ == "__main__":
    run_maestro_test("run-1", "example-launch-success.yaml", host='172.27.80.1')
    run_maestro_test("run-1", "example-fail.yaml", host='172.27.80.1')
