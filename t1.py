import win32print

# Replace with your actual printer name
PRINTER_NAME = "ZDesigner ZD421-300dpi ZPL"

zpl = """
^XA
^FO50,50^A0N,40,40^FDHello Zebra!^FS
^FO50,120^BY2
^BCN,100,Y,N,N
^FD1234567890^FS
^XZ
"""

printer = win32print.OpenPrinter(PRINTER_NAME)

try:
    job = win32print.StartDocPrinter(printer, 1, ("Zebra Test", None, "RAW"))
    win32print.StartPagePrinter(printer)

    win32print.WritePrinter(printer, zpl.encode("utf-8"))

    win32print.EndPagePrinter(printer)
    win32print.EndDocPrinter(printer)

    print("Print sent successfully!")

finally:
    win32print.ClosePrinter(printer)