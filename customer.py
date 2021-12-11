import uuid
import re

class Customer:

	def __init__(self, conn):
		self.conn = conn

	def signup(self, user_name, password):
		"""
		Customer signup
		"""
		self.regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
		if re.match(self.regex, user_name):
			self.conn.execute('INSERT INTO customer VALUES("{}", "{}", "{}")'.format(int(str(abs(int(hash(user_name))))[:4]), user_name, password))
			self.conn.commit()
			return True
		else:
			return False

	def login(self, user_name, password):
		"""
		Customer Login
		"""
		self.result = self.conn.execute('SELECT customerid from customer where username="{}" and password="{}"'.format(user_name, password)).fetchall()
		if len(self.result) == 1:
			self.customer_id = self.result[0][0]
			return True
		else :
			return False

	def order(self, src, dst, path, time):
		"""
		Customer makes and order
		"""
		self.track_id = int(str(abs(int(uuid.uuid1())))[:5])
		self.conn.execute('INSERT INTO orders VALUES("{}", "{}", "{}", "{}", "{}", "{}", 0)'.format(self.customer_id, self.track_id, src, dst, path, time))
		self.conn.commit()
		return self.track_id

	def get_all_orders(self, status=0):
		"""
		Cusotmer view his orders
		"""
		return self.conn.execute('SELECT * from orders where customerid={} '.format(self.customer_id)).fetchall()


	def show_order(self, id, status=0):
		"""
		Cusotmer view his orders
		"""
		return self.conn.execute('SELECT * from orders where customerid={} and orderid={}'.format(self.customer_id, id)).fetchall()
