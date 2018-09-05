import os
from Image import *
from Widgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QStackedWidget, QSizePolicy

class Image_Browser(QStackedWidget):

# An ImageBrowser widget is our main widget, created when the program is initialized

# StackedWidget allows us to display and switch between multiple widgets within 
# the same main window


### CONSTRUCTOR ###

    def __init__(self):

        # The ImageBrowser class is the main window which users interact with. 
        # It can switch between two views: thumbnail or zoomed. 

        super().__init__()

        self.selected_image_index = 0
        self.images = []

        self.initData()
        self.initUI()
        self.show()
    
    def initData(self, data_folder='./data'):

        file_names = sorted(os.listdir(data_folder))

        for file_name in file_names:
            if file_name == ".DS_Store":
                continue
            full_path = data_folder + "/" + file_name
            image = Image(self, full_path)
            self.images.append(image)

    ### UI INITIALIZATION ###

    def initUI(self, x=300, y=300, width=800, height=600):

        # Various window properties

        self.setWindowTitle('Image Browser')
        self.setGeometry(x, y, width, height)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(Qt.StrongFocus)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)
        self.setMaximumSize(1920, 1080)

        self.thumbnail_widget = ThumbnailWidget(self)
        self.tag_widget = TagView(self)

        self.addWidget(self.thumbnail_widget)
        self.addWidget(self.tag_widget)

    ### KEYBOARD INPUT ###
    
    def keyPressEvent(self, event):

        # Controls what happens on keyboard input. Users may navigate through images via keyboard input

        key = event.key()

        if key == Qt.Key_Left:
            self.selectPreviousImage()
            
        elif key == Qt.Key_Right:
            self.selectNextImage()

        elif key == Qt.Key_Return:
            if self.currentWidget() == self.thumbnail_widget:
                self.zoomIn()
            else:
                self.zoomOut()

        elif key == Qt.Key_Escape:
            if self.currentWidget() == self.tag_widget:
                self.zoomOut()

        
    def zoomOut(self):
        self.setCurrentWidget(self.thumbnail_widget)

    def zoomIn(self):
        self.setCurrentWidget(self.tag_widget)

    def setSelectedImageIndex(self, new_index):
        num_images = len(self.images)
        if new_index < 0:
            self.selected_image_index = num_images + new_index
        elif new_index >= num_images:
            self.selected_image_index = new_index - num_images
        else:
            self.selected_image_index = new_index

    def currentImage(self):
        return self.images[self.selected_image_index]

    def selectNextImage(self):
        self.setSelectedImageIndex(self.selected_image_index + 1)
        self.thumbnail_widget.selectNextImage()
        self.tag_widget.update()

    def selectPreviousImage(self):
        self.setSelectedImageIndex(self.selected_image_index - 1)
        self.thumbnail_widget.selectPreviousImage()
        self.tag_widget.update()