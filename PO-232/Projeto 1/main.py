# PO-232 - Algoritmos em Grafos
# Nicholas Scharan Cysne
# Projeto 1 - Weisfeiler-Lehman Isomorphism Test
# Referência: https://davidbieber.com/post/2019-05-10-weisfeiler-lehman-isomorphism-test/

from WeisfeilerLehman import *

# Object of Weisfeiler-Lehman Isomorphism Test
wl = WeisfeilerLehman()
# Number of maximum iterations
n = 12

# Creation of two graphs to check isomorphism
# Graph A 
g_a = Graph()
g_a.add_vertices(5)
g_a.add_edges([(0,1), (1,2), (2,3), (3,4), (4,0), (3,0)])
g_a['name'] = 'Graph A'
print(g_a)

# Graph B
g_b = Graph()
g_b.add_vertices(5)
#g_b.add_edges([(0,1), (1,2), (2,3), (3,4), (4,0), (3,0)])
g_b.add_edges([(0,1), (1,2), (2,3), (3,4), (4,0)])
g_b['name'] = 'Graph B'
print(g_b)

# Export images of Graph A and Graph B
plot(g_a, layout = g_a.layout("random"), target=g_a['name'] + '.png')
plot(g_a, layout = g_b.layout("random"), target=g_b['name'] + '.png')

# # Example of WL Isomorphism Test in Chemistry
# # Graph A 
# g_a = Graph()
# g_a.add_vertices(28)
# g_a.add_edges([(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,6), (0,7), (1,8), (1,9), (2,10), (2,11), (5,12), (5,13), (4,14), (4,15), 
#                (15,16), (16,17), (17,18), (18,19), (19,20), (20,16), (16,27), (17,25), (17,26), (18,23), (18,24), (19,21), (19,22)])
# g_a['name'] = 'Carboidrato A'

# # Graph A 
# g_b = Graph()
# g_b.add_vertices(28)
# g_b.add_edges([(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,6), (0,7), (1,8), (1,9), (2,10), (2,11), (5,12), (5,13), (4,14), (4,15), 
#                (15,16), (16,17), (17,18), (18,19), (19,20), (20,16), (16,27), (17,25), (17,26), (18,23), (18,24), (19,21), (19,22)])
# g_b['name'] = 'Carboidrato B'

# # Export images of Graph A and Graph B
# plot(g_a, layout = g_a.layout("kk"), target=g_a['name'] + '.png')
# plot(g_a, layout = g_b.layout("kk"), target=g_b['name'] + '.png')

# Check isomorphism between Graph A and Graph B
isomorphic = wl.check_isomorphism(g_a, g_b, n)

if isomorphic:
    print("\nResult: Graph A and Graph B are isomorphic\n")
else:
    print("\nResult: Graph A and Graph B are not isomorphic\n")
