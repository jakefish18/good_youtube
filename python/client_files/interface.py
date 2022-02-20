# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'good_tube_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 568)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("*{\n"
"    border: none;\n"
"    font: Raleway 12px;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #000000;\n"
"    border-radius: 3px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_left_menu_container = QtWidgets.QFrame(self.centralwidget)
        self.frame_left_menu_container.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_left_menu_container.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.frame_left_menu_container.setStyleSheet("")
        self.frame_left_menu_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left_menu_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu_container.setObjectName("frame_left_menu_container")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_left_menu_container)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_left_menu = QtWidgets.QFrame(self.frame_left_menu_container)
        self.frame_left_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_left_menu.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.frame_left_menu.setBaseSize(QtCore.QSize(0, 0))
        self.frame_left_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu.setObjectName("frame_left_menu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_3.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_app_name = QtWidgets.QFrame(self.frame_left_menu)
        self.frame_app_name.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_app_name.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_app_name.setObjectName("frame_app_name")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_app_name)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lbl_app_name = QtWidgets.QLabel(self.frame_app_name)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.lbl_app_name.setFont(font)
        self.lbl_app_name.setStyleSheet("")
        self.lbl_app_name.setObjectName("lbl_app_name")
        self.horizontalLayout_6.addWidget(self.lbl_app_name, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.verticalLayout_3.addWidget(self.frame_app_name)
        self.frame_tool_box = QtWidgets.QFrame(self.frame_left_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_tool_box.sizePolicy().hasHeightForWidth())
        self.frame_tool_box.setSizePolicy(sizePolicy)
        self.frame_tool_box.setStyleSheet("")
        self.frame_tool_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_tool_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_tool_box.setObjectName("frame_tool_box")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_tool_box)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.toolBox = QtWidgets.QToolBox(self.frame_tool_box)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.toolBox.setFont(font)
        self.toolBox.setStyleSheet("QToolBox {\n"
"    text-align: left;\n"
"}\n"
"\n"
"QToolBox::tab{\n"
"    text-align: left;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit{\n"
"    background-color: #FFF6F6;\n"
"}\n"
"")
        self.toolBox.setObjectName("toolBox")
        self.settings_page = QtWidgets.QWidget()
        self.settings_page.setGeometry(QtCore.QRect(0, 0, 250, 415))
        self.settings_page.setStyleSheet("QPushButton:hover {\n"
"    border-radius: 6px;\n"
"    background-color: #fc8383;\n"
"}\n"
"QPushButton:pressed {\n"
"    border-radius: 6px;\n"
"    background-color: #ff4545;\n"
"}")
        self.settings_page.setObjectName("settings_page")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.settings_page)
        self.verticalLayout_5.setContentsMargins(0, 0, -1, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.settings_form = QtWidgets.QFrame(self.settings_page)
        self.settings_form.setStyleSheet("*{\n"
"    border: 5px solid #A061C1;\n"
"    border-radius: 20px;\n"
"    background-color: #A061C1;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: #FFFFFF;\n"
"    border: 5px solid #FFFFFF;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 5px solid #fc8383;\n"
"    background-color: #fc8383;\n"
"}\n"
"QPushButton:pressed {\n"
"    border: 5px solid #ff4545;;\n"
"    background-color: #ff4545;\n"
"}")
        self.settings_form.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.settings_form.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_form.setObjectName("settings_form")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.settings_form)
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lbl_new_login = QtWidgets.QLabel(self.settings_form)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_new_login.setFont(font)
        self.lbl_new_login.setObjectName("lbl_new_login")
        self.verticalLayout_6.addWidget(self.lbl_new_login)
        self.led_login = QtWidgets.QLineEdit(self.settings_form)
        self.led_login.setStyleSheet("background-color: #FFFFFF;")
        self.led_login.setObjectName("led_login")
        self.verticalLayout_6.addWidget(self.led_login)
        self.lbl_new_api_key = QtWidgets.QLabel(self.settings_form)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_new_api_key.setFont(font)
        self.lbl_new_api_key.setObjectName("lbl_new_api_key")
        self.verticalLayout_6.addWidget(self.lbl_new_api_key)
        self.led_api_key = QtWidgets.QLineEdit(self.settings_form)
        self.led_api_key.setStyleSheet("background-color: #FFFFFF;\n"
"")
        self.led_api_key.setObjectName("led_api_key")
        self.verticalLayout_6.addWidget(self.led_api_key)
        self.chb_youtube_shorts = QtWidgets.QCheckBox(self.settings_form)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.chb_youtube_shorts.setFont(font)
        self.chb_youtube_shorts.setStyleSheet("background-color: #A061C1;")
        self.chb_youtube_shorts.setObjectName("chb_youtube_shorts")
        self.verticalLayout_6.addWidget(self.chb_youtube_shorts)
        self.btn_update_settings = QtWidgets.QPushButton(self.settings_form)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.btn_update_settings.setFont(font)
        self.btn_update_settings.setStyleSheet("")
        self.btn_update_settings.setObjectName("btn_update_settings")
        self.verticalLayout_6.addWidget(self.btn_update_settings)
        self.verticalLayout_5.addWidget(self.settings_form, 0, QtCore.Qt.AlignTop)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/настройки.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.settings_page, icon, "")
        self.add_channel_page = QtWidgets.QWidget()
        self.add_channel_page.setGeometry(QtCore.QRect(0, 0, 250, 415))
        self.add_channel_page.setStyleSheet("")
        self.add_channel_page.setObjectName("add_channel_page")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.add_channel_page)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.add_channel_form = QtWidgets.QFrame(self.add_channel_page)
        self.add_channel_form.setStyleSheet("*{\n"
"    background-color: #E2677B;\n"
"    border: 5px solid #E2677B ;\n"
"    border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: #FFFFFF;\n"
"    border: 5px solid #FFFFFF;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 5px solid #fc8383;\n"
"    background-color: #fc8383;\n"
"}\n"
"QPushButton:pressed {\n"
"    border: 5px solid #ff4545;;\n"
"    background-color: #ff4545;\n"
"}")
        self.add_channel_form.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.add_channel_form.setFrameShadow(QtWidgets.QFrame.Raised)
        self.add_channel_form.setObjectName("add_channel_form")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.add_channel_form)
        self.verticalLayout_9.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.led_add_channel = QtWidgets.QLineEdit(self.add_channel_form)
        self.led_add_channel.setStyleSheet("background-color: #FFFFFF;;")
        self.led_add_channel.setObjectName("led_add_channel")
        self.verticalLayout_9.addWidget(self.led_add_channel)
        self.btn_add_channel = QtWidgets.QPushButton(self.add_channel_form)
        self.btn_add_channel.setStyleSheet("")
        self.btn_add_channel.setObjectName("btn_add_channel")
        self.verticalLayout_9.addWidget(self.btn_add_channel)
        self.verticalLayout_7.addWidget(self.add_channel_form, 0, QtCore.Qt.AlignTop)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/плюс.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.add_channel_page, icon1, "")
        self.del_channel_page = QtWidgets.QWidget()
        self.del_channel_page.setGeometry(QtCore.QRect(0, 0, 250, 415))
        self.del_channel_page.setStyleSheet("")
        self.del_channel_page.setObjectName("del_channel_page")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.del_channel_page)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.del_channel_form = QtWidgets.QFrame(self.del_channel_page)
        self.del_channel_form.setStyleSheet("*{\n"
"    border: 5px solid #775DF0;\n"
"    background-color: #775DF0;\n"
"    border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: #FFFFFF;\n"
"    border: 5px solid #FFFFFF;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 5px solid #fc8383;\n"
"    background-color: #fc8383;\n"
"}\n"
"QPushButton:pressed {\n"
"    border: 5px solid #ff4545;;\n"
"    background-color: #ff4545;\n"
"}\n"
"")
        self.del_channel_form.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.del_channel_form.setFrameShadow(QtWidgets.QFrame.Raised)
        self.del_channel_form.setObjectName("del_channel_form")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.del_channel_form)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.led_del_channel = QtWidgets.QLineEdit(self.del_channel_form)
        self.led_del_channel.setStyleSheet("background-color: #FFFFFF;")
        self.led_del_channel.setText("")
        self.led_del_channel.setObjectName("led_del_channel")
        self.verticalLayout_10.addWidget(self.led_del_channel)
        self.btn_del_channel = QtWidgets.QPushButton(self.del_channel_form)
        self.btn_del_channel.setStyleSheet("")
        self.btn_del_channel.setObjectName("btn_del_channel")
        self.verticalLayout_10.addWidget(self.btn_del_channel)
        self.verticalLayout_8.addWidget(self.del_channel_form, 0, QtCore.Qt.AlignTop)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/минус.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBox.addItem(self.del_channel_page, icon2, "")
        self.verticalLayout_4.addWidget(self.toolBox)
        self.verticalLayout_3.addWidget(self.frame_tool_box)
        self.verticalLayout_2.addWidget(self.frame_left_menu, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout.addWidget(self.frame_left_menu_container)
        self.frame_main_widget = QtWidgets.QFrame(self.centralwidget)
        self.frame_main_widget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main_widget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main_widget.setObjectName("frame_main_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_main_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_header = QtWidgets.QFrame(self.frame_main_widget)
        self.frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_header.setObjectName("frame_header")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_header)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_btn_menu = QtWidgets.QFrame(self.frame_header)
        self.frame_btn_menu.setStyleSheet("QPushButton:hover {\n"
"    border-radius: 6px;\n"
"    background-color: #fc8383;\n"
"}\n"
"QPushButton:pressed {\n"
"    border-radius: 6px;\n"
"    background-color: #ff4545;\n"
"}")
        self.frame_btn_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_btn_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btn_menu.setObjectName("frame_btn_menu")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_btn_menu)
        self.horizontalLayout_5.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_menu = QtWidgets.QPushButton(self.frame_btn_menu)
        self.btn_menu.setStyleSheet("border-radius: 7px;")
        self.btn_menu.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/меню.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_menu.setIcon(icon3)
        self.btn_menu.setIconSize(QtCore.QSize(32, 32))
        self.btn_menu.setObjectName("btn_menu")
        self.horizontalLayout_5.addWidget(self.btn_menu, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_btn_menu)
        self.frame_search = QtWidgets.QFrame(self.frame_header)
        self.frame_search.setStyleSheet("QPushButton:hover {\n"
"    border-radius: 6px;\n"
"    background-color: #fc8383;\n"
"}\n"
"QPushButton:pressed {\n"
"    border-radius: 6px;\n"
"    background-color: #ff4545;\n"
"}")
        self.frame_search.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_search.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_search.setObjectName("frame_search")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_search)
        self.horizontalLayout_3.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.led_search = QtWidgets.QLineEdit(self.frame_search)
        self.led_search.setMinimumSize(QtCore.QSize(0, 30))
        self.led_search.setMaximumSize(QtCore.QSize(800, 16777215))
        self.led_search.setStyleSheet("border: 1px solid #000000;\n"
"border-radius: 9px;")
        self.led_search.setText("")
        self.led_search.setObjectName("led_search")
        self.horizontalLayout_3.addWidget(self.led_search)
        self.btn_search = QtWidgets.QPushButton(self.frame_search)
        self.btn_search.setMinimumSize(QtCore.QSize(50, 25))
        self.btn_search.setMaximumSize(QtCore.QSize(50, 16777215))
        self.btn_search.setStyleSheet("")
        self.btn_search.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/поиск.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_search.setIcon(icon4)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout_3.addWidget(self.btn_search, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout_2.addWidget(self.frame_search, 0, QtCore.Qt.AlignTop)
        self.frame_account_info = QtWidgets.QFrame(self.frame_header)
        self.frame_account_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_account_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_account_info.setObjectName("frame_account_info")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_account_info)
        self.horizontalLayout_4.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_account_info = QtWidgets.QLabel(self.frame_account_info)
        font = QtGui.QFont()
        font.setFamily("12px")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_account_info.setFont(font)
        self.lbl_account_info.setObjectName("lbl_account_info")
        self.horizontalLayout_4.addWidget(self.lbl_account_info, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_account_info, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.verticalLayout.addWidget(self.frame_header)
        self.frame_main_content = QtWidgets.QFrame(self.frame_main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_main_content.sizePolicy().hasHeightForWidth())
        self.frame_main_content.setSizePolicy(sizePolicy)
        self.frame_main_content.setStyleSheet("")
        self.frame_main_content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main_content.setObjectName("frame_main_content")
        self.verticalLayout.addWidget(self.frame_main_content)
        self.horizontalLayout.addWidget(self.frame_main_widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_app_name.setText(_translate("MainWindow", "GoodTube"))
        self.lbl_new_login.setText(_translate("MainWindow", "Новый логин"))
        self.led_login.setPlaceholderText(_translate("MainWindow", "Логин..."))
        self.lbl_new_api_key.setText(_translate("MainWindow", "Новый ключ API"))
        self.led_api_key.setPlaceholderText(_translate("MainWindow", "Ключ API..."))
        self.chb_youtube_shorts.setText(_translate("MainWindow", "Фильтровать Shorts"))
        self.btn_update_settings.setText(_translate("MainWindow", "Применить"))
        self.led_add_channel.setPlaceholderText(_translate("MainWindow", "url..."))
        self.btn_add_channel.setText(_translate("MainWindow", "Добавить канал"))
        self.led_del_channel.setPlaceholderText(_translate("MainWindow", "url..."))
        self.btn_del_channel.setText(_translate("MainWindow", "Удалить канал"))
        self.led_search.setPlaceholderText(_translate("MainWindow", "Поиск..."))
        self.lbl_account_info.setText(_translate("MainWindow", "Логин"))
import icons_rc
