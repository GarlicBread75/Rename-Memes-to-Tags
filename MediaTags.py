from tkinter import *
from tkinter import ttk, filedialog
from PIL import *
from PIL import Image, ImageTk
import cv2 as cv
import os
import simplejson as j

def add_tag():
    global input_tag, info_box, options, full_name, drop, tags_file

    txt = input_tag.get()
    if len(txt) < 1:
        if info_box['text'] == 'Input: Tag is empty!':
            info_box['text'] = 'Input: Tag is empty!!!'
        else:
            info_box['text'] = 'Input: Tag is empty!'
    else:
        txt = txt.replace('_', '').replace('!', '')
        if txt in options:
            if info_box['text'] == 'Input: Existent tag added!':
                info_box['text'] = 'Input: Existent tag added!!!'
            else:
                info_box['text'] = 'Input: Existent tag added!'
        else:
            resources_exists()
            with open(path+resources_folder+tags_file, 'a') as file:
                file.write(txt+'\n')
            options.append(txt)
            options.sort()
            drop['values'] = options
            info_box['text'] = 'Input: New tag added!'
        if txt not in full_name:
            full_name.append(txt)
        else:
            if info_box['text'] == 'Input: Tag already added!':
                info_box['text'] = 'Input: Tag already added!!!'
            else:
                info_box['text'] = 'Input: Tag already added!'

    input_tag.delete(0, END)

def change_file():
    global current_file, file_numbering, files_count, submit, next_file
    global preview, resized, img, info_box, max_size, full_name
    global file_name, duplicates, input_tag, drop, insert

    if 'Skipped' in info_box['text']:
        info_box['text'] = 'Info will show here.'
    current_file += 1
    if current_file < files_count:
        w, h = set_image_and_size(files[current_file])
        resized = ImageTk.PhotoImage(img.resize((w, h)))
        preview['image'] = resized
        preview.grid(row = 5, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = N+S+E+W)
        file_numbering['text'] = f'{current_file+1}/{files_count}'
        file_name['text'] = files[current_file]
        info_box['text'] = 'Info will show here.'
    else:
        finished()

    if len(full_name) > 0:
        dot = files[current_file-1].rfind('.')
        extension = files[current_file-1][dot:]
        new_name = ' '.join(full_name)
        full_name = []
        if new_name+extension not in duplicates.keys():
            os.rename(path+files[current_file-1], path+new_name+' _0'+extension)
            duplicates[new_name+extension] = 1
        else:
            os.rename(path+files[current_file-1], path+new_name+f' _{duplicates[new_name+extension]}'+extension)
            duplicates[new_name+extension] += 1   

def finished():
    global submit, next_file, insert, drop, input_tag, path, info_box, file_name
    global drop_text, file_numbering_text, input_tag_text, preview

    preview['image'] = ''
    preview.grid(row = 5, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = N+S+E+W)
    submit['command'] = submit_path
    next_file['state'] = 'disabled'
    insert['state'] = 'disabled'
    drop['state'] = 'disabled'
    input_tag['state'] = 'disabled'
    submit['text'] = 'Choose Folder'
    info_box['text'] = 'Finished!'
    file_name['text'] = ''
    input_tag_text['text'] = '      Choose'
    file_numbering_text['text'] = '           a'
    drop_text['text'] = '       Folder'
    undupe_notdupes()

def undupe_notdupes():
    for file in os.listdir(path):
        os.rename(path+file, path+file.replace(' _0', ''))

def set_image_and_size(file):
    global info_box, img, path, files, current_file, files_count, info_box

    dot = file.rfind('.')
    ext = file[dot:]

    files_left = True
    while not is_valid(file):
        current_file += 1
        if current_file >= files_count:
            files_left = False
            finished()
            break
        else:
            dot = files[current_file].rfind('.')
            ext = files[current_file][dot:]

    if not files_left:
        return 1, 1

    if ext in ['.png', '.gif']:
        img = Image.open(path+files[current_file])
    elif ext == '.mp4':
        cap = cv.VideoCapture(path+files[current_file])
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        status, frame = cap.read()
        if status:
            cv.imwrite(path+resources_folder+temp_frame, frame)
            img = Image.open(path+resources_folder+temp_frame)
    elif ext in ['.jpg', '.bmp', '.jpeg', '.webp']:
        os.rename(path+files[current_file], path+files[current_file][:dot]+'.png')
        img = Image.open(path+files[current_file])
    elif ext in ['.avi', '.mov', '.mkv', '.webm']:
        os.rename(path+files[current_file], path+files[current_file][:dot]+'.mp4')

    x, y = img.size
    aspect_ratio = 0
    if y > x:
        aspect_ratio = x/y
        x = int(max_size*aspect_ratio)
        y = max_size
    elif x > y:
        aspect_ratio = y/x
        x = max_size
        y = int(max_size*aspect_ratio)
    else:
        x = max_size
        y = max_size
    return x, y

def is_valid(file):
    global tags_file, temp_frame, files_list

    dot = file.rfind('.')
    ext = file[dot:]
    valid_file = ext in ['.png', '.gif', '.mp4', '.jpg', '.bmp', '.jpeg', '.webp', '.avi', '.mov', '.mkv', '.webm']
    not_resources = file not in [tags_file, temp_frame, files_list]
    return valid_file and not_resources

def add_tag_from_list():
    global input_tag, info_box, options, drop, full_name

    txt = drop.get()
    if len(txt) < 1:
        if info_box['text'] == 'List: Tag is empty!':
            info_box['text'] = 'List: Tag is empty!!!'
        else:
            info_box['text'] = 'List: Tag is empty!'
    else:
        info_box['text'] = 'List: Tag added!'
        if txt not in full_name:
            full_name.append(txt)
        else:
            if info_box['text'] == 'List: Tag already added!':
                info_box['text'] = 'List: Tag already added!!!'
            else:
                info_box['text'] = 'List: Tag already added!'
    input_tag.delete(0, END)
    drop.set(options[0])

def recalculate_dupes(original_filename, filename, ext):
    global duplicates, files

    if '!' in filename:
        filename = filename.replace('!', '')
    dot = filename.rfind('.')
    unext = filename[:dot]
    if filename in duplicates.keys():
        original_path = path+original_filename
        new_path = path+unext+f' _{duplicates[filename]}'+ext
        temp_path = path+unext+f' _{duplicates[filename]}!'+ext
        try:
            if original_path != new_path:
                os.rename(original_path, new_path)
        except FileExistsError:
            os.rename(new_path, temp_path)
            os.rename(original_path, new_path)
        files.append(unext+f' _{duplicates[filename]}'+ext)
        duplicates[filename] += 1
    else:
        original_path = path+original_filename
        new_path = path+unext+' _0'+ext
        temp_path = path+unext+'!'+ext
        try:
            if original_path != new_path:
                os.rename(original_path, new_path)
        except FileExistsError:
            os.rename(new_path, temp_path)
            os.rename(original_path, new_path)
        files.append(unext+' _0'+ext)
        duplicates[filename] = 1

def submit_path():
    global input_tag, submit, info_box, img, width, height, resized, preview, next_file, drop_text
    global files_count, files, insert, file_name, temp_txt, path, current_file, input_tag_text
    global duplicates, tags_file, options, drop, file_numbering_text

    current_file = 0
    files = []
    path = filedialog.askdirectory()+'/'
    resources_exists()
    if os.path.exists(path+resources_folder+files_list):
        os.remove(path+resources_folder+files_list)
    invalid = 0
    if os.path.exists(path):
        duplicates = {}
        files_count = 0
        for file in os.listdir(path):
            if not os.path.isdir(path+file):
                if is_valid(file):
                    space = file.rfind(' ')
                    dot = file.rfind('.')
                    extension = file[dot:]
                    dupe_tag = file[space+1:dot]
                    unduped = ''
                    if dupe_tag[0] == '_':
                        unduped = file[:space]+file[dot:]
                        
                    if len(unduped) > 0:
                        recalculate_dupes(file, unduped, extension)
                    else:
                        recalculate_dupes(file, file, extension)
                    files_count += 1
                    filelist[file] = 'valid'
                else:
                    invalid += 1
                    filelist[file] = 'invalid'

        if files_count > 0:
            submit['command'] = add_tag
            submit['text'] = 'Add tag'
            next_file['state'] = 'active'
            insert['state'] = 'active'
            input_tag['state'] = 'normal'
            file_numbering['text'] = f'{current_file+1}/{files_count}'
            drop['state'] = 'readonly'
            file_name['text'] = files[current_file]
            input_tag_text['text'] = 'Add tags here:'
            file_numbering_text['text'] = 'Current file:'
            drop_text['text'] = 'Tags list:'

            if os.path.exists(path+resources_folder+tags_file):
                for line in open(path+resources_folder+tags_file, 'r').readlines():
                    options.append(line.strip())
                options.sort()
            drop['values'] = options

            invalid = 0
            if invalid > 0:
                info_box['text'] = f'Skipped {invalid} invalid files.'
            else:
                info_box['text'] = 'Info will show here.'

            width, height = set_image_and_size(files[0])
            resized = ImageTk.PhotoImage(img.resize((width, height)))
            preview['image'] = resized
            
        else:
            if info_box['text'] == 'No valid files in path!':
                info_box['text'] = 'No valid files in path!!!'
            else:
                info_box['text'] = 'No valid files in path!'
    with open(path+resources_folder+files_list, 'w') as js:
        js.write(j.dumps(filelist, indent = 4))

def resources_exists():
    if os.path.exists(path+resources_folder):
        if not os.path.isdir(path+resources_folder):
            os.remove(path+resources_folder)
    else:
        os.makedirs(path+resources_folder)


#region
window = Tk()
window.geometry('350x450')
window.title('Media Tags')
window['background'] = '#a0a0a0'

path = ''
resources_folder = 'MediaTags Resources/'
tags_file = '_tags_list.txt'
temp_frame = '_first_frame.png'
files_list = '_files_list.json'
filelist = {}
duplicates = {}
files = []
files_count = 0
current_file = 0

info_box = Label(window, text = 'Choose a folder path.', bg = '#a0a0a0')
info_box.grid(row = 0, column = 1, sticky = N+S+E+W)

max_size = 300
img = Image.new
width, height = 0, 0
resized = Image.new
preview = Label(window, bg = '#804080')
preview.grid(row = 5, column = 0, columnspan = 3, padx = 10, pady = 10, sticky = N+S+E+W)

input_tag_text = Label(window, text = '      Choose', bg = '#a0a0a0')
input_tag_text.grid(row = 1, column = 0, sticky = 'w', padx = 5)
full_name = []
input_tag = Entry(window, state = 'disabled')
input_tag.grid(row = 1, column = 1, sticky = N+S+E+W)

next_file = Button(window, text = 'Next File', command = change_file, state = 'disabled', bg = '#d0d0d0', activebackground = '#d0d0d0')
next_file.grid(row = 2, column = 2, sticky = N+S+E+W, padx = 5)

options = ['']
    
file_numbering_text = Label(window, text = '           a', bg = '#a0a0a0')
file_numbering_text.grid(row = 2, column = 0, sticky = 'w', padx = 5)
file_numbering = Label(bg = '#a0a0a0')
file_numbering.grid(row = 2, column = 1, sticky = N+S+E+W)

drop_text = Label(window, text = '       Folder', bg = '#a0a0a0')
drop_text.grid(row = 3, column = 0, sticky = 'w', padx = 5)
drop = ttk.Combobox(master = window, values = options, state = 'disabled')
drop.grid(row = 3, column = 1, sticky = N+S+E+W)

insert = Button(window, text = 'Add tag from list', command = add_tag_from_list, state = 'disabled')
insert.grid(row = 3, column = 2, sticky = N+S+E+W, padx = 5)

file_name = Label(text = 'File names will show here.', bg = '#a0a0a0')
file_name.grid(row = 4, column = 0, columnspan = 3, sticky = N+S+E+W)

submit = Button(window, text = 'Choose Folder', command = submit_path)
submit.grid(row = 1, column = 2, sticky = N+S+E+W, padx = 5)
#endregion

window.mainloop()