import customtkinter as ctk
import yfinance as yf
from tkinter import filedialog
from fpdf import FPDF
import pandas as pd
from tabulate import tabulate
from list import *

def enable_export_button():
    button_export_pdf.configure(state="normal")

def disable_export_button_and_clear():
    button_export_pdf.configure(state="disabled")
    textBox.delete("1.0", "end")

def print_popular_stocks():
    textBox.delete("1.0", "end")
    for i, stock in enumerate(popularStocks, start=1):
        ticker, name = stock
        textBox.insert("end", f"{i}. {ticker} - {name}\n")
    enable_export_button()

def export_to_pdf():
    text_content = textBox.get("1.0", "end")
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text_content)
        pdf.output(file_path)

window = ctk.CTk()

window.title("Stock info")
window.rowconfigure(0, weight=0)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(3, weight=1)

topWidget = ctk.CTkFrame(window)
label = ctk.CTkLabel(window, text="", fg_color="transparent", compound="top", corner_radius=90, font=("Quicksand SemiBold", 15))
label.configure(text="Input stock ticker: ")
text = label.cget("text")
label.grid(row=0, column=0, sticky="e", padx=20, pady=20)

entry = ctk.CTkEntry(window, border_width=2, corner_radius=90, font=("Quicksand SemiBold", 12), placeholder_text="AAPL")
entry.grid(row=0, column=1, sticky="w", padx=20, pady=20)

button_100stocks = ctk.CTkButton(window, text="Print 100 popular stocks", command=print_popular_stocks, fg_color="transparent", font=("Quicksand SemiBold", 15), corner_radius=90, border_width=2)
button_100stocks.grid(row=1, column=0, sticky="e", padx=40, pady=20) 

button_clear = ctk.CTkButton(window, text="Clear", command=disable_export_button_and_clear, fg_color="transparent", font=("Quicksand SemiBold", 15), corner_radius=90, border_width=2)
button_clear.grid(row=1, column=1, sticky="w", padx=40, pady=20) 

button_export_pdf = ctk.CTkButton(window, text="Export to PDF", command=export_to_pdf, fg_color="transparent", font=("Quicksand SemiBold", 15), corner_radius=90, border_width=2, state="disabled")
button_export_pdf.grid(row=3, column=0, columnspan=2, sticky="ew", padx=250, pady=10)

textBox = ctk.CTkTextbox(window, height=500, width=900, padx=10, pady=10, font=("Quicksand SemiBold", 12))
textBox.grid(row=2, column=0, columnspan=2, sticky="nsew")  

scrollbar = ctk.CTkScrollbar(window, command=textBox.yview)
scrollbar.grid(row=2, column=2, sticky="ns")

textBox.configure(yscrollcommand=scrollbar.set)

def get_stock_info(e):
    enable_export_button()
    textBox.delete("1.0", "end")
    stock = str(e.widget.get()).upper().strip()
    if not stock:
        print("No stock ticker entered")
    else:
        None

    stockData = yf.Ticker(stock)
    
    textBox.insert("end", "Ticker: " + stock + "\n\n")

    for key in stockData.info.keys():
        try:
            v = str(key) + ": " + str(stockData.info[key]) + "\n\n"
            textBox.insert("end", v)

        except:
            pass

    history = stockData.history(period="1y", interval="1d")

    table = pd.DataFrame(history)
    table_str = tabulate(table, headers='keys', tablefmt='grid', showindex=False)

    textBox.insert("end", "Historical Data:\n\n")
    textBox.insert("end", table_str)

entry.bind("<Return>", get_stock_info)
window.mainloop()
