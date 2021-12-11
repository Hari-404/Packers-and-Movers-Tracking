class Admin:
	def __init__(self, conn):
		self.conn = conn

	def get_orders(self):
		return self.conn.execute('SELECT * from orders').fetchall()

	def change_status(self, track_id):
		self.conn.execute("update orders set status=1 where orderid={}".format(track_id))
		self.conn.commit()

	def move_package(self, track_id):
		self.result = self.conn.execute("SELECT path, status from orders where orderid={}".format(track_id)).fetchall()[0]
		self.status = self.result[1]
		if self.status == '0':
			self.path = self.result[0].split('-')
			self.status = self.path[0]
		elif self.status != '1':
			self.path = self.result[0].split('-')
			self.index = self.path.index(self.status) + 1
			if self.index < len(self.path):
				self.status = self.path[self.index]
			else:
				self.status = '1'
		self.conn.execute("update orders set status='{}' where orderid={}".format(self.status, track_id))
		self.conn.commit()
