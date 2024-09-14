import os
import random
import shutil
from datetime import datetime

def move_files(source_folder, destination_folder):
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"The source folder {source_folder} does not exist.")
        return
    
    # Check if destination folder exists, if not, create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"The destination folder {destination_folder} did not exist, so it was created.")
    
    # Walk through the source folder from the bottom up
    for root, dirs, files in os.walk(source_folder, topdown=False):
        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_folder, file)

            if os.path.exists(destination_file_path):
                base, extension = os.path.splitext(file)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randrange(0,100000))
                new_file_name = f"{base}__{timestamp}{extension}"
                destination_file_path = os.path.join(destination_folder, new_file_name)
            
            # Move the file
            # shutil.copy(source_file_path, destination_file_path)
            # print(f"Copied: {source_file_path} -> {destination_file_path}")

            shutil.move(source_file_path, destination_file_path)
            print(f"Moved: {source_file_path} -> {destination_file_path}")

if __name__ == "__main__":
    # Example usage
    source_folder = 'Folder'
    # destination_folder = 'Other Folder'
    destination_folder = source_folder

    move_files(source_folder, destination_folder)