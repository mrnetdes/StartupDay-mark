# Script to test printing using win32print
# Mark Ritchie 08/05/2017
# Uses win32print

import time
import os, sys
if (os.name != "posix"):
  import win32print
  printer_name = win32print.GetDefaultPrinter()
  hPrinter = win32print.OpenPrinter(printer_name)
  text_data = "Hello World\n"
  # Open a doc, open a page, wirte the page and close page and doc
  hJob = win32print.StartDocPrinter(hPrinter,1,("win32print Test Job",None,"TEXT"))
  win32print.StartPagePrinter(hPrinter)
  win32print.WritePrinter(hPrinter, text_data)
  win32print.EndPagePrinter(hPrinter)
  win32print.EndDocPrinter(hPrinter)
  win32print.ClosePrinter(hPrinter)
  # End of os.name != "posix"
