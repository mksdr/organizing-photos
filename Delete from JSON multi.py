"""
JSON 파일에 저장된 파일 정보를 사용하여 중복 파일을 삭제하는 스크립트입니다. 아래의 코드는 MD5 해시 값이 일치하는 파일을 찾아 삭제합니다.
'Delete from JSON.py' 파일에 멀티쓰레딩을 사용하여 더 빠르게 처리하도록 수정한 스크립트입니다.

실행하기 전에 'json_file' 변수에 JSON 파일 경로를, 'directory' 변수에 대상 폴더의 경로를 입력하시고 실행하시기 바랍니다.
멀티쓰레딩을 사용하여 파일을 처리하므로, 'max_workers'를 조정하여 스레드 수를 설정할 수 있습니다.
'Save file information as JSON.py' 파일을 사용하여 JSON 파일을 생성한 후에 사용하시기 바랍니다.


os.remove를 사용하여 파일을 삭제하므로, 파일이 삭제된 후에는 복구가 불가능할 수 있습니다. 사용 전에 참고하시기 바랍니다.
"""

import os
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_file_info(json_file):
    """JSON 파일에서 파일 정보를 불러오기"""
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_md5(file_path):
    """파일의 MD5 해시 값을 계산"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading file: {file_path}")
        print(e)
        return None

def find_and_delete_duplicates(file_path, json_):
    """파일 정보를 사용하여 지정된 디렉토리의 중복 파일을 삭제"""
    file_hash = calculate_md5(file_path)
    if file_hash is None:
        return
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

def process_files(directory, json_):
    """지정된 디렉토리와 모든 하위 폴더를 순회하며 파일을 처리"""
    with ThreadPoolExecutor(max_workers=4) as executor:  # max_workers를 조정하여 스레드 수를 설정
        futures = []
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                # 멀티쓰레딩으로 파일을 처리
                futures.append(executor.submit(find_and_delete_duplicates, file_path, json_))
        
        for future in as_completed(futures):
            try:
                future.result()  # 예외 처리를 위해 결과를 확인
            except Exception as e:
                print(f"Error in thread: {e}")


if __name__ == "__main__":
    json_file = "*.json"  # 파일 정보를 불러올 JSON 파일 경로
    directory = "Folder"  # 중복 파일을 검사할 대상 폴더 경로
    json_ = load_file_info(json_file)

    """지정된 디렉토리와 모든 하위 폴더를 순회"""
    process_files(directory, json_)