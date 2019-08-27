#!/usr/bin/python3


import os

from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from search.const.FileConst import FileConst
from search.service.fileService import FileService


def getPng(filename, end):
    filename = filename.replace(".mp4", end)
    filename = filename.replace(".wmv", end)
    filename = filename.replace(".mkv", end)
    filename = filename.replace(".avi", end)
    return filename


class MainUI(QMainWindow):
    # 初始化 loadUI
    def __init__(self):
        super().__init__()
        self.tableData = QTableWidget()
        self.gridData = QWidget()
        self.infoData = QWidget()
        self.infoLayout = QHBoxLayout()
        self.initUI()

    # 定义全局变量
    dataList = []
    rootPath = ""
    fileTypes = []
    # 执行命令
    command = ""
    # 载入数据
    tableData = ""
    isTableData = 0
    isGridData = 1
    gridData = ""
    infoData = ""
    infoLayout = ""
    curFile = None
    # 默认勾选
    imageToggle = 0
    videoToggle = 1
    docsToggle = 0

    # 搜索文本框
    dirName = ""

    # 载入UI窗口
    def initUI(self):
        self.setWindowTitle("文件目录")
        self.resize(1400, 900)
        # 创建搜索按钮
        if self.dirName == "":
            self.dirName = QLineEdit()
        openFoler = QPushButton("点我")
        openFoler.clicked[bool].connect(self.openPath)
        okButton = QPushButton("搜索")
        okButton.clicked[bool].connect(self.clickSearchButton)

        openFile = QPushButton("打开文件")
        openFile.clicked[bool].connect(self.openFile)
        openDir = QPushButton("打开文件夹")
        openDir.clicked[bool].connect(self.openFile)

        # 单选框
        grid_layout = QRadioButton("网格", )
        if self.isGridData == 1:
            grid_layout.toggle()
        table_layout = QRadioButton("表格")
        if self.isTableData == 1:
            table_layout.toggle()
        grid_layout.clicked[bool].connect(self.chooseLayout)
        table_layout.clicked[bool].connect(self.chooseLayout)
        # 复选框
        image = QCheckBox("图片", self)
        image.stateChanged.connect(self.imageChoose)
        video = QCheckBox("视频", self)
        video.stateChanged.connect(self.videoChoose)
        docs = QCheckBox("文档", self)
        docs.stateChanged.connect(self.docsChoose)
        if self.imageToggle == 1:
            image.toggle()
        if self.videoToggle == 1:
            video.toggle()
        if self.docsToggle == 1:
            docs.toggle()
        # 创建左侧组件
        left_widget = QWidget()
        left_layout = QGridLayout()
        left_layout.addWidget(grid_layout, 0, 0)
        left_layout.addWidget(table_layout, 0, 1)
        left_layout.addWidget(image, 1, 0)
        left_layout.addWidget(video, 1, 1)
        left_layout.addWidget(docs, 1, 2)

        left_layout.addWidget(self.dirName, 2, 0, 1, 3)
        left_layout.addWidget(openFoler, 3, 0, 1, 1)
        left_layout.addWidget(okButton, 3, 1, 1, 1)
        left_layout.addWidget(QLabel(""), 4, 0, 3, 3)

        left_layout.addWidget(QLabel("演员"), 5, 0, 1, 1)
        self.curActress = QLineEdit()
        left_layout.addWidget(self.curActress, 5, 1, 1, 2)
        left_layout.addWidget(QLabel("番号"), 6, 0, 1, 1)
        self.curCode = QLineEdit()
        left_layout.addWidget(self.curCode, 6, 1, 1, 2)
        left_layout.addWidget(QLabel("标题"), 7, 0, 1, 3)
        self.curTitle = QTextEdit()
        self.curTitle.setMaximumHeight(40)
        left_layout.addWidget(self.curTitle, 8, 0, 1, 3)
        self.curPic = QLabel()
        left_layout.addWidget(self.curPic, 9, 0, 15, 3)
        left_layout.addWidget(openFile)
        left_layout.addWidget(openDir)

        # 创建右侧组件
        right_widget = QWidget()
        right_layout = QGridLayout()

        # loading 选择表格布局 还是 网格布局
        if self.isTableData == 1:
            right_layout.addWidget(self.loadTableData(), 0, 0, 1, 1)
        elif self.isGridData == 1:
            scroll = QScrollArea()
            scroll.setWidget(self.loadGridData())
            right_layout.addWidget(scroll, 0, 0, 1, 1)
        # 创建主窗口组件 挂载布局
        main_widget = QWidget()
        main_layout = QGridLayout()
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget, 0, 1, 1, 16)
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 0, 0, 1, 1)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        bar = self.menuBar()
        file = bar.addMenu("文件")
        file.setShortcutEnabled(1)
        qu = QAction("退出", self)
        qu.setShortcut("q")
        file.addAction(qu)
        file.triggered[QAction].connect(self.fileMenuProcess)
        self.show()

    def loadGridData(self):

        gridData = self.gridData
        if len(self.dataList) == 0:
            self.search("G:/emby/emby-rename")
        gridLayout = QGridLayout()
        for index in range(len(self.dataList)):
            data = self.dataList[index]
            item = QToolButton()
            item.setText(str(index))
            item.setIcon(QIcon(getPng(data.path, '.png')))
            item.setIconSize(QSize(200, 300))
            item.setToolButtonStyle(Qt.ToolButtonIconOnly)
            item.setToolTip(data.name)
            item.clicked[bool].connect(self.clickGrid)
            row = int(index / 4)
            cols = index % 4
            title = QTextEdit(data.name)
            title.setMaximumHeight(40)
            gridLayout.addWidget(item, row * 2, cols)
            gridLayout.addWidget(title, row * 2 + 1, cols)
        gridData.setLayout(gridLayout)
        return gridData

    # 填充数据
    def search(self, path):
        walk = FileService(path, self.fileTypes)
        self.dataList = []
        self.dataList = walk.getFiles()

    # 菜单按钮处理
    def fileMenuProcess(self, action):
        print(action.text())
        if action.text() == "退出":
            self.close()

    # 点击搜索
    def clickSearchButton(self):
        self.statusBar().showMessage('执行中')
        # 提示框测试
        # replay = QMessageBox.question(self, '提示',
        #                               self.dirName.text(), QMessageBox.Yes)
        # if replay == QMessageBox.Yes:
        self.search(self.dirName.text())
        message = '总数:' + str(len(self.dataList)) + '   执行完毕！！！'
        self.statusBar().showMessage(message)

        if self.isGridData == 1:
            self.loadGridData()
        if self.isTableData == 1:
            self.loadTableData()
        self.initUI()

    # 选择框
    def openPath(self):
        fname = QFileDialog.getExistingDirectory(self, "选择文件夹", "/")
        if not fname:
            QMessageBox().about(self, "提示", "打开文件失败，可能是文件内型错误")
        else:
            self.dirName.setText(fname)
        self.clickSearchButton()

    # 点击事件
    def openFile(self, event):
        choose = self.sender().text()
        if choose == '打开文件':
            command = '''start "" "''' + self.curFile.path + "\""
            os.system(command)
        if choose == '打开文件夹':
            command = '''start "" "''' + self.curFile.dirPath + "\""
            os.system(command)

    # 点击事件
    def clickLine(self, event):
        col = self.tableData.currentColumn()
        index = self.tableData.currentRow()
        self.curFile = self.dataList[index]
        self.infoToLeft()
        if col == 1 or col == 0:
            command = '''start "" "''' + self.curFile.path + "\""
            os.system(command)
        if col == 3 or col == 2:
            command = '''start "" "''' + self.curFile.dirPath + "\""
            os.system(command)

    def clickGrid(self):
        text = self.sender().text()
        self.curFile = self.dataList[int(text)]
        self.infoToLeft()

    def infoToLeft(self):
        targetFile = self.curFile
        self.curCode.setText(targetFile.code)
        self.curTitle.setText(targetFile.name)
        self.curActress.setText(targetFile.actress)
        pic = Image.open(getPng(targetFile.path, '.png'))
        pic = pic.resize((250, 400))
        self.curPic.setPixmap(pic.toqpixmap())
        # self.curPic.setMaximumWidth(250)
        # self.curPic.setMaximumHeight(400)

    # 载入数据 表格形式
    def loadTableData(self):
        data = self.tableData
        data.setRowCount(0)
        data.setColumnCount(0)
        if len(self.dataList) == 0:
            self.search(self.rootPath)
        data.setColumnCount(8)
        data.setRowCount(len(self.dataList))
        # 自适应列宽度
        # data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        data.setHorizontalHeaderLabels(['图片', '名称', "番号", "路径", "优优", "大小", "创建时间", "修改时间"])
        data.itemClicked.connect(self.clickLine)
        data.setColumnWidth(0, 200)
        data.setColumnWidth(1, 130)
        data.setColumnWidth(2, 100)
        for index in range(len(self.dataList)):
            data.setRowHeight(index, 300)
            file = self.dataList[index]
            row_id = index
            row_name = QLabel()
            path = getPng(file.path, ".png")
            if QPixmap(path).isNull():
                path = path.replace("png", "jpg")
            if QPixmap(path).isNull():
                imageArray = path.split(".")
                path = ""
                for index in range(len(imageArray)):
                    if index == len(imageArray) - 1:
                        path += "-poster.jpg"
                    elif index == len(imageArray) - 2:
                        path += imageArray[index]
                    else:
                        path += imageArray[index] + "."
                path = path.replace("png", "jpg")
            if not QPixmap(path).isNull():
                pic = QPixmap(path).scaled(200, 300)
                row_name.setPixmap(pic)
            data.setCellWidget(row_id, 0, row_name)
            data.setItem(row_id, 1, QTableWidgetItem(file.name))
            data.setItem(row_id, 2, QTableWidgetItem(file.code))
            data.setItem(row_id, 3, QTableWidgetItem(file.path))
            data.setItem(row_id, 4, QTableWidgetItem(file.actress))
            data.setItem(row_id, 5, QTableWidgetItem(file.size))
            data.setItem(row_id, 6, QTableWidgetItem(file.createTime))
            data.setItem(row_id, 7, QTableWidgetItem(file.modifyTime))

        return data

    # 选择布局
    def chooseLayout(self):
        button = self.sender().text()
        if button == '表格':
            self.isTableData = 1
            self.isGridData = 0
            self.loadTableData()
        if button == '网格':
            self.isTableData = 0
            self.isGridData = 1
        self.initUI()

    # 点击图片box
    def imageChoose(self, state):
        if state == Qt.Checked:
            self.imageToggle = 1
            if FileConst.JPG not in self.fileTypes:
                self.fileTypes.append(FileConst.JPG)
            if FileConst.GIF not in self.fileTypes:
                self.fileTypes.append(FileConst.GIF)
        else:
            self.imageToggle = 0
            if FileConst.JPG in self.fileTypes:
                self.fileTypes.remove(FileConst.JPG)
            if FileConst.GIF in self.fileTypes:
                self.fileTypes.remove(FileConst.GIF)

    # 点击视频box
    def videoChoose(self, state):
        if state == Qt.Checked:
            self.videoToggle = 1
            if FileConst.MP4 not in self.fileTypes:
                self.fileTypes.append(FileConst.MP4)
            if FileConst.WMV not in self.fileTypes:
                self.fileTypes.append(FileConst.WMV)
            if FileConst.MKV not in self.fileTypes:
                self.fileTypes.append(FileConst.MKV)
            if FileConst.AVI not in self.fileTypes:
                self.fileTypes.append(FileConst.AVI)

        else:
            self.videoToggle = 0
            if FileConst.MP4 in self.fileTypes:
                self.fileTypes.remove(FileConst.MP4)
            if FileConst.WMV in self.fileTypes:
                self.fileTypes.remove(FileConst.WMV)
            if FileConst.MKV in self.fileTypes:
                self.fileTypes.remove(FileConst.MKV)
            if FileConst.AVI in self.fileTypes:
                self.fileTypes.remove(FileConst.AVI)

    # 点击文档box
    def docsChoose(self, state):

        if state == Qt.Checked:
            self.docsToggle = 1
            if FileConst.XLSX not in self.fileTypes:
                self.fileTypes.append(FileConst.XLSX)
            if FileConst.TXT not in self.fileTypes:
                self.fileTypes.append(FileConst.TXT)

        else:
            self.docsToggle = 0
            if FileConst.XLSX in self.fileTypes:
                self.fileTypes.remove(FileConst.XLSX)
            if FileConst.TXT in self.fileTypes:
                self.fileTypes.remove(FileConst.TXT)
