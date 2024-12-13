import csv

#Simple Chaining Hash Table
class ChainingHashTable:
    def __init__(self, initial_capacity=16):
        self.table = []
        #self.num = 5
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                n[1] = item
                return True

        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                return n[1]
        return None


    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for n in bucket_list:
            if n[0] == key:
                bucket_list.remove([n[0], n[1]])

class Package:
    def __init__(self, ID, addr, city, zipcode, deadline,  weight, status):
        self.ID = ID
        self.addr = addr
        self.city = city
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.ID, self.addr, self.city, self.zipcode,self.deadline, self.weight, self.status)

class Vertex:
    # Constructor for a new Vertx object. All vertex objects
    # start with a distance of positive infinity.
    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.pred_vertex = None

    def __str__(self):
        return f'{self.label} {self.distance} pred: {self.pred_vertex}'

class Graph:
    def __init__(self):
        self.adjacency_list = {}  # vertex dictionary {key:value}
        self.edge_weights = {}  # edge dictionary {key:value}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []  # {vertex_1: [], vertex_2: [], ...}

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        # {(vertex_1,vertex_2): 484, (vertex_1,vertex_3): 626, (vertex_2,vertex_6): 1306, ...}
        self.adjacency_list[from_vertex].append(to_vertex)
        # {vertex_1: [vertex_2, vertex_3], vertex_2: [vertex_6], ...}

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

#Populate hash table with package CSV contents
def loadPackageCSV(filename):
    with open(filename) as PackageCSV:
        packageData = csv.reader(PackageCSV, delimiter=',')
        next(packageData)
        for package in packageData:
            pID = int(package[0])
            pAddr = package[1]
            pCity = package[2]
            pZipCode = package[4]
            pDeadLine = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            package = Package(pID, pAddr, pCity,  pZipCode, pDeadLine, pWeight,  pStatus)

            myHash.insert(pID, package)

city_arr2 = []
weight_arr2 = []
# load the distance table contents into the empty arrays
def loadDistanceTableCSV(filename):
    with open(filename) as DistanceTableCSV:
        distanceTableData = csv.reader(DistanceTableCSV, delimiter=',')
        next(distanceTableData)
        for distance in distanceTableData:
            #print(distance[1])
            city_arr2.append(distance[1])
            weight_arr2.append(distance[2:len(distance)])

def packageLookUp(ID):
    return myHash.search(ID)

#Dijktra's algorithm
def dijkstra_shortest_path(g, start_vertex):
    # Put all vertices in an unvisited queue.
    unvisited_queue = []

    for current_vertex in g.adjacency_list:
        unvisited_queue.append(current_vertex)
        # unvisited_queue = [vertex_1, vertex_2, ...]

    # Start_vertex has a distance of 0 from itself
    start_vertex.distance = 0

    # One vertex is removed with each iteration; repeat until the list is
    # empty.
    while len(unvisited_queue) > 0:

        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            # print(unvisited_queue[i].label, unvisited_queue[i].distance, unvisited_queue[i].pred_vertex)
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)
        # print("From Start Vetex to current_vertex.label: " + current_vertex.label +" distance: " + str(current_vertex.distance))

        # Check potential path lengths from the current vertex to all neighbors.
        for adj_vertex in g.adjacency_list[current_vertex]:  # values from  dictionary
            # if current_vertex = vertex_1 => adj_vertex in [vertex_2, vertex_3], if vertex_2 => adj_vertex in [vertex_6], ...
            edge_weight = g.edge_weights[(current_vertex, adj_vertex)]  # values from dictionary
            # edge_weight = 484 then 626 then 1306, ...}
            alternative_path_distance = current_vertex.distance + edge_weight

            # If shorter path from start_vertex to adj_vertex is found, update adj_vertex's distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex

#get shortest path between two verteces
def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    #print(start_vertex.label, end_vertex.label)
    ctr = 0

    current_vertex = end_vertex
    '''and current_vertex is not None'''
    while current_vertex is not start_vertex:
        #print('\t',ctr, '\t', current_vertex)
        path = " -> " + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
        ctr += 1
    path = start_vertex.label + path
    #print('\t', path)
    return path

myHash = ChainingHashTable()

loadPackageCSV("PackageCSV.csv")

loadDistanceTableCSV("DistanceTableCSV.csv")

g = Graph()

vertex_arr = []

#adding all from the distance table vertices to graph
for i in range(0, len(city_arr2)):
    vertex_arr.append(Vertex(city_arr2[i].replace('\n', ' ')))
    g.add_vertex(vertex_arr[i])

#adding undirected edge between two vertices
for i in range(0, len(vertex_arr)):
    for j in range(i + 1, len(vertex_arr)):
        g.add_undirected_edge(vertex_arr[i], vertex_arr[j], float(weight_arr2[j][i]))

def getDistanceBetween2Cities(start, end):
    if(start <= end):
        return weight_arr2[end][start]
    else:
        return 'ERROR::make sure start is less than or equal to end'

def getMinimumDistanceBetween2Cities(start, end):
    #print("Start", start)
    #print("End", end)
    vertex_1 = vertex_arr[start]
    dijkstra_shortest_path(g, vertex_1)
    get_shortest_path(vertex_arr[start], vertex_arr[end])

    if(start <= end):
        return vertex_arr[end].distance
    else:
        return 'ERROR::make sure start is less than or equal to end'

# This is a dummy array that holds package IDs. Essentially I am trying to create a shortest path chain
# that will start at the Hub and deliver all of these packages while finding the shortest paths in between
# to build the route
arr = [1, 2, 3]

pkS1 = 0
pkE1 = city_arr2.index(" "+packageLookUp(arr[0]).addr+"\n("+packageLookUp(arr[0]).zipcode+")")

print(getMinimumDistanceBetween2Cities(pkS1, pkE1) + 0)

pkS2 = city_arr2.index(" "+packageLookUp(arr[0]).addr+"\n("+packageLookUp(arr[0]).zipcode+")")
pkE2 = city_arr2.index(" "+packageLookUp(arr[1]).addr+"\n("+packageLookUp(arr[1]).zipcode+")")

print(getMinimumDistanceBetween2Cities(pkS2, pkE2))

pkS3 = city_arr2.index(" "+packageLookUp(arr[1]).addr+"\n("+packageLookUp(arr[1]).zipcode+")")
pkE3 = city_arr2.index(" "+packageLookUp(arr[2]).addr+"\n("+packageLookUp(arr[2]).zipcode+")")

print(getMinimumDistanceBetween2Cities(pkE3, pkS3))


#The bottom code will print all shortest paths from a starting vertex (vertex_1). Here for convenience but not nessesary
# for the tsk completion

#vertex_1 = vertex_arr[1]

#dijkstra_shortest_path(g, vertex_1)

'''print("\nDijkstra shortest path:")
for v in g.adjacency_list:
    if v.pred_vertex is None and v is not vertex_1:
        print("1 to %s ==> no path exists" % v.label)
    else:
        print("1 to %s ==> %s (total distance: %g)" % (v.label, get_shortest_path(vertex_1, v), v.distance))'''

#The bottom code will print all package Ids from the hash table. Here for convenience but not nessesary
# for the tsk completion

#for i in range(len(myHash.table)+1):
    #print("Key: {} and Package: {}".format(i + 1, myHash.search(i + 1)))