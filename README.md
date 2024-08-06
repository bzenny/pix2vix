# README.md
# Pixel to Vector Converter

This web application allows users to convert pixel images to vector SVG files using color quantization and path tracing.

## Features

- Upload PNG, JPG, JPEG, or GIF images
- Choose the number of colors for quantization (2, 4, 8, or 16)
- Adjust smoothing and noise reduction parameters
- Preview uploaded image before conversion
- Download the resulting SVG file

## Installation

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```
   python app.py
   ```
4. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Upload an image using the file input
2. Select the number of colors for quantization
3. Adjust the smoothing and noise reduction sliders if desired
4. Click "Convert" to process the image
5. The converted SVG file will automatically download when ready

## Technologies Used

- Python
- Flask
- NumPy
- Pillow
- scikit-learn
- svgwrite
- pypotrace

## License

This project is open source and available under the MIT License.