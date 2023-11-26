from flask import *
from customer import Customer
from admin import Admin
from database import Database
import copy
from dijkstra import load_graph, find_short

conn = Database().connect()

customer = Customer(conn)

admin = Admin(conn)

graph = load_graph(conn)

app = Flask(__name__)

# Customer Login -> Home page
@app.route('/login', methods = ['POST'])
def login():
	uname=request.form['uname']
	password=request.form['pass']
	if customer.login(uname, password):
		return render_template("home.html")
	return "Invalid details"

# *Admin Login -> admin home page
@app.route('/admin_login', methods = ['POST'])
def admin_login():
	result = admin.get_orders()
	return render_template("admin_page.html", data=result)

# Admin changes order status
@app.route('/change_status', methods = ['POST'])
def change_status():
	order_id=request.form['orderid']
	admin.change_status(order_id)
	result = admin.get_orders()
	return render_template("admin_page.html", data=result)

# Admin move package to next city
@app.route('/move_package', methods = ['POST'])
def move_package():
	order_id=request.form['orderid']
	admin.move_package(order_id)
	result = admin.get_orders()
	return render_template("admin_page.html", data=result)

# Customer signup
@app.route('/signup', methods = ['POST'])
def signup():
	email=request.form['email']
	password=request.form['password']
	if customer.signup(email, password):
		return "Success"
	return "Invalid details"

#Signup page
@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return render_template("signup.html")

# Customer View all orders
@app.route('/get_all', methods=['POST'])
def view_orders():
	result = customer.get_all_orders()
	return render_template('results.html', data=result)

# Customer Show one order
@app.route('/show_order', methods=['POST'])
def show_order():
	order_id = int(request.form['orderid'])
	result = customer.show_order(order_id)
	return render_template('results.html', data=result)

# Customer Show one order
@app.route('/show_order_page', methods=['POST'])
def show_order_page():
	return render_template('results.html')

# Customer places an order
@app.route('/order', methods = ['POST'])
def order():
	src=request.form['city']
	dst=request.form['dstcity']
	print(src, dst, sep="+")
	path, total_dis, estimate_time = find_short(src, dst, copy.deepcopy(graph), conn)
	print(path, total_dis, estimate_time)
	temp_path = ''
	for i in path[:-1]:
		temp_path = temp_path + i + "-"
	temp_path += path[-1]
	track_id = customer.order(src, dst, temp_path, estimate_time)
	return 'Track ID : ' + str(track_id)

# Load index page->Login page -> cusomer login, Admin login
@app.route('/', methods=['GET'])
def home():
	return render_template("index.html")
	# return render_template("home.html")

if __name__ == '__main__':
 app.run(debug = True) 
