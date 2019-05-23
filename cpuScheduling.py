from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.font_manager as font_manager

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banker's")
        self.setGeometry(500,40,300, 650)


        # Creation of figure and canvas
        #self.figure = plt.figure()
        #self.canvas = FigureCanvas(self.figure)
        #self.ax = self.figure.add_subplot(111)
        #self.ax.axis('OFF')
        #self.line, = self.ax.plot([])
        #self.ax.axis([0,50,0,100])

        #self.toolbar = NavigationToolbar(self.canvas, self)
        #self.plot_widget = QWidget(self)
        #self.plot_widget.setGeometry(250, 10, 1100, 600)
        #plot_box = QVBoxLayout()
        #plot_box.addWidget(self.canvas)
        #self.plot_widget.setLayout(plot_box)

        self.label1=QLabel("no of processes",self)
        self.label1.move(30,60)
        self.label2 = QLabel("no of resources", self)
        self.label2.move(30, 100)
        self.label2 = QLabel("max resources", self)
        self.label2.move(30, 140)

        self.lineEdit1=QLineEdit(self)
        self.lineEdit1.move(120,60)
        self.lineEdit1.setText("5")
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.move(120, 100)
        self.lineEdit2.setText("4")
        self.lineEdit3 = QLineEdit(self)
        self.lineEdit3.move(120, 140)
        self.lineEdit3.setText("8 5 9 7")

        #self.combo = QComboBox(self)
        #self.combo.move(85, 300)
        #self.combo.addItems(["ROUND ROBIN", "SJF-PE", "SJF-NP", "FCFS", "PRIORITY"])


        self.button = QPushButton('Set Values', self)
        self.button.clicked.connect(self.trial)
        self.button.move(85, 490)
        #self.button = QPushButton('Draw', self)
        #self.button.clicked.connect(self.trial)
        #self.button.move(85, 520)
        self.button = QPushButton('Done', self)
        self.button.clicked.connect(self.window2)
        self.button.move(85, 550)



        #self.label4 = QLabel("priority", self)
        #self.label4.move(30, 180)
        #self.lineEdit4 = QLineEdit(self)
        #self.lineEdit4.move(120, 180)
        #self.lineEdit4.setText("1 2 3")
        #self.label5 = QLabel("queue", self)
        #self.label5.move(30, 220)
        #self.lineEdit5 = QLineEdit(self)
        #self.lineEdit5.move(120, 220)
        #self.lineEdit5.setText("3")




        self.show()




    def trial(self):
        global no
        global nor
        global maxr
        global now
        global strings1
        global strings2
        strings1=list()
        strings2=list()



        now=1

        no=int(self.lineEdit1.text())

        nor = int(self.lineEdit2.text())

        maxr = str(self.lineEdit3.text())

        for x in range(0,no):
            self.getText1()
            self.getText2()

            print(strings1[now-1]+"\n"+strings2[now-1]+"\n"+str(now+1))

            now += 1



    def getText1(self):

      global now
      global strings1
      text, okPressed = QInputDialog.getText(self, "Allocated rescources", "process"+str(now), QLineEdit.Normal, "")
      strings1.append(text)


    def getText2(self):

      global now
      global strings2
      text, okPressed = QInputDialog.getText(self, "Max rescources", "process"+str(now), QLineEdit.Normal, "")
      strings2.append(text)



    def reset(self):
        self.ax.clear()
        self.ax.axes.get_yaxis().set_visible(False)
        plt.box(False)
        ax = self.figure.add_subplot(111)
        self.ax.axis([0, 50, 0, 100])
        self.ax.axis('OFF')
        self.canvas.draw()

    def window2(self):                                             # <===
        self.w = Window2()
        self.w.show()
        self.hide()
        self.w.main()



class Window2(QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window22222")
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.browser=QTextBrowser()

        vbox=QVBoxLayout()
        vbox.addWidget(self.browser)

        self.setLayout(vbox)

    def main(self):

        global no
        global nor
        global maxr
        global now
        global strings1
        global strings2
        processes = no
        resources = nor
        max_resources = [int(i) for i in maxr.split()]



        currently_allocated = [[int(i) for i in strings1[j].split()] for j in range(processes)]

        max_need = [[int(i) for i in strings2[j].split()] for j in range(processes)]

        allocated = [0] * resources
        for i in range(processes):
            for j in range(resources):
                allocated[j] += currently_allocated[i][j]
        self.browser.append(f"\ntotal allocated resources : {allocated}")


        available = [max_resources[i] - allocated[i] for i in range(resources)]
        self.browser.append(f"total available resources : {available}\n")

        running = [True] * processes
        count = processes
        while count != 0:
            safe = False
            for i in range(processes):
                if running[i]:
                    executing = True
                    for j in range(resources):
                        if max_need[i][j] - currently_allocated[i][j] > available[j]:
                            executing = False
                            break
                    if executing:
                        self.browser.append(f"process {i + 1} is executing")
                        running[i] = False
                        count -= 1
                        safe = True
                        for j in range(resources):
                            available[j] += currently_allocated[i][j]
                        break
            if not safe:
                self.browser.append("the processes are in an unsafe state.")
                break

            self.browser.append(f"the process is in a safe state.\navailable resources : {available}\n")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    app.exec_()


def main():
    global no
    global nor
    global maxr
    global now
    global strings1
    global strings2
    processes = no
    resources = nor
    max_resources = [int(i) for i in maxr.split()]

    print("\n-- allocated resources for each process --")
    currently_allocated = [[int(i) for i in strings1[j].split()] for j in range(processes)]

    print("\n-- maximum resources for each process --")
    max_need = [[int(i) for i in strings2[j].split()] for j in range(processes)]

    allocated = [0] * resources
    for i in range(processes):
        for j in range(resources):
            allocated[j] += currently_allocated[i][j]
    print(f"\ntotal allocated resources : {allocated}")

    available = [max_resources[i] - allocated[i] for i in range(resources)]
    print(f"total available resources : {available}\n")

    running = [True] * processes
    count = processes
    while count != 0:
        safe = False
        for i in  range(processes):
            if running[i]:
                executing = True
                for j in range(resources):
                    if max_need[i][j] - currently_allocated[i][j] > available[j]:
                        executing = False
                        break
                if executing:
                    print(f"process {i + 1} is executing")
                    running[i] = False
                    count -= 1
                    safe = True
                    for j in range(resources):
                        available[j] += currently_allocated[i][j]
                    break
        if not safe:
            print("the processes are in an unsafe state.")
            break

        print(f"the process is in a safe state.\navailable resources : {available}\n")


#if __name__ == '__main__':
 #main()
