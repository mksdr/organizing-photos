"""
파일의 정보를 JSON 파일로 저장하는 스크립트입니다. 파일 이름, 파일 경로, MD5 해시 값, 파일 용량을 수집하여 JSON 파일로 저장합니다.
'Delete from JSON.py' 또는 'Delete from JSON multi.py' 파일을 사용하여 중복 파일을 삭제하기 전에 JSON 파일로 저장하기 위해 만들어졌습니다.

실행하기 전에 'directory' 변수에 파일 정보를 수집할 폴더 경로를, 'output_file' 변수에 결과를 저장할 JSON 파일의 이름을 입력하시고 실행하시기 바랍니다.
1TB 이상의 대용량 파일이 있는 경우, 파일 용량을 수집하는 데 시간이 오래 걸릴 수 있습니다.
"""

import os
import hashlib
import json

def calculate_md5(file_path):
    """파일의 MD5 해시 값을 계산"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def collect_file_info(directory):
    """
    지정된 디렉토리와 모든 하위 폴더를 순회
    파일 이름, 파일 경로, MD5 해시 값, 파일 용량을 수집
    """
    file_info_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_hash = calculate_md5(file_path)

            file_info = {
                "file_name": file,
                "file_path": file_path,
                "hash": file_hash,
                "size": file_size
            }
            file_info_list.append(file_info)

    return file_info_list

def save_to_json(data, output_file):
    """수집한 파일 정보를 JSON 파일로 저장"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    directory = "Folder"  # 대상 폴더 경로
    output_file = "*.json"  # 결과를 저장할 JSON 파일 이름

    # 파일 정보 수집
    file_info = collect_file_info(directory)

    # JSON으로 저장
    save_to_json(file_info, output_file)

    # print(f"File information has been saved to {output_file}")
    print(f'파일 정보가 {output_file}에 저장되었습니다.')
