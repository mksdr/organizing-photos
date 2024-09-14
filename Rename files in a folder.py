"""
어떠한 폴더 내의 모든 파일의 이름을 변경하는 간단한 스크립트입니다.
실행하기 전에 'folder_path'에 파일 이름을 변경할 폴더 경로를, 'new_file_name'에 변경할 파일 이름을 입력해주세요.

os.rename을 사용하여 파일 이름을 변경하므로, 파일 이름이 변경된 후에는 파일의 경로와 이름이 변경될 수 있습니다.
"""

import os

def rename_files_in_folder(folder_path):
    # 폴더 내의 파일 목록을 가져옵니다.
    files = os.listdir(folder_path)
    
    for filename in files:
        # 기존 파일 경로와 이름
        old_file_path = os.path.join(folder_path, filename)
        
        # 새로운 파일 경로와 이름
        new_file_name = '[*] ' + filename
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # 파일 이름 변경
        os.rename(old_file_path, new_file_path)
        # print(f"Renamed '{old_file_path}' to '{new_file_path}'")
        print(f'"{old_file_path}"의 이름을 "{new_file_path}"로 변경했습니다.')

folder_path = 'Folder' # 파일 이름을 변경하고자 하는 폴더의 경로
rename_files_in_folder(folder_path)