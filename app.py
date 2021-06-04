from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import psycopg2
import psycopg2.extras
#from os import path, walk
import os


app = Flask(__name__)
#Load config information. Will move to .env when needed.
app.config['TEMPLATES_AUTO_RELOAD'] = True
SECRET_KEY = os.getenv('SECRET_KEY')
app.secret_key = SECRET_KEY


def get_db_connection():
    #AWS database
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn

def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cursor.fetchone()                    
    conn.close()
    if post is None:
        abort(404)
    return post

def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM product WHERE asinid = %s", (product_id,))
    product = cursor.fetchone()                    
    conn.close()
    if product is None:
        abort(404)
    return product

def get_contents(contents_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM bin WHERE contentid = %s", (contents_id,))
    contents = cursor.fetchone()                    
    conn.close()
    if contents is None:
        abort(404)
    return contents
    
def get_bin(bin_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM physicallocation WHERE locationid = %s", (bin_id,))
    bin = cursor.fetchone()                    
    conn.close()
    if bin is None:
        abort(404)
    return bin

def get_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM orders WHERE invid = %s", (order_id,))
    order = cursor.fetchone()                    
    conn.close()
    if order is None:
        abort(404)
    return order

def get_tracking(tracking_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM tracking WHERE trackingid = %s", (tracking_id,))
    tracking = cursor.fetchone()                    
    conn.close()
    if tracking is None:
        abort(404)
    return tracking
        
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM posts');
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)', 
                         (title, content));
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE posts SET title = %s, content = %s'
                         ' WHERE id = %s',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
    
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/product')
def view_product():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT product.asinid, product.picture, product.hazardous, product.description, product.oversized, bin.locationid FROM product LEFT OUTER JOIN bin ON product.asinid=bin.asinid');
    products = cursor.fetchall()
    conn.close()
    return render_template('product.html', products=products)

@app.route('/product/<string:product_id>')
def product(product_id):
    product = get_product(product_id)

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT bin.locationid, bin.asinid, bin.quantity, bin.datereceived, bin.expirationdate,physicallocation.shelfid, physicallocation.rackid FROM bin JOIN physicallocation ON bin.locationid=physicallocation.locationid WHERE asinid = %s ", (product_id,))
    locations = cursor.fetchall()                    
    conn.close()
    return render_template('product/view_product.html', product=product, locations=locations)   

@app.route('/product/create', methods=('GET', 'POST'))
def product_create():
    if request.method == 'POST':
        asinid = request.form['asinid']
        picture = request.form['picture']
        hazardous = request.form['hazardous']
        oversized = request.form['oversized']
        description = request.form['description']
        
        if not asinid:
            flash('ASIN is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO product (asinid, picture, hazardous, oversized, description) VALUES (%s, %s, %s, %s, %s)', 
                         (asinid, picture, hazardous, oversized, description));
            conn.commit()
            conn.close()
            return redirect(url_for('view_product'))
    return render_template('product/create.html')  
       

       

@app.route('/product/<string:product_id>/edit', methods=('GET', 'POST'))
def product_edit(product_id):
    product = get_product(product_id)

    if request.method == 'POST':
        picture = request.form['picture']
        hazardous = request.form['hazardous']
        oversized = request.form['oversized']
        description = request.form['description']

        conn = get_db_connection()
            
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('UPDATE product SET picture = %s, hazardous = %s, oversized = %s , description = %s ' ' WHERE ASINid = %s', 
                         (picture, hazardous, oversized, description, product[0]));
        conn.commit()
        conn.close()
        return redirect(url_for('view_product')) 

    return render_template('product/edit.html', product=product)        

 
@app.route('/product/<string:product_id>/delete', methods=('POST',))
def product_delete(product_id):
    product = get_product(product_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM product WHERE asinid = %s', (product_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(product['asinid']))
    return redirect(url_for('view_product'))


@app.route('/create_bin', methods=('GET', 'POST'))
def create_bin():
    if request.method == 'POST':
        rackid = request.form['rackid']
        shelfid = request.form['shelfid']
        
        if not rackid:
            flash('rackid is required!')
        elif not shelfid:
            flash('rackid is required!')    
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO physicallocation (rackid, shelfid) VALUES (%s, %s)', 
                         (rackid, shelfid));
            conn.commit()
            conn.close()
            return redirect(url_for('view_bin'))
    return render_template('bin/create_bin.html') 

@app.route('/view_bin')
def view_bin():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM physicallocation');
    bins = cursor.fetchall()
    conn.close()
    return render_template('bin/view_bins.html', bins=bins)    

@app.route('/contents/bin_item', methods=('GET', 'POST'))
def bin_item():
    if request.method == 'POST':
        locationid= request.form['locationid']
        asinid = request.form['asinid']
        quantity = request.form['quantity']
        datereceived = request.form['datereceived']
        expirationdate = request.form['expirationdate']

                
        if not locationid:
            flash('locationid is required!')
        elif not asinid:
            flash('asinid is required!')   
        elif not quantity:
            flash('quantity is required!')  
        elif not datereceived:
            flash('datereceived is required!')   
        elif not expirationdate:
            flash('expirationdate is required!')              
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO bin (locationid, asinid, quantity, datereceived, expirationdate) VALUES (%s, %s, %s, %s, %s)', 
                         (locationid, asinid, quantity, datereceived, expirationdate));
            conn.commit()
            conn.close()
            return redirect(url_for('view_items'))
    return render_template('bin/contents/bin_item.html') 

@app.route('/contents/view_items')
def view_items():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM bin');
    items = cursor.fetchall()
    conn.close()
    return render_template('bin/contents/view_items.html', items=items) 

@app.route('/bin/contents/<int:contents_id>')
def contents_id(contents_id):
    contents = get_contents(contents_id)
    return render_template('bin/contents/contents.html', contents=contents)

@app.route('/bin/contents/<int:contents_id>/delete', methods=('POST',))
def contents_delete(contents_id):
    contents = get_contents(contents_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM bin WHERE contentid = %s', (contents_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(contents['contentid']))
    return redirect(url_for('view_items'))   

@app.route('/bin/contents/<int:contents_id>/edit', methods=('GET', 'POST'))
def contents_edit(contents_id):
    contents = get_contents(contents_id)

    if request.method == 'POST':
        locationid = request.form['locationid']
        asinid = request.form['asinid']
        quantity= request.form['quantity']
        datereceived = request.form['datereceived']
        expirationdate = request.form['expirationdate']

        if not asinid:
            flash('asinid is required!')
        else:
            conn = get_db_connection()
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE bin SET locationid = %s, asinid = %s, quantity = %s , datereceived = %s, expirationdate= %s ' ' WHERE contentid = %s', 
                         (locationid, asinid, quantity, datereceived, expirationdate, contents[0]));
            conn.commit()
            conn.close()
            return redirect(url_for('view_items')) 

    return render_template('bin/contents/contents_edit.html', contents=contents)     

@app.route('/bin/<int:bin_id>')
def bin_id(bin_id):
    bin = get_bin(bin_id)
    return render_template('bin/bin.html', bin=bin)

@app.route('/bin/<int:bin_id>/edit', methods=('GET', 'POST'))
def bin_edit(bin_id):
    bin = get_bin(bin_id)

    if request.method == 'POST':
        rackid = request.form['rackid']
        shelfid = request.form['shelfid']
        

        if not shelfid:
            flash('shelfid is required!')
        else:
            conn = get_db_connection()
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE physicallocation SET rackid = %s, shelfid = %s' ' WHERE locationid = %s', 
                         (rackid, shelfid, bin[0]));
            conn.commit()
            conn.close()
            return redirect(url_for('view_bin')) 

    return render_template('bin/bin_edit.html', bin=bin)   

@app.route('/bin/<int:bin_id>/delete', methods=('POST',))
def bin_delete(bin_id):
    bin = get_bin(bin_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM physicallocation WHERE locationid = %s', (bin_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(bin['locationid']))
    return redirect(url_for('view_bin'))   

@app.route('/orders/create', methods=('GET', 'POST'))
def create_order():
    if request.method == 'POST':
       
        asinid = request.form['asinid']
        buyPrice = request.form['buyPrice']
        sellPrice = request.form['sellPrice']
        store = request.form['store']
        supplier = request.form['supplier']
        quantity = request.form['quantity']
        orderNumber = request.form['orderNumber']
        fullfillment= request.form['fullfillment']
        buyer = request.form['buyer']
        
        if not asinid:
            flash('asinid is required!')
           
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO orders (asinid, buyPrice, sellPrice, store, supplier,quantity,orderNumber,fullfillment,buyer) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                         (asinid, buyPrice, sellPrice, store, supplier,quantity,orderNumber,fullfillment,buyer));
            conn.commit()
            conn.close()
            return redirect(url_for('view_orders'))
    return render_template('orders/create.html') 

@app.route('/orders/<int:order_id>')
def order_id(order_id):
    order = get_order(order_id)
    return render_template('orders/order.html', order=order)

@app.route('/orders/view_orders')
def view_orders():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #Fix missing bins caused by JOIN
    cursor.execute('SELECT DISTINCT orders.invid, orders.asinid, orders.datePurchased, orders.buyPrice, orders.sellPrice, orders.store, orders.supplier, orders.quantity, orders.orderNumber, orders.fullfillment, orders.buyer, bin.locationid FROM orders LEFT OUTER JOIN bin ON orders.asinid = bin.asinid');
    orders = cursor.fetchall()
    conn.close()
    return render_template('orders/view_orders.html', orders=orders) 

@app.route('/orders/<int:order_id>/delete', methods=('POST',))
def order_delete(order_id):
    order = get_order(order_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM orders WHERE invid = %s', (order_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(order['invid']))
    return redirect(url_for('view_orders'))       

@app.route('/orders/<int:order_id>/edit', methods=('GET', 'POST'))
def order_edit(order_id):
    order = get_order(order_id)

    if request.method == 'POST':
        asinid = request.form['asinid']
        buyPrice = request.form['buyPrice']
        sellPrice = request.form['sellPrice']
        store = request.form['store']
        supplier = request.form['supplier']
        quantity = request.form['quantity']
        orderNumber = request.form['orderNumber']
        fullfillment= request.form['fullfillment']
        buyer = request.form['buyer']
        

        if not asinid:
            flash("Hi!")
        else:
            conn = get_db_connection()
            
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('UPDATE orders SET asinid = %s, buyPrice = %s, sellPrice = %s, store = %s, supplier = %s, quantity = %s, orderNumber = %s, fullfillment = %s, buyer = %s' ' WHERE invid = %s', 
                         (asinid, buyPrice, sellPrice, store, supplier,quantity,orderNumber,fullfillment,buyer, order[0]));
            conn.commit()
            conn.close()
            return redirect(url_for('view_orders')) 

    return render_template('orders/edit.html', order=order) 









##################################TRACKING IN PROGRESS


@app.route('/tracking')
def view_tracking():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM tracking');
    trackingNums = cursor.fetchall()
    conn.close()
    return render_template('tracking/tracking.html', trackingNums=trackingNums)

@app.route('/tracking/<string:tracking_id>')
def tracking(tracking_id):
    trackingNums = get_tracking(tracking_id)
####Come back to add query for each invid in the tracking number
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT bin.locationid, bin.asinid, bin.quantity, bin.datereceived, bin.expirationdate,physicallocation.shelfid, physicallocation.rackid FROM bin LEFT OUTER JOIN physicallocation ON bin.locationid=physicallocation.locationid WHERE trackingid = %s", (tracking_id,))
    locations = cursor.fetchall()                    
    conn.close()
    return render_template('tracking/view_tracking.html', trackingNums=trackingNums,locations=locations)   

@app.route('/tracking/create', methods=('GET', 'POST'))
def tracking_create():
    if request.method == 'POST':
        trackingid = request.form['trackingid']
        invid = request.form['invid']
        received = request.form['received']
        
         ####Come back to the tags and execute
        
        if not trackingid:
            flash('Tracking Number is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO tracking (trackingid, invid, received) VALUES (%s, %s, %s)', 
                         (trackingid, invid, received));
            conn.commit()
            conn.close()
            return redirect(url_for('view_tracking'))
    return render_template('tracking/create.html')  
       

       

@app.route('/tracking/<string:tracking_id>/edit', methods=('GET', 'POST'))
def tracking_edit(tracking_id):
    tracking = get_tracking(tracking_id)

    if request.method == 'POST':
        trackingid = request.form['trackingid']
        received = request.form['received']

        conn = get_db_connection()
            
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('UPDATE tracking SET trackingid = %s, received = %s  ' ' WHERE invid = %s', 
                         (trackingid, received, tracking[0]));
        conn.commit()
        conn.close()
        return redirect(url_for('view_tracking')) 

    return render_template('tracking/edit.html', tracking=tracking)        

 
@app.route('/tracking/<string:tracking_id>/delete', methods=('POST',))
def tracking_delete(tracking_id):
    tracking = get_tracking(tracking_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM tracking WHERE trackingid = %s', (tracking_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(tracking['trackingid']))
    return redirect(url_for('view_tracking'))