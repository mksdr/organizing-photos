import os
import time
import random
import shutil
from datetime import datetime

def find_subfolders(path):
    subfolder_pairs = []
    
    # 첫 번째 수준의 하위 폴더들을 탐색
    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        
        if os.path.isdir(folder_path):
            # 두 번째 수준의 하위 폴더들을 탐색
            for subfolder_name in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder_name)
                
                if os.path.isdir(subfolder_path):
                    subfolder_pairs.append((folder_name, subfolder_name))
    
    return subfolder_pairs

def timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randrange(0,100000))


def move_files_with_timestamp(src_folder, dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print(f"Target folder '{dst_folder}' created.")

    for filename in os.listdir(src_folder):
        src_file = os.path.join(src_folder, filename)
        if os.path.isfile(src_file):
            dst_file = os.path.join(dst_folder, filename)
            if os.path.exists(dst_file):
                base, ext = os.path.splitext(filename)
                dst_file = os.path.join(dst_folder, f"{base}__{timestamp()}{ext}")

            # shutil.move(src_file, dst_file)
            shutil.copy(src_file, dst_file)
            print(f"Moved '{src_file}' to '{dst_file}'")
            time.sleep(0.01)

# 원본 폴더 경로
source_folder = r'C:\Users\USER\Desktop\listed Photos'
# 대상 폴더의 기본 경로
base_target_folder = r'Q:\MYBOX'
subfolder_pairs = find_subfolders(source_folder)
print(subfolder_pairs)

for f1, f2 in subfolder_pairs:
    src = os.path.join(source_folder, f1, f2)
    f1_ = f1 + '년'
    f2_ = str(int(f2)) + '월'
    dst = os.path.join(base_target_folder, f1_, f2_)
    move_files_with_timestamp(src, dst)