import pandas

class Record:
    def __init__(self, detailArray):
        self.timestamp = detailArray[0]
        self.msidnOrigin = detailArray[1]
        self.msisdnDest = detailArray[2]
        self.callDuration = detailArray[3]
        self.smsNumber = detailArray[4]
    
    def smsTariffing(self):
        return max(0, self.smsNumber - 5) * 1

    def outgoingCallTariffing(self):
        return self.callDuration * 4

    def imcomingCallTariffing(self):
        return max(0, self.callDuration-5) * 1

    def toString(self):
        return '%s <> %s <> %s <> %d <> %d' % (self.timestamp, self.msidnOrigin, self.msisdnDest, self.callDuration, self.smsNumber)

def getRecords(telNum, data):
    originRecords = []
    destRecords = []
    
    for line in data:
        if str(line[1]) == telNum:
            originRecords.append(Record(line))
        elif str(line[2]) == telNum:
            destRecords.append(Record(line))
    
    return [originRecords, destRecords]

def tariffing(telNum, data):
    originRecords, destRecords = getRecords(telNum, data)

    smsBill = 0
    outgoingBill = 0
    incomingBill = 0
    for orgRc in originRecords:
        smsBill += orgRc.smsTariffing()
        outgoingBill += orgRc.outgoingCallTariffing()
    for dstRc in destRecords:
        incomingBill += dstRc.imcomingCallTariffing()

    return [smsBill, outgoingBill, incomingBill]

def getSmsAndCallingBill(telNum):
    dt = pandas.read_csv('data/cdr.csv')
    smsbill, outgoingBill, incomingBill = tariffing(telNum, dt.values)
    return [smsbill, outgoingBill + incomingBill]