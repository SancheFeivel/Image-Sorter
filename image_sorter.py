import subprocess
import os
import shutil

working_folder = ""
exiftool_path = os.path.join(script_dir, "exiftool", "exiftool.exe")

def rating_check(full_file_path):
    result = subprocess.run([exiftool_path, full_file_path], stdout=subprocess.PIPE, text=True)

    rating = None
    for line in result.stdout.splitlines():
        if line.strip().startswith("Rating") and "Percent" not in line:
            print(line)
            rating = line.split(":")[1].strip()
    
    sorter(rating, full_file_path)

def sorter(rating, full_file_path):
    destination_path = os.path.join(working_folder, rating)
    os.makedirs(destination_path, exist_ok=True)
    destination_file = os.path.join(destination_path, os.path.basename(full_file_path))
    
    if not os.path.exists(destination_file):
        if rating in [ "1", "2", '3', "4", "5"]:
            shutil.move(full_file_path, destination_path)
            print(f"Moved {os.path.basename(full_file_path)} to {destination_path}")

    else:
        print(f"File {os.path.basename(full_file_path)} already exists, skipping.")


def process_all_images():
    total_images=0
    
    for filename in sorted(os.listdir(working_folder)):
        if filename.upper().endswith(".JPG"):
            total_images += 1
            full_file_path = os.path.join(working_folder, filename)
            print(f"Processing {filename}...")
            rating_check(full_file_path)
    
    print ("Processed",(total_images), "total images.")
    
def path_check():
    if not os.path.isdir(working_folder) and working_folder == "":
        print("Empty or Invalid folderpath")
    else:
        process_all_images()

def open_folder():
    print ("opening:", (working_folder))
    os.startfile(working_folder)


