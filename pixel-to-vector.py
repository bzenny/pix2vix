import cv2
import numpy as np
from PIL import Image
from svgpathtools import Path, Line, CubicBezier
import svgwrite
from vectori import trace_bitmap
import io

def pixel_to_vector(image_path, num_colors, output_file, smoothing=1.0, turdsize=2):
    # Open the image
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img_array = np.array(img)

    # Use K-means clustering to find the most dominant colors
    pixels = img_array.reshape(-1, 3)
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Quantize the image
    quantized = centers[labels.flatten()].reshape(img_array.shape).astype(np.uint8)

    # Create SVG drawing
    dwg = svgwrite.Drawing(output_file, size=img.size)

    # Process each color layer
    for color_idx in range(num_colors):
        # Create a binary image for this color
        color_mask = np.all(quantized == centers[color_idx].astype(int), axis=2).astype(np.uint8) * 255

        # Find contours using OpenCV
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Use vectori for tracing
        paths = trace_bitmap(color_mask, turdsize=turdsize, turnpolicy=2, alphamax=1.0, opticurve=1, opttolerance=0.2)

        # Convert vectori paths to svgpathtools paths for further processing
        svg_paths = []
        for path in paths:
            svg_path = Path()
            for curve in path:
                if len(curve) == 2:
                    svg_path.append(Line(complex(*curve[0]), complex(*curve[1])))
                elif len(curve) == 4:
                    svg_path.append(CubicBezier(complex(*curve[0]), complex(*curve[1]), complex(*curve[2]), complex(*curve[3])))
            svg_paths.append(svg_path)

        # Smooth paths using svgpathtools
        for path in svg_paths:
            path.smooth(smoothing=smoothing)

        # Convert the path to SVG and add it to the drawing
        color_hex = '#{:02x}{:02x}{:02x}'.format(*centers[color_idx].astype(int))
        for path in svg_paths:
            dwg.add(dwg.path(path.d(), fill=color_hex, stroke='none'))

    # Save the SVG file
    dwg.save()

    # Return SVG content as a string
    svg_output = io.StringIO()
    dwg.write(svg_output)
    return svg_output.getvalue()

# Example usage
# svg_content = pixel_to_vector('input_image.png', 4, 'output.svg', smoothing=1.0, turdsize=2)