from curses.ascii import isdigit
from operator import delitem
from tkinter.tix import FileSelectBox
import numpy as np
import bol_SDK as bol_sdk
import jinja2
import pdfkit
import pandas as pd
from base64 import encode
import os
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.encoders import encode_base64
import datetime
import csv
import uploadPDFToServer as server
# import storage as storage
import shutil
import glob
import random

# Invoice no generator
# TCB - 22 (year) - 02(month) 15(date) - 00000 (max 10000)
#format = year + '- ' + (str(randomNo).zfill(5))


# TODO: note!!! maxNoTxt file has to be changed to minumum number in txt file on pi
# orderInfo = storage.storageObject()
# # VAT
vatPercentage = 0.21

# TODO: DATE HAS TO BE CHANGED BEFORE DEPLOYING..COMMENTS ARE BELOW ON LINE 39 TO 42
# getting the previous date (today - 2)
previousDate = datetime.datetime.today() - datetime.timedelta(days=2)

# day = previousDate.day
# month = previousDate.month
# year = previousDate.year
# status = "ALL"

day = 26
month = 2
year = 2022
status = "ALL"

fromAddress = "#"
toAddress = '#'
subject = "#"
content = '#'


# --------------------------------



# --------------------------------


# getting txt number


def getTxtNo():
    f = open("maxNoCheck.txt", "r")
    f1 = f.read()
    txtNo = int(f1)
    return txtNo


def writeIncrementToTxt(val):
    with open('maxNoCheck.txt', 'w') as f:
        f.write(str(val))


def generateInvoiceNo():
    try:
        now = datetime.datetime.today() - datetime.timedelta(days=2)  # current date and time
        year = now.strftime("%Y")
        date = now.strftime("%d")
        month = now.strftime("%m")

        val = getTxtNo()
        val += 1

        # update formatted no to txt
        writeIncrementToTxt(val)
        stringFormat = f'TCB{year[-2:]}{month}{date}{str(val).zfill(5)}'
        return stringFormat
    except Exception as e:
        print(e)


# # USING PDFKIT TO APPLY MARGINS AND CONVERT HTML TO PDF USING THE HTML GENERATED


def html2pdf(html_path, pdf_path):
    """
    Convert html to pdf using pdfkit which is a wrapper of wkhtmltopdf
    """
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)


def emailPDF(fromAddress, toAddress, mailSubject, mailContent, date):
    try:
        directory = f'pdf_invoices/{date}/'
        for filename in os.scandir(directory):
            if filename.is_file:
                from_addr = fromAddress
                to_addr = toAddress
                subject = mailSubject
                content = mailContent

                msg = MIMEMultipart()
                msg['From'] = from_addr
                msg['To'] = to_addr
                msg['Subject'] = subject
                body = MIMEText(content, 'plain')
                msg.attach(body)

                with open(filename, 'rb') as f:
                    part = MIMEApplication(
                        f.read(), 'pdf')
                    part['Content-Disposition'] = 'attachment; filename="{}"'.format(
                        basename(filename))
                    encode_base64(part)
                msg.attach(part)

                server = smtplib.SMTP('smtp.googlemail.com', 587)

                #server = smtplib.SMTP_SSL('mail.teqclub.com', 465)

                server.ehlo()
                server.starttls()
                # password
                server.login(from_addr, '#')  # replace password with hash

                try:
                    server.send_message(
                        msg, from_addr=from_addr, to_addrs=[to_addr])
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


def appendDataToCSV(data, date):
    # generating csv for
    try:
        # filename = 'csv_invoices/invoices.csv'
        filename = f'csv_invoices/{date}.csv'  # include date as name
        fileEmpty = os.stat(filename).st_size == 0
        header = ['Invoice no.', 'Date', 'Email', 'Product name',
                  'EAN', 'Quantity', 'Customer name', 'Price', 'Customer Company', 'Address', 'VAT', 'TotalPrice', 'Country']
        with open(filename, 'a') as a:
            csv_out = csv.writer(a)
            if fileEmpty:
                csv_out.writerow(header)
            csv_out.writerow(data)
    finally:
        a.close()

# TODO: remember to remove first line after writing data to csv


def writeDataToCSV(data, date):
    try:
        filename = f'csv_invoices/{date}.csv'  # include date as name
        header = ['Invoice no.', 'Order no.', 'Date', 'Email', 'Product name',
                  'EAN', 'Quantity', 'Customer name', 'Price', 'Customer Company', 'Address', 'VAT', 'TotalPrice', 'Country']
        with open(filename, 'w', encoding='UTF8', newline='') as w:
            writer = csv.writer(w)
            writer.writerow(header)
            writer.writerow(data)
        appendDataToCSV(data, date)
    finally:
        w.close()


def movePDFFilesToFolder(pdf_path, date):
    try:
        osPath = os.path.dirname(os.path.abspath(__file__))
        pathToNewFolder = osPath + '/pdf_invoices/' + date
        if not os.path.isdir(pathToNewFolder):
            os.makedirs(os.path.join('pdf_invoices', date))

        shutil.move(pdf_path, pathToNewFolder)
    except Exception as e:
        print(e)


def initCSV(data, date):
    try:
        numberFromTxt = getTxtNo()
        if(numberFromTxt >= 1):
            filename = f'csv_invoices/{date}.csv'
            if os.path.isfile(filename):
                appendDataToCSV(data, date)
            else:
                writeDataToCSV(data, date)
    except Exception as e:
        print(e)


def deleteHTMLTemplates():
    try:
        osPath = os.path.dirname(
            os.path.abspath(__file__)) + "/html_templates/"
        filesToBeDeleted = glob.glob(os.path.join(osPath, "*.html"))
        for i in filesToBeDeleted:
            os.remove(i)

    except Exception as e:
        print(e)


# def getOrdersWithTwoOrMoreProducts(orderItems):

def main():
    try:
        # orderInfo = bol_sdk.bol_get_relevant_order_info(
        #     day, month, year, status)
        #line can be commented out (this is for testing)..use line 237 instead
        orderInfo = storage.storageObject()  # for debug purpose
        # print(orderInfo)

        for i in range(len(orderInfo)):
            orderPlacedDateTime = orderInfo[i]['orderPlacedDateTime']
            shipmentDetails = orderInfo[i]['shipmentDetails']
            orderItems = orderInfo[i]['orderItems']
            billingDetails = orderInfo[i]['billingDetails']

            orderDate = orderPlacedDateTime[8:10] + "-" + \
                orderPlacedDateTime[5:7] + "-" + orderPlacedDateTime[0:4]
            orderId = orderInfo[i]['orderId']

            if len(orderItems) > 1:
                for i in range(len(orderItems)):
                    product = orderItems[i]['product']
                    quantity = orderItems[i]['quantity']
                    unitPrice = orderItems[i]['unitPrice']

            else:
                product = orderItems[0]['product']
                quantity = orderItems[0]['quantity']
                unitPrice = orderItems[0]['unitPrice']

            item = product['title']
            ean = product['ean']

            email = shipmentDetails['email']
            customerName = billingDetails['firstName'] + \
                " " + billingDetails['surname']
            countryCode = billingDetails['countryCode']
            addressDetails = billingDetails['streetName'] + " " +\
                billingDetails['houseNumber'] + ", " +\
                billingDetails['zipCode'] + " " +\
                billingDetails['city'] + " " +\
                billingDetails['countryCode']
            company = "company"
            if company in billingDetails:
                customerCompany = billingDetails['company']
            else:
                customerCompany = ""

        # CALCULATING TOTAL PRICE EXCL. VAT PRICE

            orderItemsArray = []
            orderItemsPriceArray = []
            totalSum = 0

            if len(orderItems) > 1:
                for i in orderItems:
                    tmp = i['product']
                    tmp['unitPrice'] = i['unitPrice']
                    # TODO: Fix bug with finding price excl VAT
                    vat = 1 + vatPercentage
                    totalPrice = (tmp["unitPrice"] / vat)
                    vatAmount = (tmp["unitPrice"] - totalPrice)
                    actualAmount = (totalPrice + vatAmount)
                    formattedAmtWithoutVat = "{:.2f}".format(actualAmount)
                    tmp["unitPrice"] = float(formattedAmtWithoutVat)

                    orderItemsArray.append(tmp)
                    totalSum += tmp["unitPrice"]
                    # print(totalSum)

                vat = 1 + vatPercentage
                totalPrice = (totalSum / vat)
                # vatAmount = (totalSum - totalPrice)
                # grandTotal = (totalPrice + vatAmount)
            else:

                # -------------------------------------------------------------------------------------------------------------------------------------------------------------
                vat = 1 + vatPercentage
                totalPrice = (unitPrice / vat)
                vatAmount = (unitPrice - totalPrice)

                grandTotal = (totalPrice + vatAmount)

            formattedTotalVAT = "{:.2f}".format(vatAmount)
            formattedPriceExclVat = "{:.2f}".format(totalPrice)
            formattedGrandTotal = "{:.2f}".format(grandTotal)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------
            # getting the length of order items
            lengthOfOrderItems = len(orderItems)

        # SAVING OVERALL DATA INTO ONE VARIABLE FOR EASY HTML RENDERING

            invoiceNo = generateInvoiceNo()
            data = (invoiceNo, orderDate, email, item, ean, quantity,
                    customerName, unitPrice, customerCompany, addressDetails, formattedTotalVAT, formattedPriceExclVat, countryCode, orderItems, lengthOfOrderItems, orderId, orderItemsArray, orderItemsPriceArray, orderItems, formattedGrandTotal, vatPercentage)

            # exclusive for CSV init
            # generate Invoice No

            # data for csv export
            dataForCSVExport = (invoiceNo, orderId, orderDate, email, item, ean, quantity,
                                customerName, unitPrice, customerCompany, addressDetails, formattedTotalVAT, formattedPriceExclVat, countryCode)
            initCSV(dataForCSVExport, data[1])  # creating csv using date

            # initializing jinja2
            template_loader = jinja2.FileSystemLoader(searchpath="")
            template_env = jinja2.Environment(loader=template_loader)
            template_file = "/templates/invoice.html"
            template = template_env.get_template(template_file)

        #  SAVING HTML FOR CONVERSION (CAN BE DELETED AFTER CONVERSION)
            output_text = template.render(
                orderId=data[0],
                orderDate=data[1],
                email=data[2],
                productName=data[3],
                ean=data[4],
                quantity=data[5],
                customerName=data[6],
                unitPrice=data[7],
                customerCompany=data[8],
                address=data[9],
                totalVat=data[10],
                totalPrice=data[11],
                orderItems=data[13],
                lengthOfOrderItems=data[14],
                bolOrderId=data[15],
                orderItemsArray=data[16],
                priceItems=data[17],
                orderItemss=data[18],
                grandTotal=data[19],
                vatPercent=data[20]
            )

            """
        HTML to PDF
            """
            # SAVING HTML FOR CONVERSION (CAN BE DELETED AFTER CONVERSION)
            html_path = f'html_templates/{data[6]}.html'
            html_file = open(html_path, 'w')
            html_file.write(output_text)
            html_file.close()

            # printing name of customer
            print(f"Now converting {data[6]} ... ")

            # # PRINTING NAME OF PDF FILE USING THE ORDER ID
            pdf_path = f'pdf_invoices/{dataForCSVExport[0]}.pdf'
            html2pdf(html_path, pdf_path)

        # TODO: UNCOMMENT MOVING TO FOLDER, EMAILING AND OTHER FUNCTIONALITIES BELOW IF NEEDED,
        # moving files to new folder
        #    movePDFFilesToFolder(pdf_path, data[1])
        #  after pdf is generated, delete html templates
        # deleteHTMLTemplates()
        # email function.
        # print("emailing PDFs .......")
        # emailPDF(fromAddress, toAddress, subject, content, data[1])
        # generateInvoiceNo()  # generate invoice number (+1) after every loop

        # writeIncrementToTxt()
        # generateInvoiceNo()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
