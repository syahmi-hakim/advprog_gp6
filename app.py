from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Sample data (replace with a database in a production environment)
users = {}
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1", "price": 20.0},
    {"id": 2, "title": "Book 2", "author": "Author 2", "price": 25.0},
    {"id": 3, "title": "Book 3", "author": "Author 3", "price": 30.0},
]

# Routes

@app.route('/')
def index():
    search_query = request.args.get('q', '')
    filtered_books = filter_books(books, search_query)
    return render_template('index.html', books=filtered_books, search_query=search_query)

def filter_books(all_books, search_query):
    """Filter books based on the search query."""
    if search_query:
        return [book for book in all_books if search_query.lower() in book['title'].lower() or search_query.lower() in book['author'].lower()]
    else:
        return all_books

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            if username not in users:
                users[username] = {"password": password, "cart": []}
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username already exists. Please choose another.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username]["password"] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Logout successful!', 'success')
    return redirect(url_for('index'))

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'logged_in' in session and session['logged_in']:
        book = next((b for b in books if b['id'] == book_id), None)
        if book:
            users[session['username']]["cart"].append(book)
            flash(f'{book["title"]} added to your cart!', 'success')
        else:
            flash('Book not found.', 'danger')
    else:
        flash('Please log in to add items to your cart.', 'danger')

    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    if 'logged_in' in session and session['logged_in']:
        user_cart = users[session['username']]["cart"]
        return render_template('cart.html', cart=user_cart)
    else:
        flash('Please log in to view your cart.', 'danger')
        return redirect(url_for('login'))

@app.route('/purchase')
def purchase():
    if 'logged_in' in session and session['logged_in']:
        user_cart = users[session['username']]["cart"]
        total_price = sum(book["price"] for book in user_cart)
        users[session['username']]["cart"] = []
        flash(f'Purchase successful! Total: ${total_price}', 'success')
    else:
        flash('Please log in to make a purchase.', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
