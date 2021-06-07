import serial
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("Light Control System | Diploma of Andrii Bondariev ACTSI-17-3")

ser = serial.Serial("COM7", 9600, timeout = 1)
serial = QSerialPort()
serial.setBaudRate(96000)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.description())
ui.comL.addItems(portList)


def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    print(data)


def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)
    ser.write(b'1')
    data = ser.readline().decode('ascii')
    return data

def serialSend(data):
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())

def onClose():
    #serial.close()
    ser.write(b'0')
    data = ser.readline().decode('ascii')
    return data

def ledControl(val):
    if val == 2: val = 1;
    serialSend([13, val])


ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.ledC.stateChanged.connect(ledControl)

ui.show()
app.exec()
