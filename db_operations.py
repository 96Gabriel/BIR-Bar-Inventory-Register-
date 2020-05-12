import mysql.connector

#Error for wrong length
class BarcodeLengthError(Exception):
    pass

#Functions for operations
def insertProduct(my_cursor, productName, barcode, price):
    try:
        if len(barcode) != 13:
            raise BarcodeLengthError('Barcode length is not correct')
        insertQuery = 'INSERT INTO PRODUCTS VALUES(%s, %s, %s)'
        productValues = (barcode, productName, price)
        my_cursor.execute(insertQuery, productValues)
        return 'Item successfully stored in the database'
    except (mysql.connector.Error, BarcodeLengthError) as err:
        return f'Something went wrong: {err}'
        

def searchProduct(my_cursor, barcode):
    try:
        selectQuery = 'SELECT PRICE FROM PRODUCTS WHERE BARCODE = %s'
        my_cursor.execute(selectQuery, (barcode,))
        return my_cursor.fetchone()[0]
    except TypeError:
        return None

def checkChange(amount, price):
    change = amount - float(price)
    return change

def removeProduct(my_cursor, barcode):
    removeQuery = 'DELETE FROM PRODUCTS WHERE BARCODE = %s'
    my_cursor.execute(removeQuery, (barcode,))