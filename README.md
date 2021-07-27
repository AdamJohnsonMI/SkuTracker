
# InventoryManagement
Testing backend server deployment


SkuTracker, AKA InventoryManagement, is an inventory management app that allows users to track their inventory from submitting their ordered products, binning items in warehouse with the tracking number from the box into bin locations, creating pick lists, and user access control.

The front-end was created with HTML, CSS, JavaScript, and Bootstrap. The back-end was created with Python, Flask, and PostgreSQL as the database. 
![image](https://user-images.githubusercontent.com/66417986/124735784-5da5f880-dee4-11eb-9b56-137c569114e9.png)

![image](https://user-images.githubusercontent.com/66417986/124736116-b4abcd80-dee4-11eb-83d2-fcbbda560407.png)
![image](https://user-images.githubusercontent.com/66417986/124736204-c55c4380-dee4-11eb-8bc6-feafc2449ac1.png)
![image](https://user-images.githubusercontent.com/66417986/124736275-d73de680-dee4-11eb-95b9-a6e8957599a2.png)
![image](https://user-images.githubusercontent.com/66417986/124736364-ed4ba700-dee4-11eb-8e47-a4f96d11ffd5.png)
![image](https://user-images.githubusercontent.com/66417986/124736603-2e43bb80-dee5-11eb-828d-ce8b1d0c9b90.png)






Next steps for the project:

Major.
1. Restructure code to resemble MVC Structure. 
2. Organize web app functions to respective folders.
3. Improve Front end visual appeal and structure.

Misc.
1. Create a walk through video
2. Rename site to arbitrage something and research different hosting sites
3. Add preptype to users


Possible Ideas to Support Client
1. Add a date picked column?
2. Pick list bin location column should identify # of locations


Priority.
1. Have image link on receiving.


7/7/21
5. Picking less than quantity to pick should not remove the pick from system. 
7. Should not be able to receive 0 quantity or negative
8. Receiving by tracking needs a table below to show remaining tracking numbers not received
9. Missing orders page: orderid, ordernumber, asinid, description, qty missing
10. Add a note to orders that's visibile on receiving
11. Duplicate order under orderid that autopopulates current info but not the tracking numbers
