import os

def generate_info_card(output_path="info-card.svg"):
    svg_width = 490
    svg_height = 250
    
    # Terminal colors matching GitHub Dark mode
    color_title = "#58a6ff"  # Blue
    color_label = "#3fb950"  # Green
    color_text = "#8b949e"   # Gray
    
    # Edit this array to change what your info card says!
    lines = [
        {"type": "title", "text": "bismit@github"},
        {"type": "separator", "text": "------------"},
        {"type": "row", "label": "Role", "text": "Software Engineer"},
        {"type": "row", "label": "Focus", "text": "Backend Engineering & Machine Learning"},
        {"type": "row", "label": "Languages", "text": "Python, JavaScript, TypeScript"},
        {"type": "row", "label": "Goals", "text": "AI/ML Engineer"},
    ]
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '<style>',
        '  .term { font-family: "Courier New", monospace; font-size: 14px; }',
        '  .title { fill: ' + color_title + '; font-weight: bold; }',
        '  .sep { fill: ' + color_text + '; }',
        '  .label { fill: ' + color_label + '; font-weight: bold; }',
        '  .val { fill: ' + color_text + '; }',
        '</style>',
        f'<rect width="{svg_width}" height="{svg_height}" fill="transparent" />'
    ]
    
    y_pos = 40
    line_height = 26
    
    for i, line in enumerate(lines):
        delay = i * 0.15  # 150ms stagger per line
        
        # SMIL animation for fading in
        svg_lines.append(f'<g opacity="0">')
        svg_lines.append(f'  <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.3s" fill="freeze" />')
        
        if line["type"] == "title":
            svg_lines.append(f'  <text x="20" y="{y_pos}" class="term title">{line["text"]}</text>')
        elif line["type"] == "separator":
            svg_lines.append(f'  <text x="20" y="{y_pos}" class="term sep">{line["text"]}</text>')
        elif line["type"] == "row":
            svg_lines.append(f'  <text x="20" y="{y_pos}" class="term label">{line["label"]}</text>')
            svg_lines.append(f'  <text x="100" y="{y_pos}" class="term val">{line["text"]}</text>')
            
        svg_lines.append('</g>')
        y_pos += line_height

    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Success! Info card saved to {output_path}")

if __name__ == "__main__":
    generate_info_card()
