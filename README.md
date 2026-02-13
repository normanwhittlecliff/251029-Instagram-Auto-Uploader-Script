
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
- **Change Log**: [CHANGELOG.md](https://github.com/normanwhittlecliff/251029-Instagram-Auto-Uploader-Script/blob/main/CHANGELOG.md)

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

### 🔐 Instagram (Account Requirements)

**⚠️ Important**

- Your account must not be brand new
- Avoid uploading too many files at once
- Two-Factor Authentication works, but may require verification
- Automation can trigger Instagram security checks
- Use at your own risk.

## ▶️ How to Run

It is **highly recommended** that you run this script with a **IDE**, even if it's *Python's IDLE*. That's because and error can occur, which closes the entire script or, more likely, it can ask for a two-step verification, which I was only able to acomplish using a IDE.

Before running the script, be sure to configure the script.

### ⚙️ Configuration

Open the script and edit this section by adding your Instagram username, your Instagram password and the directory where the files are at:

```
USERNAME = "your_instagram_username"    # Ex: "normansvault" from @normansvault
PASSWORD = "your_instagram_password"    # Ex: "notmyrealpassword" from my password.
TARGET_DIRECTORY = r"C:\path\to\your\files"

UPLOAD_DELAY = 60  # Seconds between uploads
```

### ▶️ Hitting "Run"

After everything's set and the scipt is ran, the script will:

- Log into Instagram
- Scan every folder and subfolder
- Upload each file once
- Save uploaded files to a log
- Wait between uploads to avoid bans

### 🧠 How Duplicate Uploads Are Prevented

The script creates a file `posted_files.txt` and each successfully uploaded file path is stored there. If the script is run again, already posted files are skipped automatically.

If a file had an error while being uploaded, the script creates a file `error_log.txt` and the file path is stored there along with its error. Most errors don`t necessarly prevent the file from being uploaded, and that's something you might wanna check by yourself (sorry :/).

It is recommended that you take the uploaded file path in the `error_log.txt` file and move it to `posted_files.txt` so the script won't try to uploaded it again.

### 🔄 Image Rotation Fix (Important!)

Vertical images from phones often look sideways due to EXIF metadata.

This script:
- Reads the EXIF orientation tag
- Automatically rotates the image correctly
- Uploads the fixed version
- Keeps your original file untouched

### 🎬 Reel Thumbnail Handling

- Reels are uploaded without distortion
- A correctly sized 9:16 thumbnail is generated automatically called `thumb_temp.jpg`
- Prevents stretched or squashed preview images

### 📁 Temporary Files

The script may generate temporary files:

- `fixed_temp.jpg`
- `thumb_temp.jpg`


These files are (supposed to be) automatically deleted after the upload process finishes.

## ⚠️ Limitations & Warnings

Instagram does not officially support automation. Uploading too fast can result in:

- Temporary bans
- Account restrictions

Use UPLOAD_DELAY ≥ 60 seconds for safety and always test with a secondary account first.

## 🧩 Supported File Types

Images
- .jpg
- .jpeg
- .png
- .webp

Videos (Reels)
- .mp4
- .mov
- .avi

## 💡 Future Improvements (Ideas)

- Sort uploads by date

- Schedule uploads

- Auto-generate hashtags

- Convert HEIC images

- Blur borders instead of cropping thumbnails

- GUI interface

- Pull requests are welcome 🚀

## 📜 Disclaimer

This project is for personal and educational purposes only. 

I needed a "unlimited, easy to access" storage for the videos and photos I take with my phone, so I decided to upload it all to a private Instagram account.

You are responsible for how you use it and any consequences from Instagram.

Also, I'm really sorry for how messy this code of mine is.

## ⭐ Support

If this project helped you at all, consider giving it a star on GitHub! ⭐

That's it! :3

"Norman was here!"
