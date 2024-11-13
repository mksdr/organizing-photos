'''
folder_path 변수에 할당된 폴더 내 중복 이미지를 찾아 제거하는 스크립트입니다.
'''

import os
import hashlib
from PIL import Image

def calculate_hash(image_path):
    """이미지 파일의 해시 값 계산"""
    try:
        with Image.open(image_path) as img:
            img_hash = hashlib.md5(img.tobytes()).hexdigest()
        return img_hash
    except (OSError) as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def remove_duplicate_images(folder_path):
    """폴더 내 중복 이미지를 찾아 제거"""
    hash_map = {}
    duplicate_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                file_path = os.path.join(root, file)
                file_hash = calculate_hash(file_path)

                if file_hash in hash_map:
                    # 중복 파일이 발견되면 삭제
                    os.remove(file_path)
                    duplicate_count += 1
                    print(f"Removed duplicate image: {file_path}")
                else:
                    # 처음 발견된 파일은 해시 맵에 저장
                    hash_map[file_hash] = file_path

    print(f"Total {duplicate_count} duplicate images removed.")

# 사용 예시
folder_path = "Folder"  # 중복 이미지를 확인할 폴더 경로
remove_duplicate_images(folder_path)
