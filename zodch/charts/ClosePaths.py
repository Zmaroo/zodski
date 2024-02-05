import xml.etree.ElementTree as ET
from pathlib import Path


worldInput = Path('c://Users/marle/zod/zodch/charts/static/img/world.svg')
worldOutput = Path('c://Users/marle/zod/zodch/charts/static/img/worldClosed.svg')

def close_open_paths(input_svg_file, output_svg_file):
    # Parse the SVG file
    tree = ET.parse(input_svg_file)
    root = tree.getroot()

    # Namespace handling for SVG files
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}

    # Iterate through all path elements in the SVG
    for path in root.findall('.//svg:path', namespaces):
        d = path.get('d')
        if d and not d.strip().endswith('Z'):
            path.set('d', d + ' Z')

    # Save the modified SVG to the output file
    tree.write(output_svg_file)

# Usage example:
close_open_paths(worldInput, worldOutput)
