
# InventoryManagement
Testing backend server deployment


SkuTracker, AKA InventoryManagement, is an inventory management app that allows users to track their inventory from submitting their ordered products, binning items in warehouse with the tracking number from the box into bin locations, creating pick lists, and user access control.

The front-end was created with HTML, CSS, JavaScript, and Bootstrap. The back-end was created with Python, Flask, and PostgreSQL as the database. 

![image](https://user-images.githubusercontent.com/66417986/122397562-1365d300-cf47-11eb-95a5-fe6b26e56224.png)

Next steps for the project:

Back-end
1. Update functionality for product picture, hazardous, and oversized for searching. (Low Priority)
2. Checkbox's for buyer. Need to implement list of buyers to iterate through
3. Have image link on receiving.
4. Add preptype to users

Front-end 
1. Expiration date is missing when using tracking numbers import. Binning item by tracking number should prompt on each product.


Misc.
1. Create a walk through video

Priority
1. Picklist (column in orders showing if item is on picklist) **Clarify with client if still needed under current organization**
2. Picklist- Picker can flag missing items under pick screen with quantity missing or add to damaged screen. **Feature in progress** 
3. Improve Front end visual appeal and structure.
5. Bugfix deleting tracking numbers is done by trackingid instead of serial. Don't allow multiple of the same tracking number for same order


6/21/21

6. Picking all items should not delete row. Just view items should not show qty of 0 items
7. Receiving by tracking should have qty received.  
8. Add date received when receiving. Sort warehouse by date received. 
9. Receiving item should redirect to adding items. 
10. Creating bin should be used by user defined locationid. Edit all location references
11. Rename site to arbitrage something and research different hosting sites

10. Add a date picked column

2. Pick list bin location column should identify # of locations
9. View orders header should stick with the screen while scrolling