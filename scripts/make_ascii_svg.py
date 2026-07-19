import cv2
import sys

RAMP = " .`:-=+*cs#%@"
TARGET_WIDTH_CHARS = 75
CHAR_WIDTH = 8
CHAR_HEIGHT = 16

def generate_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load {input_path}. Did you run prep_photo.py first?")
        sys.exit(1)

    h, w = img.shape
    aspect_ratio = h / w
    target_height_chars = int(TARGET_WIDTH_CHARS * aspect_ratio * (CHAR_WIDTH / CHAR_HEIGHT))

    resized = cv2.resize(img, (TARGET_WIDTH_CHARS, target_height_chars))
    
    svg_width = TARGET_WIDTH_CHARS * CHAR_WIDTH
    svg_height = target_height_chars * CHAR_HEIGHT

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '<style>',
        '  .ascii { font-family: "Courier New", monospace; font-size: 14px; fill: #8b949e; }',
        '</style>',
        f'<rect width="{svg_width}" height="{svg_height}" fill="transparent" />'
    ]

    for y in range(target_height_chars):
        row_str = ""
        for x in range(TARGET_WIDTH_CHARS):
            pixel = resized[y, x]
            ramp_idx = int((255 - pixel) / 255 * (len(RAMP) - 1))
            # Just use the raw character directly, no special XML codes
            row_str += RAMP[ramp_idx]

        y_pos = (y + 1) * CHAR_HEIGHT
        delay = y * 0.04
        duration = 0.6
        clip_id = f"clip_{y}"

        svg_lines.append(f'<clipPath id="{clip_id}">')
        svg_lines.append(f'  <rect x="0" y="{y*CHAR_HEIGHT}" width="0" height="{CHAR_HEIGHT}">')
        svg_lines.append(f'    <animate attributeName="width" from="0" to="{svg_width}" begin="{delay}s" dur="{duration}s" fill="freeze" />')
        svg_lines.append('  </rect>')
        svg_lines.append('</clipPath>')
        
        # xml:space="preserve" forces the SVG to render blank spaces correctly
        svg_lines.append(f'<text x="0" y="{y_pos}" class="ascii" clip-path="url(#{clip_id})" xml:space="preserve">{row_str}</text>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Success! Animated SVG saved to {output_path}")

if __name__ == "__main__":
    generate_svg()