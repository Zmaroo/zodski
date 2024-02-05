
import subprocess
import json

def vscode_powershell_executor(command: str) -> str:
    """
    Execute a PowerShell command to display the current user's directory structure.

    Parameters:
    - command: A string representing a powershell command to be executed

    Returns:
    - A string of the command output
    """
    # Using subprocess to execute the Power Shell command
    process = subprocess.run(["powershell", "-Command", command], capture_output=True)
    # Return either the stdout or the stderr output
    if process.returncode == 0:
        return process.stdout.decode()
    else:
        return process.stderr.decode()
