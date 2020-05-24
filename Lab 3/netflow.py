import pandas as pd
import datetime
import matplotlib.pyplot as plt

class Record:
    def __init__(self, time_start, sourceAddress, destAddress, useBytes):
        self.ts = time_start
        self.sa = sourceAddress
        self.da = destAddress
        self.useBytes = useBytes

def getAllRecords(ipAddress):
    records = []
    data = pd.read_csv('data/nf.csv', low_memory=False)
    for itm in data.values:
        if itm[3] == ipAddress:
            records.append(Record(itm[0], itm[3], itm[4], itm[12]))
    return records

def calculateTraffic(ipAddress):
    records = getAllRecords(ipAddress)
    totalTraffic = 0
    for record in records:
        totalTraffic += record.useBytes
    return totalTraffic

def billing(ipAddress):
    totalTraffic = calculateTraffic(ipAddress)
    if totalTraffic <= 100:
        return totalTraffic * 0.5
    else:
        return totalTraffic * 1 - 100 * 0.5

def getData(ipAddress):
    records = getAllRecords(ipAddress)
    time = [record.ts for record in records]
    dataflow = [record.useBytes for record in records]
    return [time, dataflow]

def showGraphic(ipAddress):
    times, flow = getData(ipAddress)
    timesArr = [datetime.datetime.strptime(elem, '%Y-%m-%d %H:%M:%S') for elem in times]
    flowByTime = [sum(flow[:i+1]) for i in range(len(flow))]
    plt.plot(timesArr, flowByTime)
    plt.ylabel("Flow (Мб)")
    plt.xlabel('Time')
    plt.title('Diagram Netflow')
    plt.show()