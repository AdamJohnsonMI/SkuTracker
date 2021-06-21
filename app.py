from flask import Flask, render_template, request, url_for, flash, redirect, session, logging
from functools import wraps  #Used for login and admin control
from wtforms import Form, BooleanField, StringField, PasswordField, validators #Used for registering with a password
from passlib.hash import sha256_crypt
from werkzeug.exceptions import abort
import psycopg2
import psycopg2.extras #Allows dictionary cursor to be used
import os


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True #Allows templates to be edited without reloading flask
app.secret_key = os.getenv('SECRET_KEY') #Accesses secret key stored in env file

def get_db_connection(): #AWS database connection
    conn = psycopg2.connect(os.getenv('DATABASE_URL')) #URL stored in .env
    return conn

def get_post(post_id): #Get the post row with post_id as input
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cursor.fetchone()                     
    conn.close()
    if post is None:
        flash("Post does not exist")
        return redirect(url_for('dashboard'))
    return post

def get_product(product_id): #Get the product row with product_id as input
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM product WHERE asinid = %s", (product_id,))
    product = cursor.fetchone()                    
    conn.close()
    if product is None:
        flash("Product does not exist")
        return redirect(url_for('dashboard'))
    return product

def get_contents(contents_id): #Get the contents row with contents_id as input
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM bin WHERE contentid = %s", (contents_id,))
    contents = cursor.fetchone()                    
    conn.close()
    if contents is None:
        flash("Bin contents does not exist")
        return redirect(url_for('dashboard'))
    return contents
    
def get_bin(bin_id): #Get the bin row with bin_id as input
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM physicallocation WHERE locationid = %s", (bin_id,))
    bin = cursor.fetchone()                    
    conn.close()
    if bin is None:
        flash("Bin does not exist")
        return redirect(url_for('dashboard'))
    return bin

def get_order(order_id): #Get the order row with order as input
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM orders WHERE invid = %s", (order_id,))
    order = cursor.fetchone()                    
    conn.close()
    if order is None:
        flash("Order does not exist")
        return redirect(url_for('dashboard'))
    return order

def get_tracking(tracking_id): #Get the tracking row with tracking_id as input
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM tracking WHERE trackingid = %s", (tracking_id,))
    tracking = cursor.fetchone()                    
    conn.close()
    if tracking is None:
        flash("Tracking number does not exist")
        return redirect(url_for('dashboard'))
    return tracking
        
 
class RegisterForm(Form): #Captures user information from registration. 
    name = StringField('Name',[validators.Length(min=1,max=50)])
    username = StringField('Username',[validators.Length(min=4, max=25)])
    email = StringField('Email',[validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords do not match")
    ])
    confirm = PasswordField('Confirm Passowrd')

#Check if user is logged in
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap   

# Checks if user is logged in then checks if user is an admin
def admin_required(f): 
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if 'admin_role' in session:
                return f(*args, **kwargs)
            else:
                flash('Unauthorized, Please login as an admin', 'danger')
                return redirect(url_for('login'))        
        else:
            flash('Unauthorized, Please login as an admin', 'danger')
            return redirect(url_for('login'))
    return wrap  



#Begin routes section     
@app.route('/register', methods= ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data)) #Encrpyt data using SHA256
        userRole = 'user' #Sets the user role default to 'user' to limit access to application
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user == None: #Check if user row is empty
            cursor.execute("INSERT INTO users(name,email,username,password,userRole) VALUES (%s,%s,%s,%s,%s)", (name,email,username,password,userRole))
            conn.commit()
            conn.close()
            flash('You are now registered and can log in', 'success')
            return redirect(url_for('login'))
        else:    
            conn.close()
            flash("Username already taken")
            return redirect(url_for('login'))
    return render_template('register.html', form=form)    

#User login
@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username= %s", [username]) #Get user by username
        result = cursor.fetchone()
        if result:
            password = result['password']
            userrole = result['userrole']
            if sha256_crypt.verify(password_candidate, password): #Compare passwords
                session['logged_in'] = True
                session['username'] = username
                if userrole == 'admin':
                    session['admin_role'] = True
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))    ##Change to index?
            else:
                flash("Invalid login")
                return render_template('login.html')        
            conn.close()
        else:      
            flash("Username not found")
            return render_template('login.html')       
    return render_template('login.html')    
         
#User Logout and clear session
@app.route('/logout')
def logout():
    flash("You are now logged out", 'success')
    session.clear()
    return redirect(url_for('login'))
#User dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
#Site index redirects to login
@app.route('/')
def index():
    if 'logged_in' in session: #If user is logged in, redirect to dashboard
        return redirect(url_for('dashboard'))
    return redirect(url_for('login')) #Send user to login if they are not logged in

@app.route('/posts')
@login_required
def view_posts():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM posts');
    posts = cursor.fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)

@app.route('/<int:post_id>')
@login_required
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
@admin_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)', (title, content));
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@admin_required
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
            cursor.execute('UPDATE posts SET title = %s, content = %s' ' WHERE id = %s', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)
    
@app.route('/<int:id>/delete', methods=('POST',))
@admin_required
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
@admin_required
def about():
    return render_template('about.html')

@app.route('/product')
@login_required
def view_product():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) product.asinid, product.picture, product.hazardous, product.description, product.oversized, bin.locationid \
    FROM product LEFT OUTER JOIN bin ON product.asinid=bin.asinid');
    products = cursor.fetchall()
    conn.close()
    return render_template('product.html', products=products)

@app.route('/product/<string:product_id>')
@login_required
def product(product_id):
    product = get_product(product_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT bin.contentid,bin.locationid, bin.asinid, bin.quantity, bin.datereceived, bin.expirationdate,physicallocation.shelfid, physicallocation.rackid, product.description FROM bin JOIN physicallocation ON bin.locationid=physicallocation.locationid JOIN product ON bin.asinid = product.asinid WHERE bin.asinid = %s ", (product_id,))
    locations = cursor.fetchall()                    
    conn.close()
    return render_template('product/view_product.html', product=product, locations=locations)   


@app.route('/product/create', methods=('GET', 'POST'))
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@login_required
def view_bin():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM physicallocation');
    bins = cursor.fetchall()
    conn.close()
    return render_template('bin/view_bins.html', bins=bins)    


@app.route('/contents/<string:trackingid>/receiving_tracking', methods=('GET', 'POST'))
@admin_required
def receiving_tracking(trackingid):
    received = "Yes"
    tobebinned = 1
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) orders.asinid, orders.store,orders.quantity,orders.ordernumber,tracking.ordernumber,tracking.trackingid,product.description FROM orders LEFT OUTER JOIN product ON orders.asinid = product.asinid LEFT OUTER JOIN tracking ON orders.ordernumber = tracking.ordernumber WHERE trackingid = %s', (trackingid,))
    results= cursor.fetchall()

    if request.method == 'POST':
        asinid = request.form['asinid']
        quantity = request.form['quantity']
        expirationdate = request.form['expirationdate']
        store = request.form['store']

        if not asinid and not quantity:
            flash('ASIN and Quantity are required!')  
            return redirect(url_for('receiving_tracking', trackingid=trackingid))
        elif not asinid:
            flash('ASIN is required!')  
            return redirect(url_for('receiving_tracking', trackingid=trackingid))
        elif not quantity:
            flash('Quantity is required!')  
            return redirect(url_for('receiving_tracking', trackingid=trackingid))
        cursor.execute('INSERT INTO bin (asinid,quantity,trackingid,expirationdate,store,tobebinned) VALUES (%s,%s,%s,%s,%s,%s)', ( asinid,quantity,trackingid,expirationdate,store,tobebinned,));
        cursor.execute('UPDATE tracking SET received= %s  WHERE trackingID = %s', (received,trackingid,))    
        conn.commit()    



        flash(str(store))
        flash("ASIN: " + str(asinid) + "of Quanity: " + str(quantity) + " have been added to bin screen with content id: " + "?" )    
        return redirect(url_for('start_receiving'))        
    return render_template('bin/contents/receiving1.html', results=results)

@app.route('/contents/start_receiving', methods=('GET', 'POST'))
@login_required
def start_receiving():
    if request.method == 'POST':
        trackingid = request.form['trackingid']
        if trackingid == None:
            return redirect(url_for('receiving_tracking', trackingid=trackingid))
        else:
            return redirect(url_for('receiving'))
        

    return render_template('bin/contents/start_receiving.html')   

@app.route('/contents/receiving', methods=('GET', 'POST'))
@admin_required
def receiving():
    received = "Yes"
    if request.method == 'POST':
        asinid = request.form['asinid']
        quantity = request.form['quantity']
        expirationdate = request.form['expirationdate']
        tobebinned = 1
        if not asinid:
            flash('ASIN is required!')   
        elif not quantity:
            flash('Quantity is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO bin (asinid, quantity, expirationdate,tobebinned) VALUES ( %s, %s, %s,%s)', 
                            (asinid, quantity, expirationdate,tobebinned));
            conn.commit()
            conn.close()
            flash("ASIN: " + asinid + " of quantity: " + quantity + " added to binning list")
            return redirect(url_for('receiving'))
    return render_template('bin/contents/receiving.html') 

@app.route('/contents/itemsToBin', methods=('GET', 'POST'))
@admin_required
def items_to_bin():
    tobebinned = 1
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) bin.contentid, bin.asinid, bin.quantity, bin.trackingid, product.description FROM bin LEFT OUTER JOIN product ON bin.asinid = product.asinid \
        WHERE tobebinned = %s', (tobebinned,));
    items = cursor.fetchall()
    if request.method == 'POST':
        tobebinned = 0
        binlocation = request.form['binlocation']
        contentid = request.form['contentid'] 
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT locationid FROM physicallocation WHERE locationid = %s', (binlocation,))
        results = cursor.fetchone()
        if results:
            cursor.execute('UPDATE bin SET (locationid, tobebinned ) = (%s,%s) WHERE contentid = %s', (binlocation, tobebinned, contentid,))
        else:
            flash("That bin does not exist!")
            return redirect(url_for('items_to_bin'))   
        conn.commit()
        conn.close()
        flash("Item binned into location " + binlocation)
        return redirect(url_for('items_to_bin'))
    conn.close()
    return render_template('bin/contents/itemsToBin.html', items=items) 

@app.route('/bin/contents/<int:contents_id>/missing', methods=('GET', 'POST'))
@admin_required
def missing(contents_id):
    if request.method == 'POST':
        damaged = request.form['damaged']
        missing = request.form['missing']
        if damaged == '':
            damaged=0
        elif missing == '':
            missing=0
        elif damaged == '' and missing =='':
            flash('No input was given')   
            return redirect(url_for('items_to_pick'))   
        flash("Damaged: " + str(damaged) + ' Missing: ' + str(missing))   
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('UPDATE bin SET (damaged,missing) = (%s,%s) WHERE contentid=%s', (damaged,missing,contents_id,))
        conn.commit()
        conn.close()
        flash("Item information has been sent to admin panel")
        return redirect(url_for('items_to_pick')) 
    return render_template('bin/contents/missing.html') 
 

@app.route('/bin/contents/<int:contents_id>/removePick', methods=('POST',))
@admin_required
def remove_pick(contents_id):
    tobepicked = 0
    contents = get_contents(contents_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('UPDATE bin SET tobepicked = %s WHERE contentid = %s', (tobepicked, contents_id,))
    conn.commit()
    conn.close()
    flash("Pick removed from system")
    return redirect(url_for('items_to_pick'))  


@app.route('/contents/itemsToPick', methods=('GET', 'POST'))
@admin_required
def items_to_pick():
    tobepicked = 1
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) bin.contentid, bin.asinid, bin.quantity, bin.trackingid, bin.locationid, bin.pickquantity, product.description FROM bin LEFT OUTER JOIN product ON bin.asinid = product.asinid \
        WHERE tobepicked = %s', (tobepicked,));
    items = cursor.fetchall()

    
    if request.method == 'POST' :
        


        tobepicked= 0
        pick_quantity = request.form['quantity']
        contentid = request.form['contentid']
        db_quantity = 0
        for item in items:
            if int(contentid) == int(item['contentid']) :
                db_quantity = item['quantity']
        if pick_quantity == '':
            flash("Cannot pick 0!")
            conn.close()
            return redirect(url_for('items_to_pick'))     
        elif int(pick_quantity) <=0:
            flash("Cannot pick 0 or less!")
            conn.close()
            return redirect(url_for('items_to_pick')) 
        elif int(pick_quantity) > db_quantity:
            flash("Cannot pick more than what's in the bin!")
            conn.close()
            return redirect(url_for('items_to_pick'))
             
        newQuantity = (db_quantity - int(pick_quantity))
        if newQuantity > 0:
            cursor.execute('UPDATE bin SET (pickquantity, tobepicked, quantity ) = (%s,%s,%s) WHERE contentid = %s', (0, tobepicked, newQuantity, contentid,))
            conn.commit()
            flash("Partial Items picked from pick list: " + pick_quantity + " where contentid is: " + contentid)   
            conn.close()
            return redirect(url_for('items_to_pick'))
        elif newQuantity == 0:
            cursor.execute('DELETE FROM bin WHERE contentid = %s', (contentid,))    
            conn.commit()
            flash("All items from the content id were removed from bin with a pick quantity of: " + pick_quantity + " where contentid is: " + contentid)   
            conn.close()
            return redirect(url_for('items_to_pick'))
        else:
            flash("ERROR! Issue with updating quantity") 
            conn.close()
            return redirect(url_for('items_to_pick'))
    return render_template('bin/contents/itemstopick.html', items=items) 


@app.route('/contents/view_items', methods=('GET', 'POST') )
@admin_required
def view_items():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) bin.contentid, bin.locationid, bin.asinid, bin.quantity,bin.datereceived, bin.expirationdate, bin.trackingid, bin.store, bin.tobepicked, product.description FROM bin LEFT OUTER JOIN product ON bin.asinid = product.asinid ');
    items = cursor.fetchall()
    if request.method == 'POST':
        tobepicked = 1
        quantity = request.form['quantity']
        contentid = request.form['contentid']
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT quantity FROM bin WHERE contentid = %s', (contentid,))
        results = cursor.fetchone()
        if quantity == '':
            flash("Cannot pick 0!")
            conn.close()
            return redirect(url_for('view_items'))     
        elif int(quantity) <=0:
            flash("Cannot pick 0 or less!")
            conn.close()
            return redirect(url_for('view_items'))  
        elif int(quantity) > results['quantity']:
            flash("Cannot pick more than what's in the bin!")
            conn.close()
            return redirect(url_for('view_items'))   
        cursor.execute('UPDATE bin SET (pickquantity, tobepicked ) = (%s,%s) WHERE contentid = %s', (quantity, tobepicked, contentid,))
        conn.commit()
        flash("Item added to picklist with quantity: " + quantity + " where contentid is: " + contentid)
    conn.close()
    return render_template('bin/contents/view_items.html', items=items) 

@app.route('/bin/contents/<int:contents_id>')
@login_required
def contents_id(contents_id):
    contents = get_contents(contents_id)
    return render_template('bin/contents/contents.html', contents=contents)

@app.route('/bin/contents/<int:contents_id>/delete', methods=('POST',))
@admin_required
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
@admin_required
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
@login_required
def bin_id(bin_id):
    bin = get_bin(bin_id)
    return render_template('bin/bin.html', bin=bin)

@app.route('/bin/<int:bin_id>/edit', methods=('GET', 'POST'))
@admin_required
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
@admin_required
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
@admin_required
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
        description = request.form['description']
        
        if not asinid:
            flash('asinid is required!')
        if not fullfillment:
            flash('fullfillment is required! Or select N/A')    
        else:
            if not buyPrice:    
                buyPrice = None
            if not sellPrice:
                sellPrice = None
            if not quantity:
                sellPrice = None
            if not orderNumber:
                orderNumber = None
            if not quantity:
                quantity = None
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('INSERT INTO product (asinid, description) VALUES (%s, %s) ON CONFLICT (asinid) DO UPDATE SET (asinid,description) = (%s,%s)', (asinid, description,asinid, description,)); #Change DO NOTHING to update when I add other product columns
            conn.commit()
            cursor.execute('INSERT INTO orders (asinid, buyPrice, sellPrice, store, supplier,quantity,orderNumber,fullfillment,buyer) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                         (asinid, buyPrice, sellPrice, store, supplier,quantity,orderNumber,fullfillment,buyer,));
            conn.commit()
            conn.close()
            return redirect(url_for('view_orders'))
    return render_template('orders/create.html') 

@app.route('/orders/<int:order_id>')
@login_required
def order_id(order_id):
    order = get_order(order_id)
    return render_template('orders/order.html', order=order)

@app.route('/orders/view_orders')
@login_required
def view_orders():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT DISTINCT ON (1) orders.invid, orders.asinid, orders.datePurchased, orders.buyPrice, orders.sellPrice, orders.store, orders.supplier, orders.quantity, orders.orderNumber, orders.fullfillment, orders.buyer, bin.locationid, tracking.trackingid, product.description FROM orders LEFT OUTER JOIN bin ON orders.asinid = bin.asinid LEFT OUTER JOIN tracking ON orders.invid = tracking.invid LEFT OUTER JOIN product ON orders.asinid = product.asinid");
    orders = cursor.fetchall()
    conn.close()
    return render_template('orders/view_orders.html', orders=orders) 

@app.route('/orders/<int:order_id>/delete', methods=('POST',))
@admin_required
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
@admin_required
def order_edit(order_id):
    order = get_order(order_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM orders WHERE invid = %s', (order_id,));
    values = cursor.fetchone()
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
        if buyPrice == '':
            buyPrice= request.form.getlist('buyPrice')[0]
        if not asinid:
            flash("Enter an ASIN!")
        else:
            if not buyPrice:    
                buyPrice = None
            if not sellPrice:
                sellPrice = None
            if not quantity:
                sellPrice = None
            if not orderNumber:
                orderNumber = None
            if not quantity:
                quantity = None
            cursor.execute('UPDATE orders SET asinid = %s, buyPrice = %s, sellPrice = %s, store = %s, supplier = %s, quantity = %s, orderNumber = %s, fullfillment = %s, buyer = %s' ' WHERE invid = %s', 
                         (asinid, buyPrice, sellPrice, store, supplier,quantity,orderNumber,fullfillment,buyer, order[0]));
            conn.commit()
            conn.close()
            return redirect(url_for('view_orders')) 

    return render_template('orders/edit.html', order=order, values=values) 










@app.route('/tracking')
@login_required
def view_tracking():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) tracking.id, tracking.trackingid, tracking.invid, tracking.received, tracking.ordernumber, trackingcontents.trackeditem,trackingcontents.asinid, trackingcontents.quantity FROM tracking LEFT OUTER JOIN \
    trackingcontents ON tracking.trackingid = trackingcontents.trackingid')
    trackingNums = cursor.fetchall()
    conn.close()
    return render_template('tracking/tracking.html', trackingNums=trackingNums)

@app.route('/tracking/<int:order_id>/trackingList')
@login_required
def view_tracking_list(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT DISTINCT ON (1) tracking.id, tracking.trackingid, tracking.invid, tracking.received, trackingcontents.trackeditem,trackingcontents.asinid, trackingcontents.quantity FROM tracking LEFT OUTER JOIN \
    trackingcontents ON tracking.trackingid = trackingcontents.trackingid WHERE tracking.invid = %s', (order_id,))
    trackingNums = cursor.fetchall()
    conn.close()
    return render_template('tracking/trackingList.html', trackingNums=trackingNums)

@app.route('/tracking/<string:tracking_id>')  #Being used by viewing tracking number page but could be removed if tweaked
@login_required
def tracking(tracking_id):
    trackingNum = get_tracking(tracking_id)
    
                        #Need to add the tracking contents of each tracking number
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT DISTINCT ON (1) trackingcontents.invid, trackingcontents.asinid, trackingcontents.quantity, tracking.ordernumber,product.description FROM trackingcontents LEFT OUTER JOIN tracking ON tracking.trackingid = trackingcontents.trackingid \
    LEFT OUTER JOIN product ON product.asinid = trackingcontents.asinid WHERE tracking.trackingid = %s  ", (tracking_id,))
    #cursor.execute("SELECT DISTINCT ON (1) trackingcontents.invid, trackingcontents.asinid, trackingcontents.quantity, tracking.ordernumber FROM trackingcontents LEFT OUTER JOIN tracking ON tracking.trackingid = trackingcontents.trackingid WHERE tracking.trackingid = %s ", (tracking_id,))
    locations = cursor.fetchall()                    
    conn.close()
    return render_template('tracking/view_tracking.html', locations=locations, trackingNum=trackingNum)   


@app.route('/tracking/<int:order_id>/create', methods=('GET', 'POST'))
@admin_required
def tracking_create(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT orderNumber FROM orders WHERE invid = %s', (order_id,))
    result = cursor.fetchone()

    if request.method == 'POST':
        trackingid = request.form['trackingid']
        invid = order_id
        
        if not trackingid:
            flash('Tracking Number is required!')
        else:
            
            cursor.execute('select * from orders where ordernumber = %s',  (result['ordernumber'],));
            orders = cursor.fetchall()
            for order in orders:
                cursor.execute('INSERT INTO tracking (trackingid, invid, ordernumber) VALUES (%s, %s,%s)', 
                         (trackingid, order['invid'], order['ordernumber'],));
            conn.commit()      
            conn.close()
            flash("Entry added! Add more or return to view orders page")
            return redirect(url_for('tracking_create', order_id=invid)) 
    return render_template('tracking/create.html', result=result)  

       
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM orders WHERE invid = %s', (order_id,));
    values = cursor.fetchone()

@app.route('/tracking/<string:tracking_id>/edit', methods=('GET', 'POST'))
@admin_required
def tracking_edit(tracking_id):
    tracking = get_tracking(tracking_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM tracking WHERE trackingid = %s', (tracking_id,));
    values = cursor.fetchone()

    if request.method == 'POST':
        trackingid = request.form['trackingid']
        ordernumber = request.form['ordernumber']
        received = request.form['received']

        cursor.execute('UPDATE tracking SET (trackingid, ordernumber, received) = (%s,%s,%s) WHERE trackingid = %s', 
                         (trackingid, ordernumber, received, tracking_id,));
        conn.commit()
        conn.close()
        return redirect(url_for('view_tracking')) 

    return render_template('tracking/edit.html', tracking=tracking,values=values)        

 
@app.route('/tracking/<string:tracking_id>/delete', methods=('POST',))
@admin_required
def tracking_delete(tracking_id):
    tracking = get_tracking(tracking_id)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('DELETE FROM tracking WHERE trackingid = %s', (tracking_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(tracking['trackingid']))
    return redirect(url_for('view_tracking'))

@app.route('/tracking/<string:tracking_id>/addto/<int:order_id>', methods=('GET', 'POST'))
@admin_required
def tracking_addto(tracking_id,order_id):
    if request.method == 'POST':
        asinid = request.form['asinid']
        quantity = request.form['quantity'] 
        
        if not asinid:
            flash('ASIN is required!')
        elif not quantity:
            flash('Quantity is required!')    
        elif isinstance(quantity,int):
            flash('Quantity cannot have letters!')      

        else:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute('SELECT store FROM orders WHERE invid =%s', (order_id,))
            result = cursor.fetchone()
            cursor.execute('INSERT INTO trackingcontents (trackingid,asinid, quantity,invid,store) VALUES (%s, %s, %s,%s,%s) ', 
                         (tracking_id, asinid, quantity,order_id,result['store']));
            conn.commit()
            conn.close()
            return redirect(url_for('view_tracking'))
    return render_template('tracking/addto.html')      
   