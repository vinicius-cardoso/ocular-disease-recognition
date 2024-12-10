# Ocular Disease Recognition

Projeto Multidisciplinar - Engenharia de Sistemas UFMG

## Features

- Recognize ocular diseases.
- Restrict uploads to common image formats (.png, .jpg, .jpeg, .gif).
- Limit file size to a maximum of 16MB.
- Clean and responsive interface.

## Requirements

Before running the project, ensure you have the following installed:

Python 3.7+
pip (Python package manager)

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/vinicius-cardoso/ocular-disease-recognition.git
cd ocular-disease-recognition
```

2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python app.py
```

The app will be available at http://127.0.0.1:5000.

## Directory structure

```bash
flask_image_uploader/
│
├── app.py               # Main application script
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # HTML template
├── static/
│   └── uploads/         # Directory to store uploaded images
├── README.md            # Project description and setup guide
```

## Usage

1. Open the app in your browser (http://127.0.0.1:5000).
2. Use the "Carregar" button to select an image from your computer.
3. Submit the image, and it will be displayed.

## License

This project is licensed under the MIT License. Feel free to use and modify it as you see fit.