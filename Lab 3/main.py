from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
from constants import *
import cdr, netflow as nf
from docx2pdf import convert
import os

phoneNumber = input('Enter phone number: ')
ipAddress = input('Enter IP address: ')

template = "templete/invoice.docx"

document = MailMerge(template)

# Chen thong tin ngan hang
document.merge(
    bank_name = BANK_NAME,
    bik_number = BIK_NUMBER,
    bank_account_number = BANK_ACCOUNT_NUMBER
)

# Chen thong tin nha cung cap dich vu
document.merge(
    inn_number = INN_NUMBER,
    kpp_number = KPP_NUMBER,
    client_name = CLIENT_NAME,
    provider_account_number = PROVIDER_ACCOUNT_NUMBER
)

# Chen thong tin hoa don
document.merge(
    payment_number = str(PAYMENT_NUMBER),
    payment_date = date.today().strftime("%d-%m-%Y"),
    provider_details = PROVIDER_DETAILS,
    client_details = CLIENT_DETAILS
)

# Chen thong tin dich vu
total_cdr = sum(cdr.getSmsAndCallingBill(phoneNumber))
amount_netflow = nf.calculateTraffic(ipAddress)
total_netflow = nf.billing(ipAddress)
servicesList = [
    {
        'index' : '0',
        'service_name' : 'Услуг Телефония',
        'total' : str(total_cdr)
    },
    {
        'index': '1',
        'service_name' : 'Услуг Netflow',
        'amount' : str(amount_netflow),
        'unit' : 'МБ',
        'total': str(total_netflow)
    }
]
document.merge_rows('index', servicesList)

# Chen thong tin tong hoa don
payment_total_without_tax = total_cdr + total_netflow
payment_total = round(payment_total_without_tax * TAX / 100, 2)
document.merge(
    payment_total_without_tax = str(payment_total_without_tax),
    tax = str(TAX) + ' %',
    payment_total = str(payment_total),
    service_count = str(len(servicesList))
)

document.write('invoice.docx')
print('processing...')
convert('invoice.docx')
os.remove('invoice.docx')
print('complete')
