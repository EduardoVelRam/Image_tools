# Image Processing Tools

A collection of small and independent image-processing tools developed in Python using [Streamlit](https://streamlit.io/). The project is intended as an experimental and educational collection of computer vision and digital image processing techniques, with a simple web-based interface for interacting with each tool.

The repository is designed to be easily extensible: each image-processing utility is stored as an independent Python module inside the `tools/` directory, while the main application dynamically discovers and loads the available tools.

## Features

The project currently includes eleven image-processing tools covering color manipulation, image compression, histogram analysis, image composition, geometric transformations, and other visual effects.

The tools do not require external AI APIs. Most operations are implemented using traditional image-processing techniques with libraries such as Pillow, NumPy, Matplotlib, and OpenCV. One of the tools, however, implements color inversion using a simple single-layer neural network as an experimental example.

## Project Structure

```text
ImageProcessingTools/
│
├── main.py
│
├── tools/
│   ├── __init__.py
│   ├── ...
│   └── ...
│
├── requirements.txt
│
└── README.md
```

The `main.py` file serves as the central application. Instead of explicitly importing every tool, it scans the `tools/` directory for Python files and dynamically imports the selected module.

The basic architecture is:

```python
for file in os.listdir("tools"):
    if file.endswith(".py") and file != "__init__.py":
        ...
```

Each tool exposes a `run()` function, allowing the main application to execute it without requiring modifications to `main.py`.

This makes it possible to add new tools simply by placing another compatible Python module inside the `tools/` directory.

## Available Tools

### 1. Black and White to Blue

**Black and White to Blue** converts a grayscale image into a blue-and-white version.

Instead of simply replacing black pixels with blue, the grayscale intensity is mapped to different shades of blue. Dark regions become darker blue tones, while brighter regions approach white.

This creates a monochromatic visual effect while preserving the tonal structure of the original image.

---

### 2. Image Compressor

**Image Compressor** reduces the file size of an image using different JPEG quality levels.

The user can select between four quality settings:

* High
* Medium
* Low
* Very Low

The application displays the resulting image and allows the user to compare the original and compressed file sizes.

This tool demonstrates the relationship between image quality, JPEG compression, and file size.

---

### 3. Color Inverter with Neural Network

**Color Inverter with Neural Network** performs color inversion using a simple single-layer neural network.

Unlike the conventional color inverter included in this repository, this tool approaches the transformation as a learning problem. The network receives pixel values as input and learns to produce their corresponding inverted values.

The tool is primarily experimental and educational, demonstrating how a relatively simple neural network can approximate a deterministic image transformation.

---

### 4. Color Quantizer

**Color Quantizer** reduces the number of colors used by an image without relying on AI algorithms.

The implementation reduces the number of available intensity levels for the RGB channels. As a result, several similar colors are mapped to the same representative intensity.

The effect can produce images with a poster-like or retro appearance while demonstrating a basic form of color quantization.

---

### 5. Color Inverter

**Color Inverter** creates the negative of an image by inverting its pixel intensities.

For an RGB image, each channel is transformed so that dark values become bright and bright values become dark.

This is one of the simplest tools in the collection and serves as an example of a direct pixel-level image transformation.

---

### 6. Image Format Converter

**Image Format Converter** allows users to convert an image between several common formats.

Supported output formats include:

* PNG
* JPEG
* BMP
* GIF
* TIFF
* WEBP

The tool uses Pillow to perform the conversion and provides the resulting image as a downloadable file.

---

### 7. Image Merger

**Image Merger** combines two images by controlling their relative transparency.

The user can upload two images and adjust the contribution of each image using an interactive parameter. The images are automatically resized to compatible dimensions before being merged.

This produces a simple visual blending effect and demonstrates alpha-style image composition.

---

### 8. Mosaic Effect

**Mosaic Effect** transforms an image into a geometric mosaic.

The image is divided into small regions, and the average color of each region is calculated. Each region is then represented using a geometric shape.

The available shapes include:

* Squares
* Circles
* Hexagons

The size of the individual mosaic elements can also be adjusted.

---

### 9. ID Photo Generator

**ID Photo Generator** takes a photograph and generates an image using a standard small identification-photo format.

The tool crops the original image to the required aspect ratio and resizes it to an appropriate resolution for printing.

It can be useful for experimenting with image cropping, aspect ratios, resolution, and preparation of photographs for physical printing.

---

### 10. Puzzle Converter

**Puzzle Converter** overlays a geometric puzzle pattern onto an image so that the resulting image can be printed and manually cut into pieces.

The current implementation uses geometric shapes rather than attempting to reproduce complex commercial jigsaw-piece geometry. This makes the generated cutting pattern easier to calculate and ensures that adjacent pieces share consistent boundaries.

The resulting image can be printed and used as a simple physical puzzle.

---

### 11. RGB Histogram

**RGB Histogram** calculates and displays the intensity histogram of each RGB channel independently.

The application provides histograms for:

* Red
* Green
* Blue

It also implements histogram equalization using the cumulative distribution function (CDF). Each RGB channel can therefore be transformed independently, allowing the user to compare the original and equalized intensity distributions.

This tool provides a practical demonstration of histogram analysis and contrast enhancement in digital images.

## Technologies

The project primarily uses:

* **Python** — Main programming language
* **Streamlit** — Interactive web interface
* **Pillow** — Image loading, manipulation, and format conversion
* **NumPy** — Numerical and pixel-level operations
* **OpenCV** — Computer vision and image-processing operations
* **Matplotlib** — Histogram visualization

The project is intentionally based on relatively simple techniques so that the implementation of each tool can be studied and modified independently.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd ImageProcessingTools
```

Create and activate a virtual environment if desired:

```bash
python -m venv venv
```

On Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available, the main dependencies can be installed with:

```bash
pip install streamlit pillow numpy opencv-python matplotlib
```

## Running the Application

Start the Streamlit application from the project root:

```bash
streamlit run main.py
```

A web browser should open automatically with the main application.

The available tools will be displayed in the sidebar. Select a tool to load its corresponding interface.

## Adding New Tools

The project is designed to make adding new tools straightforward.

Create a new Python file inside the `tools/` directory:

```text
tools/
└── my_new_tool.py
```

The module should contain a `run()` function:

```python
import streamlit as st

def run():
    st.title("My New Tool")

    # Tool implementation
```

No changes to `main.py` are required. The application automatically detects Python files inside the `tools/` directory and adds them to the selection menu.

This architecture allows the repository to grow organically as new image-processing experiments and utilities are developed.

## Purpose

This repository is primarily a personal collection of experiments, utilities, and learning projects related to digital image processing.

The goal is not to provide a single comprehensive image-processing framework, but rather to maintain a growing set of relatively small programs that demonstrate different techniques and transformations in an accessible way.

New tools and experiments will be added over time.
