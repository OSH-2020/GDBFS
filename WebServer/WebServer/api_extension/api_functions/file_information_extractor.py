import os
import time
import exifread
from geopy.geocoders import Photon


# extract geography information
# input [Latitude,Longitude],return address in ENGLISH list
def geo_extraction(latitude, longitude):
    # 通过经纬度解析地址
    try:
        geolocator = Photon(user_agent="my-application")
        position = geolocator.reverse(str(latitude) + ',' + str(longitude), limit=1)
        addr = position.address.split(',')
        result = []
        for attribute in addr:
            # 剔除address非中文部分，大概能精确到市
            if attribute.strip(' ').encode('UTF-8').isalpha():
                result.append(attribute)
    except Exception as err:
        result = []
        print(err)
    return result


# 格式化经纬度信息
def format_lati_long(data):
    list_tmp = str(data).replace('[', '').replace(']', '').split(',')
    list = [ele.strip() for ele in list_tmp]
    data_sec = int(list[-1].split('/')[0]) / (int(list[-1].split('/')[1])*3600)
    data_minute = int(list[1])/60
    data_degree = int(list[0])
    result = data_degree + data_minute + data_sec
    return result


# 提取文件exif信息
def exif_extraction(filepath):
    result = ''
    try:
        img = exifread.process_file(open(filepath, 'rb'))
        latitude = format_lati_long(str(img['GPS GPSLatitude']))
        longitude = format_lati_long(str(img['GPS GPSLongitude']))
        result = geo_extraction(latitude, longitude)
    except KeyError:
        # print("EXIF information doesn't include GPS attribute")
        result = None
    except OSError:
        # print("File doesn't exist or Permission denied")
        result = None
    except Exception as err:
        print("Unknown error happened!" + err.__str__())
    return result


# 时间戳转化为时间
def timestamp_to_time(timestamp):
    time_struct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%dT%H:%M:%S', time_struct)


# 获取文件时间信息
def time_extraction(filepath):
    try:
        fsize = os.path.getsize(filepath)
    except OSError:
        fsize = None
    try:
        fctime = timestamp_to_time(os.path.getctime(filepath))
    except OSError:
        fctime = None
    try:
        fmtime = timestamp_to_time(os.path.getmtime(filepath))
    except OSError:
        fmtime = None
    try:
        fatime = timestamp_to_time(os.path.getatime(filepath))
    except OSError:
        fatime = None
    return fsize, fctime, fmtime, fatime


# 获取文件信息
# 返回值为{文件大小，创建时间，修改时间，访问时间，(照片)拍摄地点(如果有的话)}
# 缺省值为None
def get_properties(filepath, filename_extension=None):
    fsize, fctime, fmtime, fatime = time_extraction(filepath)
    location = exif_extraction(filepath)
    return {'path': os.path.realpath(filepath),
            'name': os.path.split(filepath)[1],
            'size': fsize,
            'cTime': fctime,
            'mTime': fmtime,
            'aTime': fatime,
            'file_create_location': location}
