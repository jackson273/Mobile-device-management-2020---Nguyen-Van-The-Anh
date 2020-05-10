from traffic import *

def traffic(ipAddress):
    res = calculateTraffic(ipAddress)
    print('Flow: %.2fMB' % res)

def showBill(ipAddress):
    res = billing(ipAddress)
    print('Bill: %.2f$' % res)

def createStatistic(ipAddress):
    showGraphic(ipAddress)