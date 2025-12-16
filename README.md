# 🎨 Elsakr Favicon Generator

<p align="center">
  <img src="assets/Sakr-logo.png" alt="Elsakr Logo" width="120">
</p>

<p align="center">
  <strong>Generate all favicon sizes from a single image</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python">
  <img src="https://img.shields.io/badge/Platform-Windows-green?style=flat-square&logo=windows">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square">
</p>

---

## ✨ Features

- 🖼️ **Multi-format Input**: PNG, JPG, WebP, BMP
- 📦 **Complete Favicon Set**:
  - `favicon.ico` (16×16, 32×32, 48×48)
  - `favicon-16x16.png`
  - `favicon-32x32.png`
  - `apple-touch-icon.png` (180×180)
  - `android-chrome-192x192.png`
  - `android-chrome-512x512.png`
  - `mstile-150x150.png`
- 🎨 **Background Color**: Set custom background for transparent images
- 📋 **Auto-generated Files**:
  - `site.webmanifest`
  - Ready-to-use HTML snippet
- 👁️ **Live Preview**: See all sizes before exporting
- 🌑 **Premium Dark UI**: Modern, sleek interface

---

## 📸 Screenshot

<p align="center">
  <img src="assets/Screenshot.png" alt="App Screenshot" width="800">
</p>

---

## 🚀 Quick Start

### Option 1: Run from Source

```bash
# Clone the repository
git clone https://github.com/khalidsakr/elsakr-favicon-generator.git
cd elsakr-favicon-generator

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Option 2: Download EXE

Download the latest release from [Releases](https://github.com/khalidsakr/elsakr-favicon-generator/releases).

---

## 🛠️ Build Executable

```bash
# Activate venv first
pip install pyinstaller

pyinstaller --noconsole --onefile --icon="assets/fav.ico" --name="Elsakr Favicon Generator" --add-data "assets;assets" main.py
```

The executable will be in the `dist/` folder.

---

## 📁 Output Structure

After generating, you'll get:

```
favicons/
├── favicon.ico
├── favicon-16x16.png
├── favicon-32x32.png
├── apple-touch-icon.png
├── android-chrome-192x192.png
├── android-chrome-512x512.png
├── mstile-150x150.png
└── site.webmanifest
```

---

## 📋 HTML Code

Add this to your website's `<head>`:

```html
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="theme-color" content="#ffffff">
```

---

## 📦 Requirements

- Python 3.10+
- Pillow

---

## 📄 License

MIT License - [Elsakr Software](https://elsakr.company)

---

<p align="center">
  Made with ❤️ by <a href="https://elsakr.company">Elsakr</a>
</p>
