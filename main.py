import os
import time
import requests
import apimoex
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
import sys
import plotly.io as pio
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import shutil
from db import DB

# DB = DB("gg.db")
START_DATE = []
END_DATE = []
SECURITY_LIST = []
DATA_PATH = "loaded_data/"
INTERVAL = 24
pio.templates.default = "plotly_dark"
dz = pd.DataFrame(apimoex.get_board_securities(session=requests.Session(), table='securities', columns=None))
table_dz = dz[['SECID', 'SHORTNAME', 'LOTSIZE', 'FACEVALUE', 'FACEUNIT', 'PREVPRICE']]


class MainWindow(QMainWindow):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Import currencies")
        Dialog.resize(1650, 700)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 10, 281, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.currencyInput = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.currencyInput.setCurrentText("")
        self.currencyInput.setObjectName("currencyInput")
        self.verticalLayout.addWidget(self.currencyInput)
        self.dateStart = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget)
        self.dateStart.setObjectName("dateStart")
        self.verticalLayout.addWidget(self.dateStart)
        self.dateEnd = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget)
        self.dateEnd.setObjectName("dateEnd")
        currentTime = QDateTime.currentDateTime()
        self.dateStart.setDateTime(currentTime.addDays(-30))
        self.dateEnd.setDateTime(currentTime)
        self.verticalLayout.addWidget(self.dateEnd)
        self.typeGraph = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.typeGraph.setCurrentText("")
        self.typeGraph.setObjectName("typeGraph")
        self.verticalLayout.addWidget(self.typeGraph)
        self.buttonImport = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonImport.setObjectName("buttonImport")
        self.verticalLayout.addWidget(self.buttonImport)
        self.buttonReset = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonReset.setObjectName("buttonReset")
        self.verticalLayout.addWidget(self.buttonReset)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 126, 161))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(440, 10, 1200, 600))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.labelImage = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.labelImage.setContentsMargins(0, 0, 0, 0)
        self.labelImage.setObjectName("labelImage")
        self.lbl = QLabel(self)
        self.typeGraph.addItem("scatter")
        self.typeGraph.addItem("bar")
        self.typeGraph.addItem("linear")
        self.typeGraph.addItem("boxplot")

        for curr in table_dz['SECID']:
            self.currencyInput.addItem(curr)

        self.labelImage.addWidget(self.lbl)
        self.buttonReset.clicked.connect(self.reset)
        self.buttonImport.clicked.connect(self.Import)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.buttonImport.setText(_translate("Dialog", "Import"))
        self.buttonReset.setText(_translate("Dialog", "Reset"))
        self.label.setText(_translate("Dialog", "Select currency:"))
        self.label_2.setText(_translate("Dialog", "Start date:"))
        self.label_3.setText(_translate("Dialog", "End date:"))
        self.label_4.setText(_translate("Dialog", "Type of graph:"))

    def Import(self):
        print("import")
        start = self.dateStart.text().split('.')[2].split(' ')[0] + '-' + self.dateStart.text().split('.')[1] + '-' + \
                self.dateStart.text().split('.')[0]
        end = self.dateEnd.text().split('.')[2].split(' ')[0] + '-' + self.dateEnd.text().split('.')[1] + '-' + \
              self.dateEnd.text().split('.')[0]
        ticket = self.currencyInput.currentText()
        dates(start, end, ticket)
        time.sleep(10)
        graphs()
        time.sleep(10)
        self.pixmap = QPixmap(f"images/{self.typeGraph.currentText()}.png")
        self.lbl.setPixmap(self.pixmap)
        path = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'images')
        shutil.rmtree(path)

    def reset(self):
        print("reset")
        currentTime = QDateTime.currentDateTime()
        self.dateStart.setDateTime(currentTime.addDays(-30))
        self.dateEnd.setDateTime(currentTime)


class DataManager:
    @staticmethod
    def update_data(
            ticket_list,
            start_date,
            end_date,
            interval,
            path,
    ) -> None:
        for security in ticket_list:
            with requests.Session() as session:
                data = apimoex.get_market_candles(
                    session,
                    security=security,
                    start=start_date,
                    interval=interval,
                    end=end_date,
                )
                whole_frame = pd.DataFrame(data)
                date, close = whole_frame["begin"], whole_frame["close"]
                attr = {"begin": date, "close": close}
                whole_frame = pd.DataFrame(attr)
                path1 = "images/"
                if not os.path.exists(path):
                    os.mkdir(path)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                whole_frame.to_csv(path + security + ".csv")

    def __init__(self, path, start_data, end_data):
        self._path_to_data = path
        self._ticket_list = list(
            map(lambda x: x.split(".")[0], os.listdir(DATA_PATH))
        )
        self.start_date = start_data
        self.end_date = end_data

    @property
    def ticket_list(self) -> list:
        return self._ticket_list

    def give_data(self, ticket: str) -> tuple:
        with open(self._path_to_data + ticket + ".csv", newline="") as csvfile:
            content = pd.read_csv(csvfile)
            values = content.loc[
                (content["begin"] >= self.start_date)
                & (content["begin"] <= self.end_date)
                ]
            x_axis, y_axis = values["begin"], values["close"]
            return x_axis, y_axis


def dates(start, end, ticket):
    SECURITY_LIST.append(ticket)
    START_DATE.append(start)
    END_DATE.append(end)
    # DB.create_table_all_secid(ticket)


def graphs():
    DataManager.update_data(SECURITY_LIST, START_DATE[-1], END_DATE[-1], INTERVAL, DATA_PATH)
    data_manager = DataManager(DATA_PATH, START_DATE[-1], END_DATE[-1])
    SECURITY_LIST.clear()
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    fig1, ax1 = plt.subplots(figsize=(20, 10))
    fig2, ax2 = plt.subplots(figsize=(20, 10))
    fig3, ax3 = plt.subplots(figsize=(20, 10))
    columns = []
    for ticket in data_manager.ticket_list:
        dates, values = data_manager.give_data(ticket)
    columns += [values]
    list1 = []
    # for i in range(0, len(dates)):
        # DB.add_secid(ticket, ticket, values[i], dates[i][:-9])
    date1 = dates[0][:-9]
    date2 = dates[len(dates) - 1][:-9]
    normalisedate1 = int(date1.replace("-", ""))
    normalisedate2 = int(date2.replace("-", ""))
    try:
        new_value = []
        new_date = []
        if (normalisedate2 - normalisedate1 > 31000):
            for i in range(0, len(dates)):
                dates[i] = dates[i][:4]

            sum = 0
            count = 0
            for i in range(len(dates)):
                try:
                    if dates[i] == dates[i + 1]:
                        count += 1
                        sum += values[i]
                    else:
                        count += 1
                        sum += values[i]
                        new_value.append(sum / count)
                        count = 0
                        sum = 0
                        new_date.append(dates[i])
                except:
                    pass
            new_date.append(dates[len(dates) - 1])
            new_value.append(sum / count)
            dates = new_date
            values = new_value
        elif (normalisedate2 - normalisedate1 > 400 and normalisedate2 - normalisedate1 < 31000):
            for i in range(0, len(dates)):
                dates[i] = dates[i][:7]
            sum = 0
            count = 0
            for i in range(len(dates)):
                try:
                    if dates[i] == dates[i + 1]:
                        count += 1
                        sum += values[i]
                    else:
                        count += 1
                        sum += values[i]
                        new_value.append(sum / count)
                        count = 0
                        sum = 0
                        new_date.append(dates[i])
                except:
                    pass
            new_date.append(dates[len(dates) - 1])
            new_value.append(sum / count)
            dates = new_date
            values = new_value
        else:
            for i in range(0, len(dates)):
                dates[i] = dates[i][:10]
    except:
        pass

    for i in range(0, len(dates)):
        list1.append((dates[i], values[i]))
    indices = np.arange(len(list1))

    plt.title('Scatter Data')
    ax3.bar(indices, values, label=ticket, alpha=0.5)
    plt.xticks(indices, dates, rotation='vertical')
    plt.tight_layout()

    plt.title('Scatter Data')
    fig.autofmt_xdate(rotation=45)

    ax.scatter(x=dates, y=values, label=ticket)
    plt.title('Bar Data')

    ax2.plot(dates, values, label=ticket)
    fig2.autofmt_xdate(rotation=45)

    pos = np.arange(len(columns)) + 1
    bp = ax1.boxplot(columns, sym='k+', positions=pos, notch=1, bootstrap=5000)
    patch = mpatches.Patch(color='black', label=data_manager.ticket_list)

    ax1.legend(handles=[patch])
    ax2.legend(loc='upper left')
    ax.legend(loc='upper left')
    ax3.legend(loc='upper left')
    fig.savefig("images/scatter.png", dpi=60)
    fig3.savefig("images/bar.png", dpi=60)
    fig2.savefig("images/linear.png", dpi=60)
    fig1.savefig("images/boxplot.png", dpi=60)
    path = os.path.join(os.path.dirname(os.path.abspath("__file__")), 'loaded_data')
    shutil.rmtree(path)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MainWindow()
    ui.setupUi(Dialog)
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("./1.jpg")))
    Dialog.setPalette(palette)
    Dialog.show()
    sys.exit(app.exec_())