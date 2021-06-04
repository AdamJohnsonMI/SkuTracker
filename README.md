
# InventoryManagement
Testing backend server deployment


SkuTracker, AKA InventoryManagement, is an inventory management app that allows users to track their inventory. 

The front-end was created with HTML, CSS, JavaScript, and Bootstrap. THe back-end was created with Python, Flask, and postgresql as the database. 

![ExamplePage](https://user-images.githubusercontent.com/66417986/120581300-93912200-c3f8-11eb-9074-d19aa8c2c03f.png)

![InventoryV3](https://user-images.githubusercontent.com/66417986/120850024-e4159600-c544-11eb-8491-0f4959470d9a.jpg)

Next steps for the project:

1. Add orders functionality as show in database diagram above. Hide the ASIN management under an admin panel. Orders page should have tracking number column when viewed as well as location of ASINs in bins.
2. Add login/authentication
3. Adding to warehouse down with tracking number instead of ASIN. App should identify ASINs in tracking number and prompt for info.
4. When receiving, date received should be added automatically.
5. Search by ASIN to find bin locations. 
6. Pick option/ship option. Maybe add a temp tab if not all items are pulled.
7. Add sort feature to pages. 

Remove ASIN page and condense to Orders tab? 1 click add.
Actual error messages. 
Forms autofilled with database info to not reset info on submit.
Change tracking number to varchar

