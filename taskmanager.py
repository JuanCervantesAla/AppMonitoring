import sys
import psutil
import time
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLabel, QFrame, QListWidgetItem,  QVBoxLayout
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#Cervantes Juan
#3-3-2025

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Task Manager")
        self.setGeometry(100, 100, 1000, 550)  # Tamaño de la ventana

        #Timer to update
        self.processTimer = QTimer(self) #Creates an instances of the timer
        self.processTimer.timeout.connect(self.loadProcesses)#When reaches timeout it would load the processes
        self.processTimer.start(1000)#Start the timer at 500

        # Frame for the header
        self.headerFrame = QFrame(self)
        self.headerFrame.setGeometry(0, 0, 1000, 50)
        self.headerFrame.setStyleSheet("background-color: #222021;")

        #Frame for the timer
        self.listFrame = QFrame(self)
        self.listFrame.setGeometry(5, 55, 550, 450)
        self.listFrame.setStyleSheet("background-color: #1A1B2E; border-radius: 5px;")

        #Frame for the graphic cpu usage
        self.cpuFrame = QFrame(self)
        self.cpuFrame.setGeometry(585,55,190,205)
        self.cpuFrame.setStyleSheet("background-color: #1A1B2E; border-radius: 5px;")

        #Frame for the graphic net usage
        self.netFrame = QFrame(self)
        self.netFrame.setGeometry(585,300,190,205)
        self.netFrame.setStyleSheet("background-color: #1A1B2E; border-radius: 5px;")

        #Frame for the graphic ram usage
        self.ramFrame = QFrame(self)
        self.ramFrame.setGeometry(785,55,190,205)
        self.ramFrame.setStyleSheet("background-color: #1A1B2E; border-radius: 5px;")

        #Frame for the graphic disk usage
        self.diskFrame = QFrame(self)
        self.diskFrame.setGeometry(785,300,190,205)
        self.diskFrame.setStyleSheet("background-color: #1A1B2E; border-radius: 5px;")

        plt.rcParams['font.family'] = 'Consolas'  # Cambia la fuente a Arial
        plt.rcParams['font.size'] = 10 

        #CPU Chart
        self.figure, self.ax = plt.subplots()
        self.ax.set_facecolor("#1A1B2E")
        self.figure.set_facecolor("#1A1B2E")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('#1A1B2E')
        self.ax.spines['right'].set_color('#1A1B2E')
        self.ax.tick_params(axis='x', colors='#008f11')
        self.ax.tick_params(axis='y', colors='#008f11')
        self.canvas = FigureCanvas(self.figure)

        #RAM Chart
        self.figureRam, self.axRam = plt.subplots()
        self.axRam.set_facecolor("#1A1B2E")
        self.figureRam.set_facecolor("#1A1B2E")
        self.axRam.spines['bottom'].set_color('white')
        self.axRam.spines['left'].set_color('white')
        self.axRam.spines['left'].set_color('white')
        self.axRam.spines['top'].set_color('#1A1B2E')
        self.axRam.spines['right'].set_color('#1A1B2E')
        self.axRam.tick_params(axis='x', colors='#008f11')
        self.axRam.tick_params(axis='y', colors='#008f11')
        self.canvasRam = FigureCanvas(self.figureRam)

        #Disk Chart
        self.figureDisk, self.axDisk = plt.subplots()
        self.axDisk.set_facecolor("#1A1B2E")
        self.figureDisk.set_facecolor("#1A1B2E")
        self.axDisk.spines['bottom'].set_color('white')
        self.axDisk.spines['left'].set_color('white')
        self.axDisk.spines['left'].set_color('white')
        self.axDisk.spines['top'].set_color('#1A1B2E')
        self.axDisk.spines['right'].set_color('#1A1B2E')
        self.axDisk.tick_params(axis='x', colors='#008f11')
        self.axDisk.tick_params(axis='y', colors='#008f11')
        self.canvasDisk = FigureCanvas(self.figureDisk)

        #Net Chart
        self.figureNet, self.axNet = plt.subplots()
        self.axNet.set_facecolor("#1A1B2E")
        self.figureNet.set_facecolor("#1A1B2E")
        self.axNet.spines['bottom'].set_color('white')
        self.axNet.spines['left'].set_color('white')
        self.axNet.spines['left'].set_color('white')
        self.axNet.spines['top'].set_color('#1A1B2E')
        self.axNet.spines['right'].set_color('#1A1B2E')
        self.axNet.tick_params(axis='x', colors='#008f11')
        self.axNet.tick_params(axis='y', colors='#008f11')
        self.canvasNet = FigureCanvas(self.figureNet)

        #Layout
        layout = QVBoxLayout(self.cpuFrame)
        layout.addWidget(self.canvas)

        #RAMLayout
        layout = QVBoxLayout(self.ramFrame)
        layout.addWidget(self.canvasRam)

        #DiskLayout
        layout = QVBoxLayout(self.diskFrame)
        layout.addWidget(self.canvasDisk)

        #NetLayout
        layout = QVBoxLayout(self.netFrame)
        layout.addWidget(self.canvasNet)

        #Get the cpu%
        self.cpuData = [0] * 60 #Last cpu values
        self.xData = list(range(60))#60 Seconds

        #Get the disk values
        self.diskData = [0] * 60
        self.xDiskData = list(range(60))

        #Get Ram values
        self.ramData = [0] * 60
        self.xRamData = list(range(60))

        #Get Ram values
        self.netData = [0] * 60
        self.xNetData = list(range(60))

        #CPU Timer and disk timer
        self.cpuTimer = QTimer(self)
        self.cpuTimer.timeout.connect(self.updateGraph)
        self.cpuTimer.start(1000)
        
        #App title
        self.title = QLabel("COMPUSTATS", self.headerFrame)
        self.title.setGeometry(20, 10, 300, 30)
        self.title.setStyleSheet("font: bold 26px 'Consolas'; color: white;")

        # Processes List and their titles
        self.systemProcessList = QListWidget(self)
        self.systemProcessList.setGeometry(10, 80, 540, 180)

        self.userProcessList = QListWidget(self)
        self.userProcessList.setGeometry(10, 290, 540, 210)

        self.listTitleSystem = QLabel("System Processes", self)
        self.listTitleSystem.setGeometry(10, 60, 300, 20)
        self.listTitleSystem.setStyleSheet("font: bold 14px 'Consolas'; color: white; background: #1A1B2E;")

        self.listTitleUser = QLabel("User Processes", self)
        self.listTitleUser.setGeometry(10, 270, 300, 20)
        self.listTitleUser.setStyleSheet("font: bold 14px 'Consolas'; color: white; background: #1A1B2E;")

        # Buttons
        # self.refreshButton = QPushButton("Update", self)
        # self.refreshButton.setGeometry(640, 500, 120, 40)
        self.killButton = QPushButton("End process", self)
        self.killButton.setGeometry(80, 510, 400, 25)

        #On click events
        # self.refreshButton.clicked.connect(self.loadProcesses)
        self.killButton.clicked.connect(self.killProcess)

        ######################################STYLES#####################################
        self.setStyleSheet("""
            QWidget {
                background-color: #0D0D1E;
                color: #fff;
            }
            QPushButton {
                background: #007ACC;
                border-radius: 5px;
                padding: 8px;
                color: #fff;
            }
            QPushButton:hover {
                background: #005f9e;
            }
            QListWidget {
                background: #1A1B2E;
                border-radius: 5px;
                border: 1px solid #fff;
                padding: 5px;
                font: 14px 'Consolas';
                color: #E0E0E0;
            }
            QListWidget::item{
                background: #1A1B2E;
                padding: 8px;
                margin: 5px;
                border-radius: 5px;
            }
            QListWidget::item:selected{
                background:#007ACC;
                color: #fff;
                font-weight: bold;
                border: 2px solid #005F9E;
            }
            QScrollBar:vertical {
                border: none;
                background: #ded232;
                width: 10px;
                margin: 5px 5px 5px 5px;
            }
            QScrollBar::handle:vertical {
                background: #007ACC;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #005F9E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }

        """)

        self.loadProcesses()

    ################################LOAD AN RETRIEVE METHODS#########################

    def loadProcesses(self):

        self.systemProcessList.setUpdatesEnabled(False)
        self.userProcessList.setUpdatesEnabled(False)#Set updates not enable

        self.systemProcessList.clear()#Clears the list everytime it updates itself
        self.userProcessList.clear()

        for proc in psutil.process_iter(['pid', 'name', 'username']):#Loop to take the processes info every time
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                user = proc.info['username']

                process = psutil.Process(pid)#Process info like cpu usage and memory usage
                cpu_usage = process.cpu_percent(interval=None)
                mem_usage = process.memory_percent()

                item_text = f"{name} (PID: {pid}) | CPU: {cpu_usage:.1f}% | RAM: {mem_usage:.1f}%"
                item = QListWidgetItem(item_text)

                if user is not None and ("system" in user.lower() or "local service" in user.lower()):
                    self.systemProcessList.addItem(item)
                else:
                    self.userProcessList.addItem(item)
            except Exception as e:
                print(f"Error loading process {proc.info['name']}: {e}")
        
        self.systemProcessList.setUpdatesEnabled(True)
        self.userProcessList.setUpdatesEnabled(True)#Set updates True



    def killProcess(self):#Stop the process
        selectedItem = self.systemProcessList.currentItem() or self.userProcessList.currentItem()
        if selectedItem:#If Selelected item
            try:
                pid = int(selectedItem.text().split("(PID: ")[1].split(")")[0])
                psutil.Process(pid).terminate()#Terminates the process
                self.loadProcesses()
            except Exception as e:#Throws an exception if needed
                print(f"Error: {e}")

    @staticmethod
    def get_network_usage(interval=1, max_bandwidth=100_000_000):  # max_bandwidth en bits (100 Mbps por defecto)
        net1 = psutil.net_io_counters()
        time.sleep(interval)
        net2 = psutil.net_io_counters()

        # Bytes transferidos en el intervalo
        bytes_sent = net2.bytes_sent - net1.bytes_sent
        bytes_recv = net2.bytes_recv - net1.bytes_recv
        total_bytes = bytes_sent + bytes_recv  # Total de bytes transmitidos y recibidos

        # Convertimos a bits por segundo
        bandwidth_used = total_bytes * 8  # Bytes a bits

        # Calculamos el porcentaje de uso basado en el ancho de banda máximo
        usage_percent = (bandwidth_used / (max_bandwidth * interval)) * 100

        return usage_percent
    
    def updateGraph(self):
        self.cpuData.append(psutil.cpu_percent())  # Obtener uso de CPU
        self.cpuData.pop(0)  # Mantener solo 60 valores

        #Disk value
        diskInfo = psutil.disk_usage('/')
        self.diskData.append(diskInfo.percent)
        self.diskData.pop(0)

        #RAM Value
        ramInfo = psutil.virtual_memory()
        self.ramData.append(ramInfo.percent)
        self.ramData.pop(0)

        #Net value

        netInfo = self.get_network_usage(1)
        self.netData.append(netInfo)
        self.netData.pop(0)

        self.ax.clear()  # Limpiar la gráfica
        self.ax.plot(self.xData, self.cpuData, linestyle='--', color='g', label="CPU Usage (%)")
        self.ax.set_ylim(0, 100)
        self.ax.set_title("CPU Usage",color="white")
        self.ax.legend()

        self.axDisk.clear()
        self.axDisk.plot(self.xDiskData,self.diskData, linestyle='--',color='g',label="Disk Usage(%)")
        self.axDisk.set_ylim(0,100)
        self.axDisk.set_title("Disk usage",color="white")
        self.axDisk.legend()

        self.axRam.clear()
        self.axRam.plot(self.xDiskData,self.diskData, linestyle='--',color='g',label="Ram Usage(%)")
        self.axRam.set_ylim(0,100)
        self.axRam.set_title("Ram usage",color="white")
        self.axRam.legend()

        self.axNet.clear()
        self.axNet.plot(self.xDiskData,self.diskData, linestyle='--',color='g',label="Net Usage(%)")
        self.axNet.set_ylim(0,100)
        self.axNet.set_title("Net usage", color="white")
        self.axNet.legend()

        self.canvas.draw()  # Redibujar la gráfica
        self.canvasDisk.draw()
        self.canvasRam.draw()
        self.canvasNet.draw()

app = QApplication(sys.argv)
window = TaskManager()
window.show()
sys.exit(app.exec())
