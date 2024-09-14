"""
JSON 파일에 저장된 파일 정보를 사용하여 중복 파일을 삭제하는 스크립트입니다. 아래의 코드는 MD5 해시 값이 일치하는 파일을 찾아 삭제합니다.

실행하기 전에 'json_file' 변수에 JSON 파일 경로를, 'directory' 변수에 대상 폴더의 경로를 입력하시고 실행하시기 바랍니다.
'Save file information as JSON.py' 파일을 사용하여 JSON 파일을 생성한 후에 사용하시기 바랍니다.

os.remove를 사용하여 파일을 삭제하므로, 파일이 삭제된 후에는 복구가 불가능할 수 있습니다. 사용 전에 참고하시기 바랍니다.
"""

import os
import json
import hashlib

def load_file_info(json_file):
    """JSON 파일에서 파일 정보를 불러오기"""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_md5(file_path):
    """파일의 MD5 해시 값 계산"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_and_delete_duplicates(file_path, json_):
    """파일 정보를 사용하여 지정된 디렉토리의 중복 파일을 삭제"""
    file_hash = calculate_md5(file_path)
    for file_info in json_:
        if file_info["hash"] == file_hash:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    break
            except Exception as e:
                print(f"Error deleting file: {file_path}")
                print(e)

if __name__ == "__main__":
    json_file = "*.json"  # 파일 정보를 불러올 JSON 파일 경로
    directory = "Folder"  # 중복 파일을 검사할 대상 폴더 경로
    json_ = load_file_info(json_file)

    """지정된 디렉토리와 모든 하위 폴더를 하면서 삭제"""
    for root, dirs, files in os.walk(directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            find_and_delete_duplicates(file_path, json_)