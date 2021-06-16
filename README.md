
# InventoryManagement
Testing backend server deployment


SkuTracker, AKA InventoryManagement, is an inventory management app that allows users to track their inventory. 

The front-end was created with HTML, CSS, JavaScript, and Bootstrap. The back-end was created with Python, Flask, and postgresql as the database. 

![ExamplePage](https://user-images.githubusercontent.com/66417986/120581300-93912200-c3f8-11eb-9074-d19aa8c2c03f.png)

![InventoryV4](https://user-images.githubusercontent.com/66417986/121511796-0846fc00-c9b7-11eb-90af-26fab959c0f0.jpg)


Next steps for the project:

Back-end

1. Update functionality for product picture, hazardous, and oversized for searching. (Low Priority)
2. Forms autofilled with database info to not reset info on submit. Editing currently overwrites fields with an empty string. (High)
3. Pick option/ship option. Maybe add a temp tab if not all items are shipped or easy re-add option. (High)
4. Actual error messages instead of a browser unknown error. (Med)



Front-end
1. Adding items to a tracking number should allow multiple items to be added at a time. 
2. Expiration date is missing when using tracking numbers import. Binning item by tracking number should prompt on each product.
3. Add a search bar to binned items screen to search by ASIN to find bin locations. 
4. Add a sort feature to pages. 


Misc.
1. Create a walk through video

Priority
1. **DONE** Adding multiple tracking numbers to same order. Button to submit and stay on same page to submit more?
2. **DONE*** Fix dashboard link
3. **DONE** Items marked as received when binning by tracking
4. **DONE** Tracking number and store attached to products in bin until picked. Also shown in view_items page
5. **DONE** Add order number column to /tracking and /tracking/<trackingid>. 
6. **DONE** Add product description to /tracking/trackingid
7. **DONE** Bin item list should just be a list of items to bin. ""Could add columns for toBeBinned and toBePicked""
8. **DONE** Ability to sort the columns
9.  Picklist (column in orders showing if item is on picklist) **Clarify Direction On This. Still Needed?**
10. **DONE**Picklist add items to a picklist table and picker should see list with a pick icon with quantity pulled
11. Picklist- Picker can flag missing items under pick screen with quantity missing or add to damaged screen. 