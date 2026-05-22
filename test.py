from zebra import Zebra

z = Zebra()
z.setqueue("ZDesigner ZD421-300dpi ZPL")

zpl = """
^XA
^PW600
^LL400
^MD30
^FO50,50^A0N,60,60^FDHELLO ZEBRA^FS
^FO50,150^BY3
^BCN,120,Y,N,N
^FD123456^FS
^XZ
"""

z.output(zpl)

print("Done")