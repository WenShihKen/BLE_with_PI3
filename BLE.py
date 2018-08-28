from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading
import time
import connectSql

file = open("address.txt","r")
address = []
device_name =[]
for line in file:
   temp_list = line.strip().split(" ")
   address.append(temp_list[0])
   device_name.append(temp_list[1])

receive_data = ""

def Send_Info(data, addr_index):
    
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    temp_list = data.strip().split(" ")
    temp = temp_list[0]
    hum = temp_list[1]
    ppm = temp_list[2]
    
    db = connectSql.Connect_To_CloudSQL("sensorData")
    cursor = db.cursor()
    
    sql_string = "insert into {}".format(device_name[addr_index])

    cursor.execute(sql_string + " (time_stamp, temperature, humidity, co2) values (%s,%s,%s,%s)"
                   ,(ts,temp,hum,ppm,))
    db.commit()

class NotificationDelegate(DefaultDelegate):

    def __init__(self, number):
        DefaultDelegate.__init__(self)
        self.number = number

    def handleNotification(self, cHandle, data):
        global receive_data
        if receive_data != "":
            receive_data = ""
        
        receive_data = str(data, encoding = "utf-8")

connections = []
connection_threads = []
scanner = Scanner(0)

class ConnectionHandlerThread (threading.Thread):
    def __init__(self, connection_index):
        threading.Thread.__init__(self)
        self.connection_index = connection_index

    def run(self):
        connection = connections[self.connection_index]
        connection.setDelegate(NotificationDelegate(self.connection_index))
        while True:
            try:
                connection.waitForNotifications(10)
                print(receive_data, connection.addr)
                Send_Info(receive_data, address.index(connection.addr))
            except Exception:
                pass
                

while True:
    try:
        print("Connected: " + str(len(connection_threads)))
        devices = scanner.scan(10)
        for d in devices:
            if d.addr in address:
                p = Peripheral(d)
                connections.append(p)
                t = ConnectionHandlerThread(len(connections)-1)
                t.start()
                connection_threads.append(t)
    except Exception:
        pass