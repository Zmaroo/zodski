
import os
import shutil

def save_file_to_directory(file_path: str, directory: str, filename: str) -> str:
    """
    Save files to the specified directory within the tool_maker directory.

    Parameters:
    - file_path: The path of the file to be saved.
    - directory: The directory path where the file should be saved.
    - filename: The name of the file to be saved.

    Returns:
    - A string message indicating success or failure.
    """
    # Create the full path for the new file destination
    destination_path = os.path.join(directory, filename)
    
    # Ensure that the specified directory exists, creating it if necessary
    os.makedirs(directory, exist_ok=True)

    try:
        # Copy the file to the specified directory
        shutil.copy2(file_path, destination_path)
        return f"File '{filename}' has been saved to '{directory}' successfully."
    except Exception as e:
        return f"Error: {e}"
