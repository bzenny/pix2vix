# pixel_to_vector.py
import numpy as np
from PIL import Image
import potrace
import svgwrite
from sklearn.cluster import KMeans

def pixel_to_vector(image_path, num_colors, output_file, smoothing=1.0, turdsize=2):
    # Open the image
    with Image.open(image_path) as img:
        # Convert to RGB if it's not already
        img = img.convert('RGB')
        img_array = np.array(img)

    # Reshape the image to a list of RGB values
    pixels = img_array.reshape(-1, 3)

    # Use K-means clustering to find the most dominant colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(pixels)

    # Replace each pixel's color with the closest cluster center
    quantized = kmeans.cluster_centers_[kmeans.labels_].reshape(img_array.shape).astype(np.uint8)

    # Create SVG drawing
    dwg = svgwrite.Drawing(output_file, size=img.size)

    # Process each color layer
    for color in range(num_colors):
        # Create a binary image for this color
        binary = np.all(quantized == kmeans.cluster_centers_[color].astype(int), axis=2).astype(np.uint8) * 255

        # Trace the bitmap
        bmp = potrace.Bitmap(binary)
        path = bmp.trace(smoothing=smoothing, turdsize=turdsize)

        # Convert the path to SVG and add it to the drawing
        color_hex = '#{:02x}{:02x}{:02x}'.format(*kmeans.cluster_centers_[color].astype(int))
        dwg.add(dwg.path(
            potrace_path_to_svg_path(path),
            fill=color_hex,
            stroke='none'
        ))

    # Save the SVG file
    dwg.save()

def potrace_path_to_svg_path(path):
    svg_path = ""
    for curve in path:
        svg_path += f"M{curve.start_point.x},{curve.start_point.y}"
        for segment in curve:
            if segment.is_corner:
                svg_path += f"L{segment.c.x},{segment.c.y}L{segment.end_point.x},{segment.end_point.y}"
            else:
                svg_path += f"C{segment.c1.x},{segment.c1.y} {segment.c2.x},{segment.c2.y} {segment.end_point.x},{segment.end_point.y}"
    return svg_path



