# BIR-Bar-Inventory-Register
A Python application that register and deletes bar items on a MySQL Database

## Technologies used
* Python
  * Tkinter for GUI
  * MySQL Connector for connecting and issuing operation to MySQL Database
* MySQL

## Tables and processes

Database has two tables with their follwoing columns:
* Products
  * BARCODE: PRIMARY KEY
  * PRODUCT_NAME: VARCHAR(50)
  * PRICE: DECIMAL(4,2)
  
* Deleted Products
  * BARCODE: PRIMARY KEY
  * PRODUCT_NAME: VARCHAR(50)
  
 Here are the available processes:

1. Insert Product

  * In order to insert a product, the user must input its names, price and barcode. Barcode uniquely identifies each product.
  
  **Example:** Two identical Heineken bottles should have different barcodes.
  
2. Sell Product

  * Before a product is sold, it first checks if the amount given by client is sufficient and if it demands a change (when amount is higher than the price).
  
  * After the product is sold, the product is deleted from Products table and a SQL trigger will send this product to the Deleted Products table
  
  
