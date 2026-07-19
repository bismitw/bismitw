import json
import os

# GitHub's dark mode green palette
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
BOX_SIZE = 10
GAP = 4
WEEKS = 53
DAYS = 7

def render_svg(input_file="data/contributions.json", output_file="contrib-heatmap.svg"):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run fetch_contributions.py first.")
        return

    with open(input_file, "r") as f:
        data = json.load(f)
    
    # Calculate total SVG dimensions
    width = WEEKS * (BOX_SIZE + GAP) - GAP
    height = DAYS * (BOX_SIZE + GAP) - GAP + 20 
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<style>',
        '  .box { opacity: 0; }',
        '  @keyframes slideIn { to { opacity: 1; transform: translateY(0); } }',
        '</style>',
        f'<rect width="{width}" height="{height}" fill="transparent" />',
        '<g transform="translate(0, 10)">'
    ]

    # Map each day to a rectangle in the grid
    for i, day in enumerate(data):
        col = i // DAYS
        row = i % DAYS
        
        x = col * (BOX_SIZE + GAP)
        y = row * (BOX_SIZE + GAP)
        
        # Fallback to highest color if level somehow exceeds palette
        color = PALETTE[min(day["level"], len(PALETTE)-1)]
        
        # Calculate the diagonal delay for the wave animation
        delay = (col * 0.02) + (row * 0.02)
        
        svg_lines.append(
            f'  <rect x="{x}" y="{y}" width="{BOX_SIZE}" height="{BOX_SIZE}" rx="2" '
            f'fill="{color}" class="box" '
            f'style="transform: translateY(10px); animation: slideIn 0.4s ease forwards {delay}s" />'
        )

    svg_lines.append('</g>')
    svg_lines.append('</svg>')

    with open(output_file, "w") as f:
        f.write("\n".join(svg_lines))
    print(f"Success! Heatmap saved to {output_file}")

if __name__ == "__main__":
    render_svg()