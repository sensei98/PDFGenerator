import os
from uploadPDFToServer import upload2server
from pathlib import Path

script_location = Path(__file__).absolute().parent
file_location = script_location
file = file_location.open()

abspath = os.path.dirname(os.path.abspath(__file__))
print(current_path)
print(abspath)

path = 'pdf_invoices/'
dirname = os.path.dirname(path)

print(dirname)

file = "./pdf_invoices/"

localpath = current_path + file


if os.path.isfile(localpath):
    print("file exists")
    f = open(localpath)

    try:
        upload2server(localpath, remotepath)
    except Exception as e:
        print(e)

    f.close
else:
    print("path does not exist")


try:

except Exception as e:
    print(e)


path_name = "pdf_invoices/#.pdf"

if os.path.isfile(path_name):
    print("File exists")
    f = open(path_name)
    # Execute other file operations here
    f.close()

else:
    print("File does not exist! IOError has occured")

# ------------------------------------------------------------------------------------------
file = '#'
localpath = file
remotepath = "/home/pi/storage/bol_invoice/pdf/" + file
try:
    upload2server(localpath, remotepath)
except Exception as e:
    print(e)

# ------------------------------------------------------------------------------------------
current_path = 'pdf_invoices/'
path = current_path
folder = os.fsencode(path)
filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith('pdf'):
        filenames.append(filename)

lpath = 'pdf_invoices/', filenames, '.pdf'
remotepath = "/home/pi/storage/bol_invoice/pdf/", filenames
try:
    upload2server(lpath, remotepath)
except Exception as e:
    print(e)
            totalPrice = unitPrice
            vat = 21
            netPrice =
            if orderId == '1334947919':
                print(orderItems)
                print(list[0])

                for k in i["product"].items():
                    tupleData = k
                    print(tupleData["ean"])


                     # print(i["product"])
                    list = [(k, v) for k, v in i["product"].items()]
                    for i in list:
                        array.append(i)
                print(array)

                    newEan = list[0]
                    newItem = list[1]
                    tupleDataForEan.append(newEan)
                    tupleDataForItem.append(newItem)
                # print(newItem)
                # print(newEan)
            print(tupleDataForEan)
            print(tupleDataForItem)