import db_operations
import tkinter as tk
import mysql.connector

root = tk.Tk()

HEIGHT = 600
WIDTH = 1080

#Connect with Bar Database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='pass',
    database='BAR_DATABASE'
)

#Create cursor
my_cursor = mydb.cursor(prepared=True)

def changeToInsertPage(frame):
    frame.place_forget()
    InsertProductUI(root)

def changeToSellPage(frame):
    frame.place_forget()
    SellProductUI(root)

def goBack(frame):
    frame.place_forget()
    MainPageUI(root)

#Main Page
class MainPageUI:
    def __init__(self, master):
        self.master = master
        master.title('Bar Inventory Register')

        # Canvas
        self.canvas = tk.Canvas(master, height=HEIGHT, width=WIDTH)
        self.canvas.pack()

        #Main Frame
        self.mainFrame = tk.Frame(master)
        self.mainFrame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        #Title Frame
        self.titleFrame = tk.Frame(self.mainFrame, bg='#0e68c2')
        self.titleFrame.place(x=0, y=0, relheight=0.6, relwidth=1.0)

        #Title
        self.title = tk.Label(self.titleFrame, text='Welcome to the Bar Inventory Register!', font=('Arial Black', 20)).place(relx= 0.5, rely=0.5, anchor='n')

        #Buttons Frame
        self.buttonsFrame = tk.Frame(self.mainFrame)
        self.buttonsFrame.place(x=0, rely=0.6, relheight=0.4, relwidth=1.0)

        #Insert Product Button
        self.insertBtn = tk.Button(self.buttonsFrame, text='Insert Product', command=lambda: changeToInsertPage(self.mainFrame))
        self.insertBtn.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.2)

        #Sell Product Button
        self.sellBtn = tk.Button(self.buttonsFrame, text='Sell Product', command=lambda: changeToSellPage(self.mainFrame))
        self.sellBtn.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.2)

#Insert Page
class InsertProductUI:
    def __init__(self, master):
        self.master = master
        master.title('Insert Product - Bar Inventory Register')

        # NumProducts Variable
        self.numProducts = 0

        #Product Name and Price variables
        self.productName = ''
        self.productPrice = 0

        # Main Frame
        self.mainFrame = tk.Frame(master, bg='#0e68c2')
        self.mainFrame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        #Input Frame
        self.inputFrame = tk.Frame(self.mainFrame)
        self.inputFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        #Title Label
        self.titleLabel = tk.Label(self.inputFrame, text='Insert new Product', font='Arial 25 bold')
        self.titleLabel.place(relx=0.05, rely=0.02)

        #Entries and Entries Labels

        #Quantity/Barcode Label
        self.quantityBarcodeLabel = tk.Label(self.inputFrame, text='Quantity:', font='Arial 10')
        self.quantityBarcodeLabel.place(relx=0.05, rely=0.25)

        #QuantityBarcode Entry
        self.quantityBarcodeEntry = tk.Entry(self.inputFrame, font='Arial 10')
        self.quantityBarcodeEntry.place(relx=0.12, rely=0.25)

        #Product Name Label
        self.productNameLabel = tk.Label(self.inputFrame, text='Product Name:', font='Arial 10')
        self.productNameLabel.place(relx=0.05, rely=0.4)

        #Product Name Entry
        self.productNameEntry = tk.Entry(self.inputFrame, font='Arial 10')
        self.productNameEntry.place(relx=0.16, rely=0.4)

        #Price Label
        self.priceLabel = tk.Label(self.inputFrame, text='Price:', font='Arial 10')
        self.priceLabel.place(relx=0.05, rely=0.55)

        #Price Entry
        self.priceEntry = tk.Entry(self.inputFrame, font='Arial 10')
        self.priceEntry.place(relx=0.10, rely=0.55)

        #Continue/Insert Button
        self.continueInsertBtn = tk.Button(self.inputFrame, text='Continue', command=lambda: self.continueCommand(self.quantityBarcodeEntry.get(), self.productNameEntry.get(), float(self.priceEntry.get())))
        self.continueInsertBtn.place(relx=0.05, rely=0.7, relwidth=0.1)

        #Back Button
        self.backBtn = tk.Button(self.inputFrame, text='<< Back', command=lambda: goBack(self.mainFrame))
        self.backBtn.place(relx=0.2, rely=0.7, relwidth=0.1)
        #Feedback Label
        self.feedback = tk.Label(self.inputFrame, font='Arial 10')
        self.feedback.place(relx=0.05, rely=0.85)

    def insertProductCommand(self, barcode, name, price):
        text = db_operations.insertProduct(my_cursor, name, barcode, price)
        mydb.commit()

        #Feedback message
        self.feedback.config(text=text)

        if 'Something went wrong:' not in text:
            self.numProducts -= 1
            self.checkNumProducts()
    
    def checkNumProducts(self):
        if(self.numProducts == 0):
            self.continueInsertBtn.place_forget()
            self.feedback.config(text='You sucessfully inserted all the products in the database')
            self.backBtn.config(command=lambda: changeToInsertPage(self.mainFrame))

    def continueCommand(self, quantity, name, price):
        self.numProducts = int(quantity)    
        self.productName = name
        self.productPrice = float(price)
        self.quantityBarcodeLabel.config(text='Barcode:')
        self.priceEntry.place_forget()
        self.productNameEntry.place_forget()
        self.continueInsertBtn.config(text='Insert', command=lambda: self.insertProductCommand(self.quantityBarcodeEntry.get(), self.productName, self.productPrice))

#Sell Page
class SellProductUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Sell Product - Bar Inventory Register')

        #Final Price
        self.finalPrice = 0

        #List of Products
        self.listProducts = list()

        #Main Frame
        self.mainFrame = tk.Frame(master, bg='#0e68c2')
        self.mainFrame.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        #Input Frame
        self.inputFrame = tk.Frame(self.mainFrame)
        self.inputFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        #Title Label
        self.titleLabel = tk.Label(self.inputFrame, text='Sell Product', font='Arial 25 bold')
        self.titleLabel.place(relx=0.05, rely=0.02)

        #Entries and Entries Labels

        #Barcode/Amount Label
        self.label = tk.Label(self.inputFrame, text='Barcode:', font='Arial 10')
        self.label.place(relx=0.05, rely=0.25)

        #Barcode/Amount Entry
        self.entry = tk.Entry(self.inputFrame, font='Arial 10')
        self.entry.place(relx=0.12, rely=0.25)

        #Continue Product Button
        self.continueBtn = tk.Button(self.inputFrame, text='Continue', command=lambda: self.searchProductCommand(barcode=self.entry.get()))
        self.continueBtn.place(relx=0.12, rely=0.7, relwidth=0.1)

        #Check Button
        self.checkBtn = tk.Button(self.inputFrame, text='Check', command=lambda: self.searchProductCommand())
        self.checkBtn.place(relx=0.24, rely=0.7, relwidth=0.1)

        #Back Button
        self.backBtn = tk.Button(self.inputFrame, text='<< Back', command=lambda: goBack(self.mainFrame))
        self.backBtn.place(relx=0.36, rely=0.7, relwidth=0.1)

        #Price/Error Label
        self.priceLabel = tk.Label(self.inputFrame, text='', font='Arial 10')
        self.priceLabel.place(relx=0.05, rely=0.15)

        #Confirmation/Error Label
        self.confirmationLabel = tk.Label(self.inputFrame, text='', font='Arial 10')
        self.confirmationLabel.place(relx=0.05, rely=0.8)

    def searchProductCommand(self, barcode=None):
        if barcode is not None:
            self.listProducts.append(barcode)
            price = db_operations.searchProduct(my_cursor, barcode)
            if price is None:
                #Error label
                self.priceLabel.config(text='Barcode is not correct or product is not existent')
            else:
                self.finalPrice += float(price)
                #Insert Price Label
                self.priceLabel.config(text=f'Price: €{self.finalPrice}')

        else:
            self.continueBtn.place_forget()
            self.label.config(text='Amount')
            #Change Button Text And Command
            self.checkBtn.config(command=lambda: self.checkChangeCommand(float(self.entry.get()), self.finalPrice))
        mydb.commit()

    def checkChangeCommand(self, amount, price):
        change = db_operations.checkChange(amount, price)
        text = 'Item was sucessfully purchased'
        if change >= 0:
            if change > 0:
                text = text + f'You must pay €{change} in change. Item was purchased successfully'
            for barcode in self.listProducts:
                db_operations.removeProduct(my_cursor, barcode)
        elif change < 0:
            text = 'Amount is not enough'

        self.confirmationLabel.config(text=text)
        self.checkBtn.place_forget()
        self.backBtn.config(command= lambda: changeToSellPage(self.mainFrame))
        self.listProducts.clear()
        mydb.commit()


main_page_ui = MainPageUI(root)
main_page_ui
root.mainloop()