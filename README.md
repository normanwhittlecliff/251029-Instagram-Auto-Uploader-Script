
# 📸 Instagram Auto-Uploader Script

A Python script that automatically uploads images and videos from a directory (including subfolders) to Instagram, where...

* 🖼 Images are uploaded as posts
* 🎬 Videos are uploaded as Reels
* 📝 Each upload uses the file name as the caption (perfect for date-based archives)
* 🔄 Automatically fixes vertical image rotation
* ⏳ Includes rate limiting
* 🧠 Keeps a log to avoid reposting files (Split into posted and errors)

## 📝 Information
- **Project ID**: 251029
- **Creator**: Norman Santos (normanwhittlecliff)
- **Date of Creation**: October 29, 2025
- **Language**: Python

## 🚀 Features

- ✔ Recursively scans all folders inside a given directory
- ✔ Uploads each image as a post
- ✔ Uploads each video as a Reel
- ✔ Uses file name (without extension) as caption
- ✔ Fixes EXIF rotation issues (common on phone photos)
- ✔ Prevents duplicate uploads using a log file
- ✔ Safe upload pacing to avoid Instagram rate limits
- ✔ Automatic cleanup of temporary files

## 📂 Example Folder Structure

```
media/
├── 2022/
│   ├── 2022-05-01.jpg
│   ├── 2022-05-02.mp4
│
├── 2023/
│   ├── 2023-01-10.png
│   ├── 2023-01-15.mov

```

Each file will be uploaded **once**, in a specific order, using:

```
Caption → 2022-05-01
Caption → 2022-05-02

Caption → 2023-01-10
Caption → 2023-01-15
```

## 🛠 Requirements & Dependencies

### 🐍 Python

Python 3.9 or newer

### 📦 Python Libraries

Install all dependencies with: 

```
pip install instagrapi pillow opencv-python
```

And the following due to a specific error that it can happen:

```
pip install instagrapi pillow opencv-python-headless
```
