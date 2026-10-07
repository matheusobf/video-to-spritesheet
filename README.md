# Video to Spritesheet Converter

![UI Preview](https://i.imgur.com/76S4LhO.png)

A modern, fast, and lightweight desktop application built with Python and CustomTkinter. This tool allows game developers, VFX artists, and 3D generalists to easily convert video files into a single high-resolution spritesheet image (texture atlas). 

It is highly optimized to prevent memory crashes and automatically calculates constraints to respect the absolute JPG/PNG size limits.

## ✨ Features

* **Modern GUI**: Built with CustomTkinter for a sleek, dark-mode user interface.
* **Smart Resolution Auto-fill**: Type a standard width (e.g., `3840`, `1920`, `1280`), and the app automatically fills in the correct 16:9 height.
* **Custom Framerate Extraction**: Extract frames at 5, 10, 15, 24, 30, or 60 FPS depending on your animation needs.
* **Memory Safety Constraints**: Automatically calculates the grid and prevents you from generating an image larger than `65,500 x 65,500` pixels (the maximum physical limit for standard image formats).
* **Standalone Output**: Saves the generated `.jpg` spritesheet directly into the original video's folder.

## 🚀 How to Use

1. Click **"Choose video file"** and select your video (`.mp4`, `.avi`, `.mov`, `.mkv`).
2. Enter the desired **Width** and **Height** for *each individual frame* inside the spritesheet.
3. Select the **Frames per Second (FPS)** you want to extract.
4. Click **"Convert to Spritesheet"**.
5. Wait for the progress bar to finish. The output image will be saved in the same directory as your video!

## 💻 Running from Source

If you want to run the python script directly, you will need **Python 3.8+** installed.

1. Clone this repository:
   ```bash
   git clone [https://github.com/matheusobf/video-to-spritesheet.git](https://github.com/matheusobf/video-to-spritesheet.git)
   cd video-to-spritesheet
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## 📦 How to Compile (Create an `.exe`)

You can compile this Python script into a standalone Windows executable so you can run it without a terminal or Python installed.

1. Make sure you have installed the requirements, which includes `pyinstaller`.
2. Run the following command in your terminal:
   ```bash
   python -m PyInstaller --noconsole --onefile app.py
   ```
3. Once the process is complete, navigate to the newly created `dist/` folder. Your `app.exe` will be waiting for you there.

## 🤝 How to Contribute

Contributions, issues, and feature requests are welcome! If you want to improve the code, follow these steps:

1. **Fork** the project.
2. Create your Feature Branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the Branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a **Pull Request**.

## ⚠️ Important Note Regarding 4K / High Res

Image formats like JPG and PNG have a hard limit of roughly 65,500 pixels per side. Because of this, if you attempt to generate a spritesheet using 4K frames (3840x2160) for a long video at a high FPS, the tool will stop you and tell you the maximum allowed duration. To bypass this, consider lowering your frame resolution or extracting at a lower FPS (like 10 or 15).

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.