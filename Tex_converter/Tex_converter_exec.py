'''
Tex converter
This tool generate .tex files of image files. It uses renderman txmake app. 
In the box, user needs to put the folder path where all images are and click on Generate tex button.
single image can also be converted to tex through the same process.

this file is connected to texcnvt_com_funcs.py file

Developed by
Girijashankar Senapati

'''

from PySide import QtCore, QtUiTools, QtGui
from PySide.QtCore import QFile
from PySide.QtGui import QWidget, QApplication, QProgressBar, QFileDialog
import os
import sys
import subprocess as sp

txmake_path = "/opt/pixar/RenderManProServer-23.5/bin/txmake"
al_format = ["png", "tif", "jpg", "jpeg", "exr", "hdr", "tiff"]
base_dir = "/mnt/assets/.Dev_data/app_libs/Tex_converter"

tex_converter_ui_file = os.path.join(base_dir, "ui_files", "tex_converter_gui_file.ui")
comm_func_file = os.path.join(base_dir, "common_funcs", "texcnvt_com_funcs.py")

sys.path.append(base_dir)
if os.path.exists(comm_func_file):
    import common_funcs.texcnvt_com_funcs as tcom_func
    reload(tcom_func)
else:
    raise Exception(comm_func_file + " is missing.")


def load_ui():
    ui_loader = QtUiTools.QUiLoader()
    file = QFile(tex_converter_ui_file)
    file.open(QFile.ReadOnly)
    ui = ui_loader.load(file)
    file.close()
    return ui


class SLWidget(QWidget):
    def __init__(self):
        super(SLWidget, self).__init__()
        self.ui = load_ui()
        self.ui.gen_tex_btn.clicked.connect(lambda: self.conv_btn_func(al_format,txmake_path))
        #self.ui.gen_tex_btn.clicked.clicked.connect(self.fileDialog())

    def fileDialog(self):
        """The QFileDialog this widget is using."""
        try:
            return self._filedialog
        except AttributeError:
            self._filedialog = d = QFileDialog(self)
            d.setFileMode(QFileDialog.Directory)
            return d

    def conv_btn_func(self, al_format, txmake_path):
        '''
        :param al_format: list:: image format list ["png", "tiff", "exr"]
        :param txmake_path: string:: pixar txmake path "/opt/pixar/RenderManProServer-23.5/bin/txmake"
        :param progress_bar_ui: string:: progress bar ui to show progress
        :return: None
        '''
        get_ui_dir = self.ui.dir_path_box.text()
        progress_bar_ui = self.ui.prgrs_bar
        if os.path.exists(get_ui_dir):
            tcom_func.convert_to_tex(txmake_path=txmake_path, dir_path=get_ui_dir, img_format=al_format, progress_bar=progress_bar_ui)
        else:
            print "Path missing: ", get_ui_dir
        return None


def main():
    print ""
    print "Running Tex generator......"
    print ""
    app = QApplication(sys.argv)
    win = SLWidget()
    win.ui.show()
    sys.exit(app.exec_())


main()


