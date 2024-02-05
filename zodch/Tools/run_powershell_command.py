
import subprocess
import shlex

def run_powershell_command(command):
    try:
        # Execute the PowerShell command
        process = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        # Return a tuple containing the standard output and error
        return {
            "output": process.stdout,
            "error": process.stderr,
            "return_code": process.returncode
        }
    except subprocess.CalledProcessError as e:
        # In case of an error during command execution, return the error details
        return {
            "output": e.stdout,
            "error": e.stderr,
            "return_code": e.returncode
        }

# Example usage:
# result = run_powershell_command('Write-Host "Hello PowerShell"')
# print(result)
