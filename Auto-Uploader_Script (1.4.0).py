print(">IMPORTING LIBRARIES...")

import os
import time
from PIL import Image, ExifTags
from instagrapi import Client
from time import sleep
from random import randint

print(">LIBRARIES IMPORTED!\n")

# ===================================
# CONFIGURATION
# ===================================

USERNAME = "your_username"      # Change it to your Instagram username
PASSWORD = "your_password"      # Change it to your Instagram password
TARGET_DIRECTORY = r"C:\Users\path\to\your\folder"  # Change to your folder

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi")

UPLOAD_DELAY = 60  # Delay between uploads (in seconds)
POSTED_LOG_FILE = "posted_files.txt"
ERROR_LOG_FILE = "error_log.txt"
TEMP_FIXED_IMAGE = "fixed_temp.jpg"  # Temporary file for corrected orientation


# ===================================
# COSMETIC FUNCTIONS
# ===================================

def converSecondsToTimeString(seconds):
    hours = 0
    while True:
        if seconds >= (60 * 60):
            hours += 1
            seconds -= 60 * 60
        else:
            break

    minutes = 0
    while True:
        if seconds >= (60):
            minutes += 1
            seconds -= 60
        else:
            break
        
    return f"{hours:02d}h{minutes:02d}m{seconds:02d}s";
    

def sleepCountDown(lastFile, seconds):
    for second in range(seconds):
        currentSecond = seconds - second
        if (currentSecond % 60 == 0) or (currentSecond < 60 and str(currentSecond)[-1] == "0"):
            print(f"Last File: {lastFile} | Waiting:", converSecondsToTimeString(seconds - second))
        sleep(1)
    print(0)


# ===================================
# REEL THUMBNAIL
# ===================================


import cv2
from PIL import Image

def generate_thumbnail(video_path, thumbnail_path="thumb_temp.jpg"):
    """
    Extracts a middle frame from the video, fixes orientation,
    and ensures proper 9:16 aspect ratio for Reels.
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    target_frame = frame_count // 2  # Middle frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    success, frame = cap.read()
    cap.release()

    if not success:
        return None

    # Convert BGR to RGB (OpenCV → Pillow format)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)

    # Resize & crop for 9:16
    width, height = img.size
    target_ratio = 9 / 16
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Too wide → crop sides
        new_width = int(height * target_ratio)
        offset = (width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, height))
    else:
        # Too tall → crop top & bottom
        new_height = int(width / target_ratio)
        offset = (height - new_height) // 2
        img = img.crop((0, offset, width, offset + new_height))

    img.save(thumbnail_path)
    return thumbnail_path




# ===================================
# IMAGE ORIENTATION FIXING
# ===================================

def fix_image_orientation(filepath):
    """
    Open image and fix EXIF rotation if needed.
    Returns a path to a corrected image (may be original or temp file).
    """
    try:
        image = Image.open(filepath)

        # Find EXIF orientation tag
        exif = image._getexif()
        if exif:
            for tag, value in ExifTags.TAGS.items():
                if value == "Orientation":
                    orientation_key = tag
                    break

            orientation = exif.get(orientation_key)

            # Apply rotation based on EXIF orientation
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
            else:
                return filepath  # No rotation needed

            # Save corrected copy
            image.save(TEMP_FIXED_IMAGE)
            return TEMP_FIXED_IMAGE

        return filepath  # No EXIF or no rotation needed

    except Exception:
        return filepath  # If any issue, use original


# ===================================
# SUPPORT FUNCTIONS
# ===================================

def login_instagram():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    return cl

def get_all_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def get_caption(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def load_posted_log():
    if not os.path.exists(POSTED_LOG_FILE):
        return set()
    with open(POSTED_LOG_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_to_log(filepath):
    with open(POSTED_LOG_FILE, "a") as f:
        f.write(filepath + "\n")

def save_to_error_log(filepath, error):
    with open(ERROR_LOG_FILE, "a") as f:
        f.write(filepath + "\nERROR: " + error + "\n\n")


# ===================================
# MAIN SCRIPT
# ===================================

def main():
    print("STARTING SCRIPT...")
    counting = 1
    numberOfFiles = 0
    cl = login_instagram()
    posted_files = load_posted_log()

    for filepath in get_all_files(TARGET_DIRECTORY):
        numberOfFiles += 1
        if filepath in posted_files:
            print(f"SKIPPING (already posted): {filepath}")
            continue

        caption = get_caption(filepath)
        print(f"{caption}")

        try:
            # IMAGE POST
            if filepath.lower().endswith(IMAGE_EXTENSIONS):
                corrected_path = fix_image_orientation(filepath)
                print(f"POSTING IMAGE: {filepath} (corrected: {corrected_path})")
                cl.photo_upload(corrected_path, caption)

            # VIDEO REEL (unchanged)
            elif filepath.lower().endswith(VIDEO_EXTENSIONS):
                print(f"POSTING REEL: {filepath}")
                thumb = generate_thumbnail(filepath)
                cl.clip_upload(filepath, caption, thumbnail=thumb)

            else:
                print(f"UNSUPPORTED FILE: {filepath}\n")
                continue
            print(f"✅ UPLOADED!")
            save_to_log(filepath)

        except Exception as e:
            print(f"❌ ERROR POSTING {filepath}: {e}\n")
            save_to_error_log(filepath, str(e))

        
        UPLOAD_DELAY = randint(60, 120)
        print(str(counting) + "|", end="")
        if counting == 3:
            sleepCountDown(
                filepath,
                UPLOAD_DELAY * randint(5, 7)  # 10, 12
                );
            #print(counting, filepath, UPLOAD_DELAY, randint(10, 20), UPLOAD_DELAY * randint(10, 20))
            counting = 1
        else:
            sleepCountDown(
                 filepath,
                 UPLOAD_DELAY
                )
            #print(counting, filepath, UPLOAD_DELAY, randint(10, 20), UPLOAD_DELAY * randint(10, 20))
            counting += 1
        print();

    # Cleanup temp image file
    if os.path.exists(TEMP_FIXED_IMAGE):
        os.remove(TEMP_FIXED_IMAGE)
    
    print("\nNumber of files uploaded: ", numberOfFiles)


if __name__ == "__main__":
    main()

input("\n\nScript Finished. Press Enter to exit program...")



