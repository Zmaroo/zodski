
import os
import matplotlib.pyplot as plt
from graphviz import Digraph

def project_directory_diagram(path, output_format):
    """
    A tool to generate a visual diagram of the user's project directory, illustrating
    the folder structure and files. The diagram is generated in the specified output
    format: 'png', 'jpg', or 'svg'.
    
    Parameters:
    - path (str): The path to the project directory.
    - output_format (str): The image format of the output diagram (e.g., 'png', 'jpg', 'svg').
    
    Returns:
    The path to the generated visual diagram.
    """
    
    if output_format not in ('png', 'jpg', 'svg'):
        raise ValueError("Invalid output format. Please choose 'png', 'jpg', or 'svg'.")
    
    if not os.path.isdir(path):
        raise NotADirectoryError("The provided path is not a directory.")
    
    dot = Digraph(comment='Project Directory Structure')

    for root, dirs, files in os.walk(path):
        # Normalize root path and make sure it's relative to the original directory for display
        root_display = os.path.relpath(root, start=path)
        root_display = root_display.replace('\\', '/')

        # Node for the directory
        dot.node(root_display, label=os.path.basename(root))
        
        # Nodes and edges for files in the directory
        for file in files:
            file_id = os.path.join(root_display, file)
            dot.node(file_id, label=file, shape='box')
            dot.edge(root_display, file_id)
        
        # Edges for subdirectories in the directory
        for _dir in dirs:
            dir_id = os.path.join(root_display, _dir)
            dot.edge(root_display, dir_id)

    # Generate the diagram
    output_path = '/mnt/data/project_diagram'
    dot.render(filename=output_path, format=output_format, cleanup=True)

    return f"{output_path}.{output_format}"

# Example usage:
# diagram_path = project_directory_diagram('/path/to/project', 'png')
# print(f"Diagram created at: {diagram_path}")
