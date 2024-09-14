"""
JPG, JPEG, PNG 이미지 파일과 MP4, AVI, MOV 동영상 파일이 유효한지 확인하고,
파일이 유효하지 않거나 손상되었을 경우에, 파일을 삭제합니다.

실행하기 전에 'folder_path' 변수에 폴더 경로를 입력하시고 실행하시기 바랍니다.

이미지 파일이 유효한지 확인하는 방법은 PIL 라이브러리를 사용하였고,
동영상 파일이 유효한지 확인하는 방법은 OpenCV 라이브러리를 사용하였습니다.

os.remove를 사용하여 파일을 삭제하므로, 파일이 삭제된 후에는 복구가 불가능할 수 있습니다. 사용 전에 참고하시기 바랍니다.
"""

from PIL import Image
import cv2
import os

def is_valid_image(file_path):
    """주어진 파일이 유효한 이미지 파일인지 확인"""
    try:
        with Image.open(file_path) as img:
            img.verify()  # 이미지 파일이 손상되었는지 검사
            img.load()  # 이미지 파일이 실제로 로드되는지 검사
        return True
    except (IOError, SyntaxError):
        return False
    except Exception as e:
        print(f'IMG Error: {e}')
        return True

def is_valid_video(file_path):
    """주어진 파일이 유효한 동영상 파일인지 확인"""
    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return False
        # 첫 번째 프레임을 읽어보면서 확인 (파일이 열렸더라도 문제가 있을 수 있으므로)
        ret, _ = cap.read()
        cap.release()
        return ret  # 첫 프레임이 제대로 읽히면 True
    except cv2.error:
        return False

def is_image_file(filename):
    # 이미지 확장자인지 확인
    image_extensions = ['.jpg', '.jpeg', '.png']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def is_video_file(filename):
    # 동영상 확장자인지 확인
    video_extensions = ['.mp4', '.avi', '.mov']
    return any(filename.lower().endswith(ext) for ext in video_extensions)

# Folder path
folder_path = 'folder'  # 이미지 파일이 있는 폴더 경로를 입력하세요

for filename in os.listdir(folder_path):
    if is_image_file(filename):
        file_path = os.path.join(folder_path, filename)
        if not is_valid_image(file_path):
            print(f'손상된 파일: {filename}')
            ### 파일 삭제하기 ###
            os.remove(file_path)
        else:
            print(f'정상 파일: {filename}')
    elif is_video_file(filename):
        file_path = os.path.join(folder_path, filename)
        if is_valid_video(file_path):
            print(f'정상 파일: {filename}')
        else:
            print(f'손상된 파일: {filename}')
            ### 파일 삭제하기 ###
            os.remove(file_path)