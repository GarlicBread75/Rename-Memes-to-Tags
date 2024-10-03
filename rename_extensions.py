import os



path = 'C:/New Folder (71)/memes/'
for file in os.listdir(path):
    dot = file.rfind('.')
    ext = file[dot:]
    if ext in ['.jpg', '.bmp', '.jpeg', '.webp']:
        os.rename(path+file, path+file[:dot]+'.png')
    elif ext in ['.avi', '.mov', '.mkv', '.webm']:
        os.rename(path+file, path+file[:dot]+'.mp4')