import cv2
import numpy as np
from PIL import Image
import svgwrite

def pixel_to_vector(image_path, num_colors, output_file, smoothing=1.0, turdsize=2):
    # Open the image
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img_array = np.array(img)

    # Reduce colors using k-means clustering
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

        # Find contours
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Simplify contours
        for contour in contours:
            epsilon = smoothing * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) > turdsize:  # Only add contours with more points than turdsize
                color_hex = '#{:02x}{:02x}{:02x}'.format(*centers[color_idx].astype(int))
                points = [tuple(pt[0]) for pt in approx]
                dwg.add(dwg.polygon(points, fill=color_hex))

    # Save the SVG file
    dwg.save()

# Example usage
# pixel_to_vector('input_image.png', 4, 'output.svg', smoothing=1.0, turdsize=2)
