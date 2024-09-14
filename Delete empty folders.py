"""
어떠한 폴더 안에 있는 모든 하위 폴더 중에서 비어있는 폴더를 삭제하는 간단한 스크립트입니다.
실행하기 전에 'folder_path' 변수에 대상 폴더의 경로를 입력하고 실행하시기 바랍니다.
"""

import os

def delete_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            if not os.listdir(dir_path): # 폴더가 비어있다면 삭제
                os.rmdir(dir_path)
                # print(f"Deleted empty folder: {dir_path}")
                print(f'비어있는 폴더 삭제: {dir_path}')


folder_path = 'Folder' # 대상 폴더 경로
delete_empty_folders(folder_path)