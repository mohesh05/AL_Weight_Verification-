from flask import Flask, render_template, request, jsonify
import pandas as pd
import serial
import time
import os
import logging
import threading
import win32print

app = Flask(__name__)

# =====================================================
# LOGGING CONFIGURATION
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================================================
# SERIAL PORT CONFIGURATION
# =====================================================

SERIAL_PORT = "COM3"
BAUD_RATE = 9600

# =====================================================
# THREAD LOCK FOR SERIAL ACCESS
# =====================================================

serial_lock = threading.Lock()

# =====================================================
# CONNECT SERIAL PORT
# =====================================================

try:

    ser = serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=2
    )

    # WAIT FOR DEVICE RESET

    time.sleep(2)

    logging.info("✅ Connected To Serial Port")

except Exception as e:

    ser = None

    logging.warning(
        "⚠️ Serial Port Not Connected (Demo Mode Enabled)"
    )

    logging.error(e)

# =====================================================
# LOAD PRODUCT DATABASE
# =====================================================

CSV_FILE = "products.csv"

if not os.path.exists(CSV_FILE):

    raise FileNotFoundError(
        f"{CSV_FILE} not found"
    )

try:

    df = pd.read_csv(
        CSV_FILE,
        dtype=str
    )

    # CLEAN CSV DATA

    df = df.apply(

        lambda x: x.str.strip()

        if x.dtype == "object"

        else x
    )

    # REMOVE .0 ISSUE

    df["barcode"] = df["barcode"].str.replace(
        ".0",
        "",
        regex=False
    )

    # FAST LOOKUP DICTIONARY

    products_dict = df.set_index(
        "barcode"
    ).to_dict("index")

    logging.info(
        "✅ CSV DATA LOADED SUCCESSFULLY"
    )

except Exception as e:

    logging.error(
        "❌ Failed To Load CSV"
    )

    logging.error(e)

    raise

# =====================================================
# ZEBRA QR PRINT FUNCTION
# =====================================================

def print_barcode_zebra(

    product_name,

    barcode,

    weight
):

    printer_handle = None

    try:

        # =========================================
        # SANITIZE VALUES
        # =========================================

        product_name = str(
            product_name
        ).replace("^", "")

        barcode = str(
            barcode
        ).replace("^", "")

        weight = str(
            weight
        ).replace("^", "")

        # =========================================
        # PRINTER NAME
        # =========================================

        printer_name = "ZDesigner ZD421-300dpi ZPL"

        logging.info(
            f"Using Printer: {printer_name}"
        )

        # =========================================
        # QR DATA
        # =========================================

        qr_data = f"""
Product: {product_name}
Barcode: {barcode}
Weight: {weight} g
Status: PASS
"""

        # =========================================
        # ZPL QR LABEL
        # =========================================

        zpl = f"""
^XA

^PW560
^LL240
^LH0,0
^MD18

^CF0,30
^FO25,20^FDWEIGHT VERIFICATION^FS

^CF0,24
^FO25,75^FDProduct : {product_name}^FS
^FO25,110^FDBarcode : {barcode}^FS
^FO25,145^FDWeight  : {weight} g^FS

^FO350,35
^BQN,2,6
^FDLA,Product:{product_name};Barcode:{barcode};Weight:{weight}g;Status:PASS^FS
^XZ
"""


        # =========================================
        # OPEN PRINTER
        # =========================================

        printer_handle = win32print.OpenPrinter(
            printer_name
        )

        # =========================================
        # START PRINT JOB
        # =========================================

        win32print.StartDocPrinter(

            printer_handle,

            1,

            ("QR Label", None, "RAW")
        )

        win32print.StartPagePrinter(
            printer_handle
        )

        # =========================================
        # SEND ZPL TO PRINTER
        # =========================================

        win32print.WritePrinter(

            printer_handle,

            zpl.encode("utf-8")
        )

        win32print.EndPagePrinter(
            printer_handle
        )

        win32print.EndDocPrinter(
            printer_handle
        )

        logging.info(
            "✅ QR Label Printed Successfully"
        )

    except Exception as e:

        logging.error("❌ Printer Error")

        logging.error(e)

    finally:

        if printer_handle:

            try:

                win32print.ClosePrinter(
                    printer_handle
                )

            except Exception as e:

                logging.error(
                    "❌ Failed To Close Printer"
                )

                logging.error(e)

# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def index():

    return render_template("index.html")

# =====================================================
# VERIFY PRODUCT
# =====================================================

@app.route("/verify", methods=["POST"])
def verify():

    try:

        # =============================================
        # VALIDATE REQUEST
        # =============================================

        if not request.json:

            return jsonify({

                "status": "ERROR",

                "message": "Invalid JSON Request"

            }), 400

        if "barcode" not in request.json:

            return jsonify({

                "status": "ERROR",

                "message": "Barcode Missing"

            }), 400

        # =============================================
        # GET BARCODE INPUT
        # =============================================

        barcode = str(
            request.json["barcode"]
        ).strip()

        barcode = barcode.replace(
            ".0",
            ""
        )

        logging.info(
            f"Scanned Barcode: {barcode}"
        )

        # =============================================
        # FIND PRODUCT
        # =============================================

        product = products_dict.get(barcode)

        # =============================================
        # PRODUCT NOT FOUND
        # =============================================

        if not product:

            logging.warning(
                "❌ Barcode Not Found"
            )

            return jsonify({

                "status": "ERROR",

                "message": "Barcode Not Found"

            })

        # =============================================
        # GET PRODUCT DETAILS
        # =============================================

        product_name = product["product_name"]

        expected_weight = float(
            product["expected_weight"]
        )

        # =============================================
        # READ WEIGHT FROM MACHINE
        # =============================================

        try:

            if ser:

                with serial_lock:

                    # CLEAR BUFFER

                    ser.reset_input_buffer()

                    # REQUEST WEIGHT

                    ser.write(b"READ\n")

                    time.sleep(1)

                    weight_data = ser.readline().decode(
                        errors="ignore"
                    ).strip()

                logging.info(
                    f"Weight Data: {weight_data}"
                )

                if not weight_data:

                    raise Exception(
                        "Empty Weight Data"
                    )

                current_weight = float(
                    weight_data
                )

            else:

                # DEMO MODE

                current_weight = expected_weight

                logging.info(
                    "⚠️ DEMO MODE ENABLED"
                )

        except Exception as e:

            logging.error(
                "❌ Weight Reading Failed"
            )

            logging.error(e)

            return jsonify({

                "status": "ERROR",

                "message": "Weight Reading Failed"

            })

        logging.info(
            f"Expected Weight: {expected_weight}"
        )

        logging.info(
            f"Current Weight: {current_weight}"
        )

        # =============================================
        # CALCULATE TOLERANCE
        # =============================================

        lower_limit = expected_weight * 0.95

        upper_limit = expected_weight * 1.05

        # =============================================
        # PASS CONDITION
        # =============================================

        if lower_limit <= current_weight <= upper_limit:

            logging.info(
                "✅ STATUS: PASS"
            )

            # SEND PASS SIGNAL

            try:

                if ser:

                    with serial_lock:

                        ser.write(b"PASS\n")

            except Exception as e:

                logging.error(
                    "PASS Signal Failed"
                )

                logging.error(e)

            # =========================================
            # PRINT QR LABEL
            # =========================================

            print_barcode_zebra(

                product_name,

                barcode,

                current_weight
            )

            return jsonify({

                "status": "PASS",

                "product_name": product_name,

                "expected_weight": expected_weight,

                "current_weight": current_weight

            })

        # =============================================
        # FAIL CONDITION
        # =============================================

        else:

            logging.warning(
                "❌ STATUS: FAIL"
            )

            # SEND FAIL SIGNAL

            try:

                if ser:

                    with serial_lock:

                        ser.write(b"FAIL\n")

            except Exception as e:

                logging.error(
                    "FAIL Signal Failed"
                )

                logging.error(e)

            return jsonify({

                "status": "FAIL",

                "product_name": product_name,

                "expected_weight": expected_weight,

                "current_weight": current_weight

            })

    except Exception as e:

        logging.error(
            "❌ Unexpected Error"
        )

        logging.error(e)

        return jsonify({

            "status": "ERROR",

            "message": "Internal Server Error"

        }), 500

# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False,

        threaded=True

    )