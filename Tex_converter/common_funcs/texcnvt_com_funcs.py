'''
Tex converter tool common functions.
This tool generate .tex files of image files. It uses renderman txmake app. 
In the box, user needs to put the folder path where all images are and click on Generate tex button.
single image can also be converted to tex through the same process.

this file is connected to Tex_converter_exec.py file.

Developed by
Girijashankar Senapati

'''

import os
import subprocess as sp


def get_all_data(dir_path):
    '''
    :param dir_path: string:: dir name  eg: "C:\Users\girija-ss\Desktop\Data\misc\Silhouette"
    :return: list :: eg: ["file.exr, file.png]
    '''
    return os.listdir(dir_path)


def verify_img_file(filename, al_format_list):
    '''
    :param filename: string:: file1.exr
    :param al_format_list: list:: ["png", "tiff", "exr"]
    :return: string:: file1.exr
    '''
    str_a = filename.split(".")[-1]
    if str_a.lower() in al_format_list:
        return filename
    else:
        return None


def gen_in_file(file_name, dir_path):
    '''
    :param file_name: string:: file1.exr
    :param dir_path: string:: dir name  eg: "C:\Users\girija-ss\Desktop\Data\misc\Silhouett"
    :return: string:: file path C:\Users\girija-ss\Desktop\Data\misc\Silhouette\file1.exr
    '''
    return os.path.join(dir_path, file_name)


def gen_out_file(file_name):
    '''
    :param file_name: string:: /home/ref_files/reft.png
    :return: string:: /home/ref_files/reft.tex
    '''
    str_a = file_name.split(".")[-1]
    out_file = file_name.replace(str_a, "tex")
    return out_file


def last_name(file_name):
    '''
    :param file_name: string:: /home/ref_files/reft.png
    :return: string:: reft.png
    '''
    return file_name.split("/")[-1]


def txmake_cmd(txmake_path, in_file, out_file):
    '''
    :txmake_path: string:: pixar txmake path "/opt/pixar/RenderManProServer-23.5/bin/txmake"
    :param in_file: string :: image path "/home/gshankar165/PycharmProjects/Tex_converter/ref_files/tower.jpg"
    :param out_file: string:: output tex path "/home/gshankar165/PycharmProjects/Tex_converter/ref_files/tower.tex"
    :return: integer:: return code
    '''
    cr_tex_files = sp.Popen([txmake_path, in_file, out_file])
    out, error = cr_tex_files.communicate()
    return cr_tex_files.returncode


def source_files(dir_path, img_format):
    '''
    this function clean out all images in the directory and create a fresh image files list to to convert to tex.
    :param dir_path: string:: "/home/gshankar165/PycharmProjects/Tex_converter/ref_files
    :param img_format: list :: eg: ["exr", "png" , "tiff"]
    :return: list:: all textures full path list ["/home/ref_files/tower.jpg", "/home/ref_files/roof_texture.png"]
    '''
    al_data = get_all_data(dir_path)
    al_clean_data = []
    for each_object in al_data:
        img_file = verify_img_file(filename=each_object, al_format_list=img_format)
        if img_file is not None:
            in_file_path = gen_in_file(file_name=img_file, dir_path=dir_path)
            al_clean_data.append(in_file_path)
    return al_clean_data


def convert_to_tex(txmake_path, dir_path, img_format, progress_bar):
    '''
    this functions generates tex files of all images list.
    :param txmake_path: string:: pixar txmake path "/opt/pixar/RenderManProServer-23.5/bin/txmake"
    :param dir_path: string:: "/home/gshankar165/PycharmProjects/Tex_converter/ref_files
    :param img_format: list :: eg: ["exr", "png" , "tiff"]
    :param progress_bar_ui: string:: progress bar ui to show progress
    :return: None
    '''
    if os.path.isdir(dir_path):
        source_file_list = source_files(dir_path=dir_path, img_format=img_format)
    else:
        source_file_list = [dir_path]
    # set progress bar value
    new_value = 0
    data_length = len(source_file_list)
    def_value = 100/data_length
    progress_bar.setValue(int(def_value))
    for each_file in source_file_list:
        new_value = def_value + new_value
        progress_bar.setValue(new_value)
        # start converting to tex
        target_file = gen_out_file(file_name=each_file)
        if os.path.exists(target_file):
            print "Skipping: tex file exists: ", last_name(file_name=target_file)
        else:
            run_txmake_cmd = txmake_cmd(txmake_path=txmake_path, in_file=each_file, out_file=target_file)
            if run_txmake_cmd is 0:
                if os.path.exists(target_file):
                    print "Done: ", last_name(file_name=target_file)
            else:
                print "Error: ", last_name(file_name=each_file)
    progress_bar.setValue(100)
    print ""
    print "The process has been completed"
    return None

