from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QPushButton, QScrollArea, QFrame, QStackedWidget, QMessageBox, QLineEdit, QComboBox, QCheckBox
from PySide6.QtGui import QPalette, QColor, QLinearGradient, QPixmap, QFont, QGuiApplication, QPainter, QImage, QIcon
from PySide6.QtWidgets import QApplication
from typing import Union
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from sql import Search
from datetime import date as dat


class RequestThread(QThread):
    finished = Signal(list)
    import time

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.run)
        self.timer.start()

    def run(self):
        if not mode:
            t = self.time.localtime()
            year = t.tm_year
            day_account = 366 if is_leap_year(year) else 365
            self.finished.emit([year, day_account, t.tm_yday, t.tm_hour, t.tm_min, t.tm_sec])
        else:
            t = self.time.localtime()
            year = t.tm_year
            now = dat(year, t.tm_mon, t.tm_mday)
            target = dat(int(data[0][2]), int(data[0][3]), int(data[0][4]))
            days = target - now
            self.finished.emit([data[0][1], days.days, t.tm_hour, t.tm_min, t.tm_sec])


def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


def is_valid_date(year, month, day):
    # 判断年份是否在合理范围内
    if year < 1 or month < 1 or month > 12:
        return False

    # 判断闰年和平年的每个月的天数
    max_days = [31, 28 + (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)), 31, 30, 31, 30, 31, 31, 30, 31, 30,
                31]

    # 判断天数是否在合理范围内
    if day < 1 or day > max_days[month - 1]:
        return False

    return True


def congig_bat():
    import os
    path = os.getcwd()
    pan = path[:2]
    print(pan)
    f = open('mb5.bat', 'w')
    str = rf"""@echo off
    {pan}
    cd "{path}"
    start "" "Countdown to Life.exe"
    """
    f.write(str)


def frame_widget(widget, layout=None, width=None, height=None) -> (QWidget, Union[QVBoxLayout, QHBoxLayout]):
    layout = QVBoxLayout() if layout == "v" else QHBoxLayout()
    widget.setLayout(layout)
    if height:
        widget.setFixedHeight(height)
    if width:
        widget.setFixedWidth(width)
    return widget, layout


def label_style(content, color, font):
    label = QLabel(content)
    label.setFont(QFont(*font))
    label.setStyleSheet(f"color: rgba{color}; background-color: transparent; border: 0px")
    return label


def label_img(label, img_path, img_width, img_height,  label_width=None, label_height=None, font=None, color=None):
    image = QImage(img_path)
    pixmap = QPixmap.fromImage(image.scaled(img_width, img_height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
    label.setPixmap(pixmap)
    if font:
        label.setFont(QFont(*font))
    if color:
        label.setStyleSheet(f"color: rgba{color}; background-color: transparent")

    return label


def separation(shape='h', color='(250, 250, 250, 240)'):
    separation_line = QFrame()
    separation_line.setLineWidth(1)
    separation_line.setStyleSheet(f'color: rgba{color};')
    line_shape = QFrame.Shape.HLine if shape == 'h' else QFrame.Shape.VLine
    separation_line.setFrameShape(line_shape)
    if shape == 'h':
        separation_line.setFixedHeight(1)
    else:
        separation_line.setFixedWidth(1)
    return separation_line


def scroll_area(scroll_area, shape='v', width=None, height=None):
    scroll_qss = """
      QScrollBar:vertical {
          border-width: 0px;
          border: none;
          background:rgba(64, 65, 79, 0);
          width:12px;
          margin: 0px 0px 0px 0px;
          border: none;
      }
      QScrollBar::handle:vertical {
          background: #DCDCDC;
          min-height: 20px;
          max-height: 20px;
          margin: 0 0px 0 0px;
          border-radius: 6px;
      }
      QScrollBar::add-line:vertical {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
          stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
          height: 0px;
          border: none;
          subcontrol-position: bottom;
          subcontrol-origin: margin;
      }
      QScrollBar::sub-line:vertical {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
          stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
          height: 0 px;
          border: none;
          subcontrol-position: top;
          subcontrol-origin: margin;
      }
      QScrollBar::sub-page:vertical {
      background: rgba(64, 65, 79, 0);
      }

      QScrollBar::add-page:vertical {
      background: rgba(64, 65, 79, 0);
      }
      QScrollArea {
        background-color: transparent;
        border: 0px; 
        }
            QScrollBar:horizontal {
          border-width: 0px;
          border: none;
          background:rgba(64, 65, 79, 0);
          height:12px;
          margin: 0px 0px 0px 0px;
          border: none;
      }
      QScrollBar::handle:horizontal {
          background:  #DCDCDC;
          min-width: 20px;
          max-width: 20px;
          margin: 0 0px 0 0px;
          border-radius: 6px;
      }
      QScrollBar::add-line:horizontal {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
          stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
          width: 0px;
          border: none;
          subcontrol-position: bottom;
          subcontrol-origin: margin;
      }
      QScrollBar::sub-line:horizontal {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
          stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
          width: 0 px;
          border: none;
          subcontrol-position: top;
          subcontrol-origin: margin;
      }
      QScrollBar::sub-page:horizontal {
      background: rgba(64, 65, 79, 0);
      }

      QScrollBar::add-page:horizontal {
      background: rgba(64, 65, 79, 0);
      }

    """
    scroll_qss_hor = """
      QScrollBar:horizontal {
          border-width: 0px;
          border: none;
          background:rgba(64, 65, 79, 0);
          height:12px;
          margin: 0px 0px 0px 0px;
          border: none;
      }
      QScrollBar::handle:horizontal {
          background:  #DCDCDC;
          min-width: 20px;
          max-width: 20px;
          margin: 0 0px 0 0px;
          border-radius: 6px;
      }
      QScrollBar::add-line:horizontal {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
          stop: 0 rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
          width: 0px;
          border: none;
          subcontrol-position: bottom;
          subcontrol-origin: margin;
      }
      QScrollBar::sub-line:horizontal {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
          stop: 0  rgba(64, 65, 79, 0), stop: 0.5 rgba(64, 65, 79, 0),  stop:1 rgba(64, 65, 79, 0));
          width: 0 px;
          border: none;
          subcontrol-position: top;
          subcontrol-origin: margin;
      }
      QScrollBar::sub-page:horizontal {
      background: rgba(64, 65, 79, 0);
      }

      QScrollBar::add-page:horizontal {
      background: rgba(64, 65, 79, 0);
      }

    """
    scroll_area.setWidgetResizable(True)
    scroll_area.viewport().setStyleSheet("background-color: transparent;")
    scroll_widget = QWidget(scroll_area)
    if shape == 'v':
        scroll_area.setStyleSheet(scroll_qss)
        frame = frame_widget(scroll_widget, layout='v', height=height, width=width)
    else:
        scroll_area.setStyleSheet(scroll_qss_hor)
        frame = frame_widget(scroll_widget, layout='h', height=height, width=width)
    scroll_area.setWidget(frame[0])

    return scroll_area, frame[1]


def input_widget(input, placehoder, width=None, height=None):
    input.setPlaceholderText(placehoder)
    input_qss = """QLineEdit {
            background-color: white;
            border: 0px solid rgba(20, 20, 20, 220);
            border-radius: 10px;
            padding: 12px;
        }
        """
    input.setStyleSheet(input_qss)
    input.setFont(QFont('Arial', 15))
    if width:
        input.setFixedWidth(width)
    if height:
        input.setFixedHeight(height)
    return input


def combox_widget(catalog, data, width, height):
    qss = """
        QComboBox
        {
            padding:2px;
            border-style:solid;
            border-radius:2px; 
            border-width:1px; 
            border-color: #FFFFFF;
            background-color: white;
            font-size: 14px;

        }
        QComboBox::drop-down
        {
            width:5px;
            border:0px;
        }

        QComboBox QAbstractItemView::item
        {
            font-size: 12px;
            height:25px; 
        }      

    """
    catalog.setMaxVisibleItems(4)
    if height:
        catalog.setFixedHeight(height)
    if width:
        catalog.setFixedWidth(width)
    catalog.addItems(data)
    catalog.setStyleSheet(qss)

    return catalog


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('The Countdown to Life')
        self.setWindowIcon(QIcon('img/time.png'))
        self.resize(1000, 650)
        primary = QGuiApplication.primaryScreen().availableGeometry()
        center = primary.center()
        self.move(center - self.rect().center())
        self.setWindowOpacity(1)
        self.background_color()
        # self.showMaximized()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(0)
        self.main_layout.addSpacing(175)

        self.show_inform()
        self.show_time()

        self.music_first_load = 0
        self.pixmap = QPixmap("")

        self.config()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def show_inform(self):
        top_widget = QWidget()
        self.top_widget = frame_widget(top_widget, layout='v')
        # self.top_widget[0].setStyleSheet("background-color: blue;")
        self.main_layout.addWidget(self.top_widget[0])
        self.content1 = label_style(content="221 days away from 2024 !", color='(255, 255, 255, 240)', font=('Arial', 20))
        self.content2 = label_style(content="Today has passed 17 hours ,", color='(255, 255, 255, 240)', font=('Arial', 20))
        self.content3 = label_style(content="and there are 11 hours, 23 minutes and 42 seconds left ...", color='(255, 255, 255, 240)', font=('Arial', 20))


        self.top_widget[1].setSpacing(20)
        self.top_widget[1].addWidget(self.content1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.top_widget[1].addWidget(self.content2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.top_widget[1].addWidget(self.content3, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch()

    def show_time(self):
        bottom_widget = QWidget()

        self.bottom_widget = frame_widget(bottom_widget, layout='h', height=80)
        self.main_layout.addWidget(self.bottom_widget[0])
        # self.bottom_widget[0].setStyleSheet("background-color: rgba(112, 128, 144, 100);")

        button = QWidget()
        self.button = frame_widget(button, layout='v', width=60, height=60)
        self.button[0].setStyleSheet("background-image: url('img/song.jpg');background-position: center;"
                                     "background-repeat: no-repeat; border-radius: 10px;"
                                     "background-color: rgba(112, 128, 144, 100)")
        self.button[0].mousePressEvent = self.play_music
        self.bottom_widget[1].addWidget(self.button[0])
        self.bottom_widget[1].addStretch()
        self.stop = QLabel("unpause")
        self.stop = label_img(self.stop, 'img/unpause.png', 26, 26, color='(235, 235, 235, 245)', font=('Arial', 9))
        self.button[1].addWidget(self.stop, alignment=Qt.AlignmentFlag.AlignCenter)

        self.set = label_style(content="setting", color='(255, 255, 255, 245)', font=('Arial', 12))
        self.bottom_widget[1].addWidget(self.set)
        self.bottom_widget[1].addSpacing(20)

    def start_thread(self):
        self.thread = RequestThread()
        self.thread.finished.connect(self.update_time)
        self.thread.start()

    def update_time(self, data):
        if not mode:
            self.content1.setText(f"{data[1]+1-data[2]} days away from {data[0]+1} !")
            self.content2.setText(f"Today has passed {data[3]} hours ,")
            self.content3.setText(f"and there are {23-data[3]} hours, {59-data[4]} minutes and {59-data[5]} seconds left ...")
        else:
            self.content1.setText(f"{data[1]} days away from {data[0]} !")
            self.content2.setText(f"Today has passed {data[2]} hours ,")
            self.content3.setText(
                f"and there are {23 - data[2]} hours, {59 - data[3]} minutes and {59 - data[4]} seconds left ...")

    def play_music(self, event):
        self.music_init()
        import pygame
        if not self.play_status:
            pygame.mixer.music.unpause()
            self.play_status = True
            self.stop.setText("pause")
            label_img(self.stop, 'img/pause.png', 26, 26)
        else:
            pygame.mixer.music.pause()
            self.play_status = False
            self.stop.setText("unpause")
            label_img(self.stop, 'img/unpause.png', 26, 26)

    def background_color(self):
        # 设置背景色为渐变色
        palette = QPalette()
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(28, 28, 38, 250))
        gradient.setColorAt(1, QColor(48, 48, 58, 250))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

    def show_child(self, event):
        if not self.set_window:
            self.set_window = Child()
        self.set_window.show()
        self.set_window.activateWindow()
        self.set_window.raise_()
        self.set_window.showNormal()

    def music_init(self):
        if not self.music_first_load:
            import pygame
            from os import listdir
            files_dirs = listdir()
            mp3_files = [file for file in files_dirs if file.endswith(".mp3")]
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_files[0])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.pause()
            self.music_first_load = 1
        else:
            pass

    def config(self):
        # music
        self.play_status = False

        # 子窗口
        self.set_window = None

        # 事件
        self.button[0].mousePressEvent = self.play_music
        self.set.mousePressEvent = self.show_child

        if not int(data[0][5]):
            self.pixmap = QPixmap("img/bac.png")
            self.update()
        else:
            self.pixmap = QPixmap("")
            self.update()

    def closeEvent(self, event):
        self.set_window.close()
        event.accept()


class Child(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("setting")
        self.setWindowIcon(QIcon('img/time.png'))
        self.resize(750, 500)
        primary = QGuiApplication.primaryScreen().availableGeometry()
        center = primary.center()
        self.move(center - self.rect().center())
        self.setWindowOpacity(1)
        self.background_color()

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(10)
        # self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.side()
        self.side_right()

        self.pixmap = QPixmap('')

        self.config()



    def side(self):
        side_widget = QWidget()
        self.side_widget = frame_widget(side_widget, layout='v', width=200)
        self.side_widget[0].setStyleSheet("background-color: rgba(112, 128, 144, 50)")
        self.main_layout.addWidget(self.side_widget[0])

        # line = separation(shape='v')
        # self.main_layout.addWidget(line)
        self.button_list()

    def side_right(self):
        # 创建stack， 并添加frame
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        self.put_right_frame1()
        self.put_right_frame2()
        self.put_right_frame3()

    def put_right_frame1(self):
        widget = QScrollArea()
        self.right_frame1 = scroll_area(widget, shape='v')

        self.stack.addWidget(self.right_frame1[0])

        self.right_frame1[1].setSpacing(10)

        self.put_frame1_content()

    def put_right_frame2(self):
        widget = QScrollArea()
        self.right_frame2 = scroll_area(widget, shape='v')
        self.stack.addWidget(self.right_frame2[0])

        self.right_frame1[1].setSpacing(10)

        self.put_frame2_content()

    def put_right_frame3(self):
        widget = QScrollArea()
        self.right_frame3 = scroll_area(widget, shape='v')
        self.stack.addWidget(self.right_frame3[0])

        self.right_frame3[1].setSpacing(30)
        self.put_frame3_content()

    def put_frame1_content(self):
        widget = QWidget()
        widget = frame_widget(widget, layout='h')
        self.right_frame1[1].addWidget(widget[0])
        content1 = label_style(content="Title", color='(255, 255, 255, 240)', font=('Arial', 18))
        widget[1].addWidget(content1, alignment=Qt.AlignmentFlag.AlignLeft)

        input = QLineEdit(self)
        self.input = input_widget(input, "Please enter a title")
        self.right_frame1[1].addWidget(self.input)

        self.right_frame1[1].addSpacing(20)

        widget = QWidget()
        widget = frame_widget(widget, layout='h')
        self.right_frame1[1].addWidget(widget[0])
        content1 = label_style(content="Data", color='(255, 255, 255, 240)', font=('Arial', 18))
        widget[1].addWidget(content1, alignment=Qt.AlignmentFlag.AlignLeft)

        widget = QWidget()
        widget = frame_widget(widget, layout='h')

        month = QComboBox()
        data = ('--Month--', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10 ', '11 ', '12 ')
        self.month = combox_widget(month, data=data, width=100, height=40)
        self.right_frame1[1].addWidget(widget[0])
        widget[1].addWidget(self.month)

        day = QComboBox()
        data = [str(i) + " " for i in range(1, 32)]
        data.insert(0, '--Day--')
        self.day = combox_widget(day, data=data, width=100, height=40)
        self.right_frame1[1].addWidget(widget[0])
        widget[1].addWidget(self.day)

        import time
        t = time.localtime()
        year = t.tm_year
        data = list((str(year + i) for i in range(9)))
        data.insert(0, '--Year--')
        year = QComboBox()
        self.year = combox_widget(year, data=data, width=100, height=40)
        self.right_frame1[1].addWidget(widget[0])
        widget[1].addWidget(self.year)

        widget[1].addSpacing(25)

        self.reset = label_style(content="default", color='(255, 255, 255, 250)', font=('Arial', 12))
        widget[1].addWidget(self.reset)


        qss = """
            QPushButton {
            font-family: Arial;
            background: transparent;
            margin-right: 5px;
            color: rgba(255, 255, 255, 220); 
            padding-top: 5px;
            padding-bottom: 5px;
            border-radius: 5px;
            border: 2px solid rgba(255, 255, 255, 220);
            }
            QPushButton:hover {
            color: rgba(255, 255, 255, 255);
            border: 2px solid rgba(255, 255, 255, 255);
            }
        """

        widget = QWidget()
        widget = frame_widget(widget, layout='h')
        self.save = QPushButton("save")
        self.save.setStyleSheet(qss)
        self.save.setFixedHeight(50)
        self.save.setFixedWidth(100)
        self.save.setFont(QFont('Arial', 14))
        self.right_frame1[1].addWidget(widget[0])
        widget[1].addSpacing(50)
        widget[1].addWidget(self.save, alignment=Qt.AlignmentFlag.AlignLeft)

        self.right_frame1[1].addStretch()

    def put_frame2_content(self):
        widget = QWidget()
        widget = frame_widget(widget, layout='v', height=130)
        widget[0].setStyleSheet("background-color: rgba(112, 128, 144, 70); border-radius:10")
        self.right_frame2[1].addWidget(widget[0])
        content1 = label_style(content="Theme", color='(255, 255, 255, 240)', font=('Arial', 18))
        widget[1].addWidget(content1, alignment=Qt.AlignmentFlag.AlignLeft)
        widget[1].setSpacing(10)

        layout = QHBoxLayout()
        layout.setSpacing(20)

        widget[1].addLayout(layout)

        theme1 = QWidget()
        self.theme1 = frame_widget(theme1, layout='v', width=100, height=70)
        self.theme1[0].setStyleSheet("background-image: url('img/song.jpg');background-position: center;"
                                     "background-repeat: no-repeat; border-radius: 10px;"
                        "background-color: rgba(112, 128, 144, 100); border: 2px solid raba(112, 128, 144, 200);")
        self.theme1[0].mousePressEvent = None
        layout.addWidget(self.theme1[0])
        label = label_style(content="Grass", color='(255, 255, 255, 240)', font=('Arial', 11))
        self.theme1[1].addWidget(label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        theme2 = QWidget()
        self.theme2 = frame_widget(theme2, layout='v', width=100, height=70)
        self.theme2[0].setStyleSheet("background-image: url('img/moun.png');background-position: center;"
                                     "background-repeat: no-repeat; border-radius: 10px;"
                        "background-color: rgba(112, 128, 144, 100); border: 2px solid raba(112, 128, 144, 200);")
        self.theme2[0].mousePressEvent = None
        layout.addWidget(self.theme2[0])
        label = label_style(content="Night", color='(255, 255, 255, 240)', font=('Arial', 11))
        self.theme2[1].addWidget(label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()


        widget = QWidget()
        widget = frame_widget(widget, layout='v')
        self.right_frame2[1].addWidget(widget[0])
        content1 = label_style(content="Other", color='(255, 255, 255, 240)', font=('Arial', 18))

        widget[1].addWidget(content1, alignment=Qt.AlignmentFlag.AlignLeft)
        widget[1].setSpacing(10)

        layout = QHBoxLayout()
        layout.setSpacing(20)

        widget[1].addLayout(layout)

        auto_open = QWidget()
        self.auto_open = frame_widget(auto_open, layout='h')
        qss = """
            QCheckBox{
                background-color: transparent;
                color: white;
            }
            QCheckBox::indicator{
             width: 30px;
             height: 30px;
            } 
            
            QCheckBox::indicator:unchecked {
                image: url(img/Switch-off.png);
            }
            QCheckBox::indicator:checked {
                image: url(img/Switch.png);
            
            }
        """
        content1 = label_style(content="auto-start on boot", color='(255, 255, 255, 240)', font=('Arial', 14))
        self.auto_open[1].addWidget(content1)
        self.auto_open[1].addStretch()
        self.auto_open[0].setStyleSheet("background-color: rgba(112, 128, 144, 70); border-radius:10")

        self.auto_open_checkbox = QCheckBox()
        self.auto_open_checkbox.setFont(QFont("Arial", 12))
        self.auto_open_checkbox.setStyleSheet(qss)
        self.auto_open[1].addWidget(self.auto_open_checkbox)

        layout.addWidget(self.auto_open[0])

        layout = QHBoxLayout()
        layout.setSpacing(20)

        widget[1].addLayout(layout)

        widget[1].addStretch()

    def put_frame3_content(self):
        self.right_frame3[1].addStretch()
        poem = ('spring is a lot of rain,',
                'summer is hot,',
                'autumn is a cool season in a year,',
                'winter is cold and sometimes snowy.'
                )
        for i in range(len(poem)):
            widget = QWidget()
            widget = frame_widget(widget, layout='h')
            self.right_frame3[1].addWidget(widget[0])
            content1 = label_style(content=poem[i], color='(255, 255, 255, 240)', font=('Arial', 18))
            widget[1].addWidget(content1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.right_frame3[1].addStretch()


    def background_color(self):
        # 设置背景色为渐变色
        palette = QPalette()
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(28, 28, 38, 250))
        gradient.setColorAt(1, QColor(48, 48, 58, 250))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def button_style(self):
        self.button_list_qss = '''
            QPushButton {
            font-family: Arial;
            background: transparent;
            margin-right: 5px;
            color: lightGray;
            text-align: left;  
            padding-left: 25px;
            padding-top: 16px;
            padding-bottom: 16px;
            border-radius: 10px;
            }
            QPushButton:hover {
            color: white;
            }
        '''
        self.button_list_qss_selected = '''
            font-family: Arial;
            text-align:left;
            background: rgba(220, 220, 220, 50%);;
            margin-right: 5px;
            color: white;
            padding-left: 25px;
            padding-top: 16px;
            padding-bottom: 16px;
            border-radius: 10px;
        '''

    def button_list(self):
        self.button_style()
        self.list1 = QPushButton('Custom Timer')
        self.list1.setStyleSheet(self.button_list_qss_selected)
        self.list1.setFont(QFont('Arial', 14))
        self.side_widget[1].addWidget(self.list1)

        self.list2 = QPushButton('Appearance')
        self.list2.setStyleSheet(self.button_list_qss)
        self.list2.setFont(QFont('Arial', 14))
        self.side_widget[1].addWidget(self.list2)

        self.list3 = QPushButton('More')
        self.list3.setStyleSheet(self.button_list_qss)
        self.list3.setFont(QFont('Arial', 14))
        self.side_widget[1].addWidget(self.list3)

        self.side_widget[1].addStretch()

    def config(self):
        self.loading_seting()

        self.list1.clicked.connect(lambda: self.change_button(self.list1, self.right_frame1[0]))
        self.list2.clicked.connect(lambda: self.change_button(self.list2, self.right_frame2[0]))
        self.list3.clicked.connect(lambda: self.change_button(self.list3, self.right_frame3[0]))
        self.list3.clicked.connect(lambda: self.change_button(self.list3, self.right_frame3[0]))

        self.save.clicked.connect(lambda: self.update_set())
        self.reset.mousePressEvent = self.update_default

        self.theme1[0].mousePressEvent = lambda event=None: self.theme_change(theme=0)
        self.theme2[0].mousePressEvent = lambda event=None: self.theme_change(theme=1)

        self.auto_open_checkbox.clicked.connect(self.auto_open_event)

        self.init_ui()

        if not int(data[0][5]):
            self.pixmap = QPixmap("img/grass.png")
            self.update()
        else:
            self.pixmap = QPixmap("")
            self.update()

    def change_button(self, current_button, target_frame):
        list_buttons = [self.list1, self.list2, self.list3]
        for button in list_buttons:
            if button == current_button:
                button.setStyleSheet(self.button_list_qss_selected)
                self.stack.setCurrentWidget(target_frame)
                self.list1.setFont(QFont('Arial', 14))
            else:
                button.setStyleSheet(self.button_list_qss)
                self.list1.setFont(QFont('Arial', 14))

    def closeEvent(self, event):
        self.resize(750, 500)
        primary = QGuiApplication.primaryScreen().availableGeometry()
        center = primary.center()
        self.move(center - self.rect().center())

    def update_set(self):
        name = self.input.text()[:10]
        print(name)
        year = self.year.currentText() if self.year.currentText() != '--Year--' else '0'
        month = self.month.currentText() if self.month.currentText() != '--Month--' else '0 '
        day = self.day.currentText() if self.day.currentText() != '--Day--' else '0 '
        if is_valid_date(int(year), int(month[:-1]), int(day[:-1])) and name:
            sql = Search()
            sql.change(['1', name, year, month[:-1], day[:-1]])
            QMessageBox.information(self, "Tips", "Succeed! The settings take effect the next time you start up", QMessageBox.StandardButton.Yes,
                                    QMessageBox.StandardButton.Yes)

        elif not name:
            QMessageBox.information(self, "Tips", "The title is incorrect！", QMessageBox.StandardButton.Yes,
                                    QMessageBox.StandardButton.Yes)
        else:
            QMessageBox.information(self, "Tips", "The Date is incorrect！", QMessageBox.StandardButton.Yes , QMessageBox.StandardButton.Yes)

    def loading_seting(self):
        sql = Search()
        data = sql.find()
        self.theme_num = data[0][5]
        self.auto_open_num = data[0][6]
        self.max_num = data[0][7]

    def update_default(self, event=None):
        self.input.setText('')
        self.year.setCurrentIndex(0)
        self.month.setCurrentIndex(0)
        self.day.setCurrentIndex(0)
        self.input.setText('')

        sql = Search()
        sql.change([1, '', '', '', ''])
        print(sql.find())

        QMessageBox.information(self, "Tips", "The settings have been restored to default and will take effect on the next startup", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.Yes)

    def theme_change(self, theme=0):
        if theme == 0:
            window.pixmap = QPixmap("img/bac.png")
            self.pixmap = QPixmap('img/grass.png')
            window.update()
            self.update()
            sql = Search()
            sql.change_set([1, '0'], item='theme')

        elif theme == 1:
            window.pixmap = QPixmap("")
            self.pixmap = QPixmap('')
            window.update()
            self.update()
            sql = Search()
            sql.change_set([1, '1'], item='theme')

    def auto_open_event(self):
        is_checked = self.auto_open_checkbox.isChecked()
        import register
        if is_checked:
            sql = Search()
            sql.change_set([1, '1'], item='open_auto')
            import os
            current_file_path = os.getcwd() + "\\" + "mb5.bat"
            register.add_startup_registry(current_file_path)
            print(current_file_path)
            congig_bat()

        else:
            sql = Search()
            sql.change_set([1, '0'], item='open_auto')
            current_file_path = sys.argv[0]
            register.delete_startup_registry(current_file_path)
            print(current_file_path)

    def init_ui(self):
        sql = Search()
        data = sql.find()
        self.input.setText(data[0][1])
        self.year.setCurrentText(data[0][2])
        self.month.setCurrentText(data[0][3] + ' ')
        self.day.setCurrentText(data[0][4] + ' ')

        self.auto_open_checkbox.setChecked(True if int(data[0][6]) else False)


mode = 0
sql = Search()
data = sql.find()
if data[0][2] and data[0][3] and data[0][4]:
    mode = 1


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start_thread()
    sys.exit(app.exec())
