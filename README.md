# Pix2Vix: Pixel to Vector Converter

Pix2Vix is a web application that converts pixel images to vector graphics (SVG format). It uses a combination of image processing techniques and machine learning to produce high-quality vector output.

## Features

- Upload PNG, JPG, or GIF images
- Choose the number of colors for quantization (2, 4, 8, or 16)
- Adjust smoothing and noise reduction parameters
- Preview uploaded images before conversion
- Download the resulting SVG file

## Technologies Used

- Python 3.11
- Flask
- OpenCV
- NumPy
- Pillow
- scikit-learn
- svgwrite
- svgpathtools
- vectori
- Tailwind CSS
- Font Awesome

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pix2vix.git
   cd pix2vix
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Upload an image, adjust the settings, and click "Convert"

4. The converted SVG file will be automatically downloaded

## Development

To run the application in debug mode, set the `FLASK_ENV` environment variable to `development`:

```
export FLASK_ENV=development  # On Windows, use `set FLASK_ENV=development`
python app.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).