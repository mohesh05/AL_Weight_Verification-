## Weight Verification and Smart Dispatch Validation System

## 📌 Project Overview

The Weight Verification and Smart Dispatch Validation System is an industrial automation project developed to reduce dispatch errors, detect missing components, and improve packaging quality assurance.

The system automatically:
- scans product barcode
- reads product weight from weighing machine
- compares actual weight with stored expected weight
- validates using ±5% tolerance
- generates PASS / FAIL status
- prints QR label using Zebra printer

This project helps industries automate dispatch verification and reduce manual errors.

---

# 🚀 Features

✅ Barcode Scanner Integration  
✅ Real-Time Weight Verification  
✅ RS232 Serial Communication  
✅ PASS / FAIL Validation  
✅ Automatic QR Printing  
✅ Zebra Printer Integration  
✅ Industrial Dashboard UI  
✅ Auto Focus Barcode Input  
✅ Smart Dispatch Validation  
✅ CSV Product Database Support  
✅ Fast Product Lookup  
✅ Automated Quality Checking  

---

# 🏭 Industrial Problem Solved

In dispatch departments, industries face:
- Missing components
- Incorrect packaging
- Human errors
- Slow manual checking
- Wrong dispatch validation

This system automates the complete verification process.

---

# 🛠️ Technologies Used

## Frontend
- HTML
- CSS
- JavaScript

## Backend
- Python
- Flask

## Database
- CSV File

## Communication
- RS232 Serial Communication
- PySerial

## Printing
- Zebra ZPL Printing

## Libraries Used
- Flask
- Pandas
- PySerial
- PyWin32

---

# 🖥️ Hardware Components

- Barcode Scanner
- Weighing Machine
- RS232 to USB Converter
- Zebra QR Printer
- Computer System

---

# ⚙️ System Workflow

```text
Barcode Scan
      ↓
Fetch Product Data
      ↓
Read Weight From Machine
      ↓
Compare Expected Weight
      ↓
Tolerance Validation (±5%)
      ↓
PASS / FAIL Result
      ↓
Print QR Label


📂 Project Structure
AL_weight/
│
├── app.py
├── products.csv
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── generated_qr/
│
└── README.md


📦 Installation
1️⃣ Clone Project
git clone <repository-link>

OR

Download ZIP and extract.

2️⃣ Create Virtual Environment
python -m venv .venv
3️⃣ Activate Virtual Environment
Windows
.venv\Scripts\activate
4️⃣ Install Required Packages
pip install flask pandas pyserial pywin32
▶️ Run Project
python app.py

Application runs at:

http://127.0.0.1:5000
🗂️ CSV Database Format
products.csv
barcode,product_name,expected_weight
8901230000000,Product A,500
8901230000001,Product B,750
8901230000002,Product C,1000
🔌 RS232 Configuration

Inside app.py

SERIAL_PORT = "COM3"
BAUD_RATE = 9600

Change COM port according to your system.

🖨️ Zebra Printer Configuration

Set printer name inside:

printer_name = "ZDesigner ZD421-300dpi ZPL"

OR use default printer:

win32print.GetDefaultPrinter()
📱 QR Label Contains

Generated QR includes:

Product Name
Barcode Number
Weight
PASS Status

Example:

Product:Product B;
Barcode:8901230000001;
Weight:750g;
Status:PASS
📊 Weight Validation Logic

Tolerance used:

±5%

PASS Condition
Lower Limit ≤ Actual Weight ≤ Upper Limit
🎯 Advantages
Faster dispatch process
Reduced manual errors
Smart industrial automation
Real-time validation
Automatic QR printing
Better quality assurance
Improved productivity
🏭 Applications
Manufacturing Industries
Packaging Industries
Logistics
Warehouse Management
Smart Factories
Dispatch Departments
🔮 Future Enhancements
Cloud Database Integration
AI Analytics
IoT Monitoring
ERP Integration
RFID Support
Mobile Dashboard
📸 Output Features

✅ Live Weight Display
✅ PASS / FAIL Status
✅ QR Label Printing
✅ Real-Time Barcode Validation

👨‍💻 Developed Using
Python Flask
HTML/CSS
Zebra ZPL
PySerial
Pandas
📄 License

This project is developed for:

Academic Project
Industrial Automation Demo
Final Year Project
Internship Presentation
🙏 Acknowledgement

Special thanks to:

Project Guide
Faculty Members
Industry Support Team
Friends & Family

for their valuable support throughout the project development.

