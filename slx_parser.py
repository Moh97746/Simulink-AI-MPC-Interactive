import zipfile
import xml.etree.ElementTree as ET
import os
import sys

def parse_slx(slx_path):
    if not slx_path.endswith('.slx'):
        print("Error: Please provide a valid .slx file.")
        return

    # Extract to temp
    temp_dir = 'temp_slx_extract'
    with zipfile.ZipFile(slx_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    xml_path = os.path.join(temp_dir, 'simulink', 'systems', 'system_root.xml')
    if not os.path.exists(xml_path):
        print("Error: system_root.xml not found. Is this a valid modern Simulink file?")
        return

    tree = ET.parse(xml_path)
    root = tree.getroot()

    blocks = {}
    lines = []

    # Parse Blocks
    for block in root.findall('.//Block'):
        sid = block.get('SID')
        b_type = block.get('BlockType')
        name = block.get('Name')
        if sid and b_type:
            blocks[sid] = {'name': name.replace('\n', ' '), 'type': b_type}

    # Parse Lines
    for line in root.findall('.//Line'):
        src_tag = line.find(".//P[@Name='Src']")
        dst_tag = line.find(".//P[@Name='Dst']")
        
        # Sometimes there are multiple branches
        branches = line.findall(".//Branch")
        
        src = src_tag.text if src_tag is not None else None
        
        dsts = []
        if dst_tag is not None:
            dsts.append(dst_tag.text)
        for b in branches:
            b_dst = b.find(".//P[@Name='Dst']")
            if b_dst is not None:
                dsts.append(b_dst.text)

        if src:
            src_id = src.split('#')[0]
            for d in dsts:
                dst_id = d.split('#')[0]
                lines.append((src_id, dst_id))

    # Clean up
    import shutil
    shutil.rmtree(temp_dir)

    generate_code(slx_path, blocks, lines)

def generate_code(slx_path, blocks, lines):
    base_name = os.path.basename(slx_path).replace('.slx', '')
    out_file = f"gen_{base_name}.py"
    
    code = f'\"\"\"Auto-generated Layout from {base_name}.slx\"\"\"\n'
    code += 'import sys, os\n'
    code += 'sys.path.insert(0, os.path.dirname(__file__))\n'
    code += 'from draw_light import *\n\n'
    
    code += 'fig, ax = setup_fig(24, 14)\n'
    code += 'ax.set_xlim(-2, 30)\n'
    code += 'ax.set_ylim(-2, 20)\n\n'
    
    code += 'C = COLORS\n\n'
    
    # Very naive layout: place blocks in a grid
    code += '# ====== BLOCKS ======\n'
    x, y = 0, 15
    block_coords = {}
    for sid, data in blocks.items():
        name = data['name']
        b_type = data['type']
        
        color = "C['fw']"
        if 'Gain' in b_type: color = "C['gain']"
        elif 'Sum' in b_type: color = "C['mux']"
        elif 'Subsystem' in b_type: color = "C['ai']"
        elif 'Out' in b_type or 'In' in b_type: color = "C['const']"
        
        code += f"draw_block(ax, {x}, {y}, 2.5, 1.5, '{name}', {color}, {color.replace(']', '_bg]')}, fontsize=10, gid='b_{sid}')\n"
        block_coords[sid] = (x + 2.5, y + 0.75)  # approximate output port
        
        x += 4
        if x > 20:
            x = 0
            y -= 3

    code += '\n# ====== WIRES ======\n'
    for src, dst in lines:
        if src in blocks and dst in blocks:
            code += f"# Wire from {blocks[src]['name']} to {blocks[dst]['name']}\n"
            # We don't have exact coordinates in this naive generator, so we just use draw_ortho_arrow placeholder
            # The user will need to adjust coordinates manually
            code += f"# draw_ortho_arrow(ax, [(X1, Y1), (X2, Y2)], C['fw'])\n"

    code += f'\nsave_fig(fig, "./{base_name}_Generated.png", dpi=300)\n'
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print(f"Auto-generation complete!")
    print(f"Found {len(blocks)} Blocks and {len(lines)} Wires.")
    print(f"Generated Python code saved to: {out_file}")
    print("Note: The layout is placed in a naive grid. You must open the generated file and manually adjust the X, Y coordinates and draw the wires for a professional look.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python slx_parser.py <model.slx>")
    else:
        parse_slx(sys.argv[1])
