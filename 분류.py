import os
import time
import shutil
from pymediainfo import MediaInfo
from datetime import timedelta
import datetime
from dateutil import parser
from PIL import Image
import piexif

##### 동영상 파일 처리 #####
def get_media_creation_date(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == 'General':
            return track.encoded_date or track.tagged_date
    return None


def convert_utc_to_kst__v(utc_time_str):
    # 문자열을 datetime 객체로 변환
    utc_time = parser.parse(utc_time_str)
    
    # 9시간 더해서 KST로 변환
    kst_time = utc_time + timedelta(hours=9)
    
    # KST 시간을 문자열로 변환
    kst_date_str = kst_time.strftime('%Y-%m-%d')
    
    return kst_date_str

##### 이미지 파일 처리 #####
def get_image_creation_date(file_path):
    try:
        image = Image.open(file_path)
        exif_data = piexif.load(image.info['exif'])
        creation_date = exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        return creation_date
    except KeyError:
        return None
    except piexif.InvalidImageDataError:
        print(f"|| Invalid EXIF data for file: {file_path}")
        return None
    except Exception as e:
        print(f"|| Error: {e}")
        return None

def convert_utc_to_kst__p(time_str):
    # 문자열을 datetime 객체로 변환
    date_obj = datetime.datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
    # datetime 객체를 원하는 형식의 문자열로 변환
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def get_modified_time(file_path):
    # 파일의 수정된 시간(타임스탬프)을 가져옴
    modified_time = os.path.getmtime(file_path)
    # 타임스탬프를 datetime 객체로 변환
    modified_time_dt = datetime.datetime.fromtimestamp(modified_time)
    return modified_time_dt


def organize_files_by_date(src_folder, dest_folder_base):
    for filename in os.listdir(src_folder):
        file_path = os.path.join(src_folder, filename)
        creation_date = None
        kst_time_str = None

        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v')):
            creation_date = get_media_creation_date(file_path)
            if creation_date:
                kst_time_str = convert_utc_to_kst__v(creation_date)
        elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.CR2')):
            # print('Hello World')
            creation_date = get_image_creation_date(file_path)
            # print(f'Creation date: {creation_date}')
            modified_date = get_modified_time(file_path)
            # print(f'Modified date: {modified_date}')
            if creation_date == None:
                # '''
                '''
                print('|||||\nNone\n')
                print(filename)
                time.sleep(0.1)
                kst_time_str = convert_utc_to_kst__p(str(modified_date).replace('-', ':'))
                '''
                kst_time_str = None
                # '''
            elif creation_date == '0000:00:00 00:00:00':
                # '''
                '''
                print('|||||\n0000\n')
                print(filename)
                time.sleep(0.1)
                kst_time_str = convert_utc_to_kst__p(str(modified_date).replace('-', ':'))
                '''
                kst_time_str = None
                # '''
            elif creation_date:
                try:
                    kst_time_str = convert_utc_to_kst__p(creation_date)
                except ValueError:
                    # kst_time_str = creation_date.split(' ')[1].replace(':', '-')
                    kst_time_str = None
            # print(f'KST time: {kst_time_str}')
        
        if kst_time_str:
            print(f'KST time: {creation_date}')
            if '-' in kst_time_str:
                year, month, _ = kst_time_str.split('-')
            elif '-' not in kst_time_str:
                # 문자열을 datetime 객체로 변환
                datetime_obj = datetime.datetime.strptime(kst_time_str, "%Y:%m:%d %H:%M:%S")

                # 각 구성 요소를 변수로 추출
                year = datetime_obj.year
                month = datetime_obj.month

            if year <= '2024':
                dest_folder = os.path.join(dest_folder_base, year, month)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                file_name = os.path.basename(file_path)
                dest_file_path = os.path.join(dest_folder, file_name)

                # 동일한 파일이 존재할 경우 타임스탬프 추가
                if os.path.exists(dest_file_path):
                    base, ext = os.path.splitext(file_name)
                    new_file_name = f"{base}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
                    dest_file_path = os.path.join(dest_folder, new_file_name)

                # shutil.copy(file_path, dest_file_path)
                shutil.move(file_path, dest_file_path)
                print(f'Copied {file_path} to {dest_file_path}')
                

# 사용 예시
src_folder = r'F:\GoPro'
dest_folder_base = r'C:\Users\USER\Desktop\Photos'

organize_files_by_date(src_folder, dest_folder_base)