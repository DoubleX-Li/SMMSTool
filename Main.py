import os
import sys
from tkinter import Tk

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QWidget

from SMMSTool import SMMSTool, ImageUrl


class SMMSToolGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tool = SMMSTool()
        self.hasResult = False
        self.uploadList = []

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        self.dragArea = QTextEdit()

        self.fileinfo = QLineEdit()
        self.removeBtn = QPushButton("Remove")
        self.removeBtn.clicked.connect(self.clearUploadList)
        self.removeBtn.hide()
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.upload)
        self.uploadBtn.hide()
        self.browseBtn = QPushButton("Browse...")
        self.browseBtn.clicked.connect(self.browse)

        self.label = QLabel()
        self.getUrl = QRadioButton("url")
        self.getUrl.clicked.connect(self.showUrl)
        self.getMarkdown = QRadioButton("markdown")
        self.getMarkdown.clicked.connect(self.showUrl)
        self.getDelete = QRadioButton("delete")
        self.getDelete.clicked.connect(self.showUrl)
        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(self.getUrl)
        self.radioGroup.addButton(self.getMarkdown)
        self.radioGroup.addButton(self.getDelete)

        self.list = QListWidget()
        self.list.itemClicked.connect(self.copyToClipboard)

        grid.addWidget(self.dragArea, 1, 0, 1, 4)
        grid.addWidget(self.fileinfo, 2, 0)
        grid.addWidget(self.removeBtn, 2, 1)
        grid.addWidget(self.uploadBtn, 2, 2)
        grid.addWidget(self.browseBtn, 2, 3)
        grid.addWidget(self.label, 3, 0, 1, 4)
        grid.addWidget(self.getUrl, 4, 0)
        grid.addWidget(self.getMarkdown, 4, 1)
        grid.addWidget(self.getDelete, 4, 2)
        grid.addWidget(self.list, 5, 0, 1, 4)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 300)
        self.center()
        self.setWindowTitle('SMMSToolGUI')

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '警告', "是否要退出?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileIsImage(self, filepath):
        imageExtension = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        inputExtension = os.path.splitext(filepath)[1]
        if inputExtension in imageExtension:
            return True
        else:
            return False

    def upload(self):
        print("待传图片有" + len(self.uploadList).__str__())
        for filepath in self.uploadList:
            print("正在处理uploadList")
            if os.path.isfile(filepath):
                if self.fileIsImage(filepath):
                    uploadStatus, uploadMsg = self.tool.upload(filepath)
                    if uploadStatus == -1 or -2:
                        print("Status:")
                        print(uploadStatus)
                    elif uploadStatus == 0:
                        print("Status:")
                        print(uploadStatus)
                        print("上传成功时查看信息")
                        self.tool.outputInfo()
                else:
                    print("不是图片")
            else:
                print("不是文件")
        self.label.setText("上传成功")
        self.hasResult = True

    def clearUploadList(self):
        self.uploadList = []
        self.refreshFileInfo()
        self.hideBtn()

    def refreshFileInfo(self):
        if len(self.uploadList) == 0:
            self.fileinfo.setText('')
        elif len(self.uploadList) == 1:
            self.fileinfo.setText(self.uploadList[0])
        else:
            self.fileinfo.setText("选择了" + len(self.uploadList).__str__() + "个文件")

    def hideBtn(self):
        self.removeBtn.hide()
        self.uploadBtn.hide()

    def showBtn(self):
        self.removeBtn.show()
        self.uploadBtn.show()

    def browse(self):
        filepaths = QFileDialog.getOpenFileNames(self, "选择文件", "C:/")[0]
        for filepath in filepaths:
            self.uploadList.append(filepath)
        self.showBtn()
        self.refreshFileInfo()

    def showUrl(self):
        # self.hasResult = True
        # self.tool.urlList = [ImageUrl('test1.jpg', 'https://test1.jpg', 'https://deletetest1.jpg'),
        #                      ImageUrl('test2.jpg', 'https://test2.jpg', 'https://deletetest2.jpg'),
        #                      ImageUrl('test3.jpg', 'https://test3.jpg', 'https://deletetest3.jpg'), ]

        if self.hasResult:
            self.list.clear()
            sender = self.sender()

            if sender.text() == 'url':
                for url in self.tool.urlList:
                    self.list.addItem(QListWidgetItem(url.url))
            elif sender.text() == 'markdown':
                for url in self.tool.urlList:
                    self.list.addItem(QListWidgetItem("![" + url.name + "](" + url.url + ")"))
            elif sender.text() == 'delete':
                for url in self.tool.urlList:
                    self.list.addItem(QListWidgetItem(url.delete))
        else:
            QMessageBox.question(self, "警告", "不存在结果", QMessageBox.Yes, QMessageBox.Yes)

    def copyToClipboard(self, item):
        print(item.text())
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(item.text())
        r.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    smmsToolGUI = SMMSToolGUI()
    sys.exit(app.exec_())