import os, string, random


def is_valid(file):
    global tags_file, temp_frame, invalid_list, duplicates_json

    dot = file.rfind('.')
    ext = file[dot:]
    valid_file = ext in ['.png', '.gif', '.mp4', '.jpg', '.bmp', '.jpeg', '.webp', '.avi', '.mov', '.mkv', '.webm']
    not_resources = file not in [tags_file, temp_frame, invalid_list, duplicates_json]
    return valid_file and not_resources


tags_file = '_tags_list.txt'
temp_frame = '_first_frame.png'
invalid_list = '_invalid_files.txt'
duplicates_json = '_duplicates.json'
path = 'C:\\New Folder (71)\\test\\'
for file in os.listdir(path):
    if not os.path.isdir(path+file) and is_valid(file):
        dot = file.rfind('.')
        extension = file[dot:]
        os.rename(path+file, path+''.join(random.choices(string.ascii_letters, k = 10))+extension)