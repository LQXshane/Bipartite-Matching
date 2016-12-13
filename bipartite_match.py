
# coding: utf-8

# # For bipartite matching,
# the construction is to introduce source-
# and sink nodes to the bipartite graph G(V,E)
# call ford-fulkerson on a new graph G'(V', E')
# where we mark source node by index 0 and sink (V+1).
# Every internal node on the left, X, has an edge of weight 1 to the sink s;
# every internal node on the right, Y, has an edge of weight 1 to the sink t;
# the original edges E remains, each assigned with weight 1.
# We will have the perfect matching 
# if ford-fulkerson returns a valid max flow value and every vertex is visited
# if not we will determine the size of the largest bipartite matching.

# In[18]:

# Deal with the data storage

V = 200
src = 0
sink = V+1
Vp = V+2 # V' as V prime

graph = [[0 for col in range(Vp)] for row in range(Vp)]

import string
def readFileToArray( filename ):
    arr = [] # List of rankings
    with open( filename ) as file:
        for List in file:
            tmp = List.strip(string.whitespace)
            arr.append(tmp)
    file.close()
    return arr


edge = readFileToArray('hw5test.txt')

# assign the correspding edge weight to 1 in our adjacency list
for i in range(len(edge)):
    idx0 = int(edge[i].split(' ')[0])
    idx1 = int(edge[i].split(' ')[1])
    graph[idx0][idx1] = 1

for i in range(1,101):
    graph[0][i] = 1 # each node in X are connected to source
    graph[i+100][201] = 1


# In[19]:

graph[0][0:10]


# # Ford-Fulkerson algorithm using BFS
# For this part, I collaborated with 
# Jin Yue, Xiang Li, Jingjing Zhu and Yanjia Zhang
# since this is the main algorithm of our course project- 
# Image Segmentation- for which we have submitted earlier
# a similar version of this implementation.
# The following is my implementation for this homework 5.1

# In[20]:

def ford_fulkerson(graph, s, t, V):
    # Input graph stored in adjacency list, for example,
    # graph = [[0, 1, 1, 0], 
    #          [0, 0, 1, 1],
    #          [0, 0, 0, 1], 
    #          [0, 0, 0, 0]]
    # in this case, we have four vertices: source, two internal nodes and sink.
    # The first row corresponds to the edges starting from the source node s, e.g. there are two edges of weight 1: 
    # from s to node 1 and from s to node 2
    # both node 1 and 2 has an edge to the sink node t
    
    # V is the dimension of our adjacency list
    
    max_flow = 0  
    
    rgraph = [[0 for col in range(V)] for row in range(V)]  
    # initialize residual graph
    for i in range(V):
        for j in range(V):
            rgraph[i][j] = graph[i][j]

    parent = [0 for i in range(V)]
    
    # finding s-t augmenting paths in the residual graph
    
    while bfs(rgraph, s, t, parent, V):  
        # initial flow we now recursively search from sink 
        # and calculate bottleneck
        flow = float("inf")  
        v = t 
        while v != s:  
            u = parent[v]
            flow = min(flow, rgraph[u][v])
            v = parent[v]
        bottleneck = flow
        v = t
        while v != s:  
            u = parent[v]
            
            rgraph[v][u] += bottleneck
            # forward edge
            rgraph[u][v] -= bottleneck  
            # backward edge
            v = parent[v]

        max_flow += bottleneck  # get the total values of flows

    # get all nodes that are visited
    parent = [0 for i in range(V)]
    visited = bfs2(rgraph, s, parent, V)
    print "The total values of flows is: %d" % max_flow
    return visited

# determine if there is a path using BFS
# return True or False, boolen value
def bfs(rgraph, s, t, parent, V):
    # create a list to store visited nodes
    # initialize to False 
    visited = [False for i in range(V)]  
    visited[s] = True  
    # parent remembers the start node of each edge
    parent[s] = -1 
    
    q = list()  
    q.insert(0, s)  
    
    # standard bfs
    while len(q) != 0:  
        row = q.pop()  
        for i in range(V): 
            if not visited[i] and rgraph[row][i] > 0:
                q.insert(0, i)  
                parent[i] = row  
                # mark its parent as the current row node
                visited[i] = True  
                # mark the node as visited
    return visited[t]  


# bfs2: exactly the same as bfs
# except that we now return 
# the complete array of the visited nodes 
def bfs2(rgraph, s, parent, V):
    
    visited = [False for i in range(V)]  
    visited[s] = True  
    parent[s] = -1  
    q = list()  
    q.insert(0, s)  
    while len(q) != 0:  
        row = q.pop()  
        for i in range(V):  
            
            if not visited[i] and rgraph[row][i] > 0:
                q.insert(0, i)  
                parent[i] = row  
                visited[i] = True  
    return visited  


# In[21]:


# sample small dataset borrowed from CLRS book 286.8(C) to validate my algorithm
sample_V = 11
sample_src = 0
sample_sink = 10
sample_graph = [[0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

match = ford_fulkerson(sample_graph, sample_src, sample_sink, sample_V) # test out to be 3, as was shown in the book


# In[22]:

match = ford_fulkerson(graph, src, sink, Vp)
# print those vertices who are not being visited
print "Vertices not being visited:"
for i in range(1,V+1):
    if not match[i]:
        print i

