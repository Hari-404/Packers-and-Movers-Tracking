import sys
import heapq

class Vertex:
	def __init__(self, node):
		self.id = node
		self.adjacent = {}
		self.distance = sys.maxsize
		self.visited = False  
		self.previous = None
		
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.distance == other.distance
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, self.__class__):
			return self.distance < other.distance
		return NotImplemented
		
	def __hash__(self):
		return id(self)

	def add_neighbor(self, neighbor, weight=0):
		self.adjacent[neighbor] = weight

	def get_connections(self):
		return list(self.adjacent.keys())  

	def get_id(self):
		return self.id

	def get_weight(self, neighbor):
		return self.adjacent[neighbor]

	def set_distance(self, dist):
		self.distance = dist

	def get_distance(self):
		return self.distance

	def set_previous(self, prev):
		self.previous = prev

	def set_visited(self):
		self.visited = True

	def __str__(self):
		return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
	def __init__(self):
		self.vert_dict = {}
		self.num_vertices = 0

	def __iter__(self):
		return iter(list(self.vert_dict.values()))

	def add_vertex(self, node):
		self.num_vertices = self.num_vertices + 1
		new_vertex = Vertex(node)
		self.vert_dict[node] = new_vertex
		return new_vertex

	def get_vertex(self, n):
		if n in self.vert_dict:
			return self.vert_dict[n]
		else:
			return None

	def add_edge(self, frm, to, cost = 0):
		if frm not in self.vert_dict:
			self.add_vertex(frm)
		if to not in self.vert_dict:
			self.add_vertex(to)

		self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
		self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

	def get_vertices(self):
		return list(self.vert_dict.keys())

	def set_previous(self, current):
		self.previous = current

	def get_previous(self, current):
		return self.previous

def shortest(v, path):
	if v.previous:
		path.append(v.previous.get_id())
		shortest(v.previous, path)
	return



def dijkstra(aGraph, start, target):
	start.set_distance(0)

	unvisited_queue = [(v.get_distance(),v) for v in aGraph]
	heapq.heapify(unvisited_queue)

	while len(unvisited_queue):
		uv = heapq.heappop(unvisited_queue)
		current = uv[1]
		current.set_visited()

		for next in current.adjacent:
			if next.visited:
				continue
			new_dist = current.get_distance() + current.get_weight(next)
			
			if new_dist < next.get_distance():
				next.set_distance(new_dist)
				next.set_previous(current)
		while len(unvisited_queue):
			heapq.heappop(unvisited_queue)
		unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
		heapq.heapify(unvisited_queue)



neighbour = {'Andhra Pradesh': ['Karnataka', 'Odisha', 'Tamil Nadu', 'Telangana'],
'Arunachal Pradesh': ['Assam', 'Nagaland'], 
'Assam': ['Arunachal Pradesh', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Tripura', 'West Bengal'], 
'Bihar': ['Uttar Pradesh', 'West Bengal', 'Jharkhand'], 
'Chhattisgarh': ['Jharkhand', 'Madhya Pradesh', 'Maharashtra', 'Odisha', 'Telangana', 'Uttar Pradesh'], 
'Goa': ['Maharashtra', 'Karnataka'], 
'Gujarat': ['Madhya Pradesh', 'Maharashtra', 'Rajasthan'], 
'Haryana': ['Himachal Pradesh', 'Rajasthan', 'Uttar Pradesh'], 
'Himachal Pradesh': ['Haryana', 'Punjab', 'Uttar Pradesh', 'Uttarakhand'], 
'Jharkhand': ['Bihar', 'Chhattisgarh', 'Odisha', 'Uttar Pradesh', 'West Bengal'], 
'Karnataka': ['Andhra Pradesh', 'Goa', 'Kerala', 'Maharashtra', 'Tamil Nadu', 'Telangana'], 
'Kerala': ['Karnataka', 'Tamil Nadu'], 
'Madhya Pradesh': ['Chhattisgarh', 'Gujarat', 'Maharashtra', 'Rajasthan', 'Uttar Pradesh'], 
'Maharashtra': ['Chhattisgarh', 'Goa', 'Gujarat', 'Karnataka', 'Madhya Pradesh', 'Telangana'], 
'Manipur': ['Nagaland', 'Mizoram', 'Assam'], 
'Meghalaya': ['Assam'], 
'Mizoram': ['Assam', 'Manipur', 'Tripura'], 
'Nagaland': ['Arunachal Pradesh', 'Assam', 'Manipur'], 
'Odisha': ['West Bengal', 'Jharkhand', 'Chhattisgarh', 'Andhra Pradesh', ], 
'Punjab': ['Rajasthan', 'Himachal Pradesh'], 
'Rajasthan': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat'], 
'Sikkim': ['West Bengal'], 
'Tamil Nadu': ['Andhra Pradesh', 'Karnataka', 'Kerala'], 
'Telangana': ['Andhra Pradesh', 'Chhattisgarh', 'Karnataka', 'Maharashtra'], 
'Tripura': ['Assam', 'Mizoram'], 
'Uttar Pradesh': ['Bihar', 'Chhattisgarh', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Madhya Pradesh', 'Rajasthan', 'Uttarakhand'], 
'Uttarakhand': ['Himachal Pradesh', 'Uttar Pradesh'], 
'West Bengal': ['Odisha', 'Jharkhand', 'Bihar', 'Sikkim', 'Assam']}

def load_graph(conn):
	country_graph = Graph()
	for key in neighbour:
		query = 'SELECT capital from states where state="{}"'.format(key)
		src = conn.execute(query).fetchall()[0][0]
		country_graph.add_vertex(src)
		for v in neighbour[key]:
			query = 'SELECT capital from states where state="{}"'.format(v)
			dst = conn.execute(query).fetchall()[0][0]
			query = 'SELECT dis from distance where src="{}" and dst="{}"'.format(src, dst)
			dis = conn.execute(query).fetchall()[0][0]
			country_graph.add_edge(src, dst, dis)
	return country_graph



def find_short(src, dst, g, conn):
	query = 'SELECT tierlist.state, capital, city, tier from tierlist join states on tierlist.state=states.state where tierlist.city="{}"'.format(src)
	src = conn.execute(query).fetchall()[0]
	# print(src)

	query = 'SELECT tierlist.state, capital, city, tier from tierlist join states on tierlist.state=states.state where tierlist.city="{}"'.format(dst)
	dst = conn.execute(query).fetchall()[0]
	# print(dst)

	dijkstra(g, g.get_vertex(src[1]), g.get_vertex(dst[1])) 

	target = g.get_vertex(dst[1])
	path = [target.get_id()]
	shortest(target, path)
	path, total_dis = path[::-1], target.get_distance()

	final_path = []

	if src[3] == 2:
		# print(src[2], end=" ")
		final_path.append(src[2])
		query = 'SELECT dis FROM distance WHERE src="{}" AND dst="{}"'.format( src[2], src[1] )
		total_dis = total_dis + conn.execute(query).fetchall()[0][0]

	for city in path:
		# print(city, end=" ")
		final_path.append(city)
	# print(path, total_dis)
		
	if dst[3] == 2:
		# print(dst[2], end=" ")
		final_path.append(dst[2])
		query = 'SELECT dis FROM distance WHERE src="{}" AND dst="{}"'.format( dst[1], dst[2] )
		total_dis = total_dis + conn.execute(query).fetchall()[0][0]
	# print()
	# print('Total distance = ', total_dis)
	t = estm_time(total_dis)
	return (final_path, total_dis, t)

def estm_time(dis):
    temp = dis / 1000
    # print(temp)
    days = int(temp)
    hours = 24 * (temp - int(temp))
    if hours <= 12:
        hours = 12
    else:
        days = days + 1
        hours = 0
    return str(days) + "D:" + str(hours) + "H"
    # print(days, hours, sep=" ")
