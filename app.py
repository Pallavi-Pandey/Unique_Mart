from flask import Flask, render_template, redirect, url_for, request, flash
from models import *
from models import db
import secrets
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BigMart.sqlite3'
# db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.config['SECRET_KEY'] = 'Pallavi'



with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes

# Admin dashboard page (accessible to admins only after login)
@app.route('/admin/home')
@login_required
def admin_home():
    existing_category = Category.query.all()
    print(existing_category)
    # return "admin home"
    return render_template('admin_home1.html',data=existing_category)

@app.route("/delete_category/<cat_id>", methods=['GET'])
@login_required
def delete_cat(cat_id):
    db.session.delete(Category.query.filter_by(id=cat_id).first())
    db.session.commit()
    return redirect("/admin/home")


@app.route("/edit_category/<cat_id>", methods=['GET', 'POST'])
@login_required
def edit_cat(cat_id):
    cat= Category.query.filter_by(id=cat_id).first()
    if request.method=='POST':
        category_name = request.form['category_name']
        cat.name=category_name
        db.session.add(cat)
        db.session.commit()
        return redirect("/admin/home")
    
    print(cat)
    return render_template('edit_category.html', data=cat)

@app.route("/view_category/<cat_id>", methods=['GET'])
@login_required
def view_cat(cat_id):
    cat= Category.query.filter_by(id=cat_id).first()
    products=Product.query.filter_by(category_id=cat_id).all()
    print(cat)
    print(products)
    return render_template('view_cat.html', cat=cat, products=products)


# Add Category page (accessible to admins only after login)
@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category_name = request.form['category_name']

        # Check if the category already exists in the database
        existing_category = Category.query.filter_by(name=category_name).first()
        if existing_category:
            return render_template('add_category.html',error="Category already exist")
        else:
            # Create a new category
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash("Category added successfully.", 'success')
            return redirect("/admin/home")


    return render_template('add_category.html')

# All products page (visible to all users)
@app.route('/all_products', methods=['GET'])
@login_required
def all_products():
    category_id = request.args.get('category')
    if category_id == 'all':
        products = Product.query.all()
    elif category_id:
        products = Product.query.filter_by(category_id=category_id).all()
    else:
        products = []

    categories = Category.query.all()
    return render_template('all_products.html', products=products, categories=categories)

@app.route("/edit_product",methods=['GET', 'POST'])
@login_required
def edit_product():

    if request.method=='POST':
        return "hi"
    return render_template("edit_product.html")

# Add Product page (accessible to admins only after login)
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():

    if request.method == 'POST':
        product_name = request.form['product_name']
        price = float(request.form['price'])
        manufacture_date = datetime.strptime(request.form['manufacture_date'], '%Y-%m-%d')
        expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')
        category_id = int(request.form['category'])
        quantity = int(request.form['quantity'])
        image_link = request.form['image_link']

        category = Category.query.get(category_id)
        if not category:
            return "Invalid category selected."

        new_product = Product(
            product_name=product_name,
            price=price,
            manufacture_date=manufacture_date,
            expiry_date=expiry_date,
            category=category,
            quantity=quantity,
            image_link=image_link
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect("/view_category/"+str(category_id))
    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)



# User signup page
@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name=request.form['username']

        # Check if the user already exists in the database 
        existing_user = User.query.filter_by(email=email).first()
        if existing_user: 
            return "User already exists. Please log in instead."

        # Create a new user
        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()

        # Log in the user after successful signup
        login_user(new_user)
        return redirect(url_for('all_products'))

    return render_template('user_signup.html')

# User login page
@app.route('/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if not user or not user.password == password:
            return "Invalid email or password."

        # Log in the user
        login_user(user)
        return redirect(url_for('all_products'))

    return render_template('user_login.html')


# Admin signup page
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        # Check if the admin already exists in the database
        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            return "Admin already exists. Please log in instead."

        # Create a new admin
        new_admin = Admin(email=email, password=password, username=username)
        db.session.add(new_admin)
        db.session.commit()

        # Log in the admin after successful signup
        login_user(new_admin)
        return redirect(url_for('admin_home'))

    return render_template('admin_signup.html')

# Admin login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the admin exists in the database
        admin = Admin.query.filter_by(email=email).first()
        if not admin or not admin.password == password:
            return "Invalid email or password."

        # Log in the admin
        login_user(admin)
        return redirect(url_for('admin_home'))

    return render_template('admin_login.html')


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login'))


# Run the app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port = 5600)
