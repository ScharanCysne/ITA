# PO-232 - Algoritmos em Grafos
# Nicholas Scharan Cysne
# Projeto 1 - Weisfeiler-Lehman Isomorphism Test
# Referência: https://davidbieber.com/post/2019-05-10-weisfeiler-lehman-isomorphism-test/
 
from igraph import *

class WeisfeilerLehman:

    def __init__(self):
        self.hash = dict()      # Dictionary of hashs

    def to_hash(self, g):
        # For each node label, add a matching hash in the dict
        for v in g.vs:
            # Check if hash already exists
            if str(v['Current Label']) not in self.hash:
                # Store hash in dict
                self.hash[str(v['Current Label'])] = sum(v['Label Multiset'])

            # Update Previous Label and hash
            v['Previous Label'] = sum(v['Current Label'])
            v['label'] = sum(v['Current Label'])

        return g

    def generateCompressedLabels(self, g):
        # For each node, multiset label is the list of neighbours labels
        for v in g.vs:
            v['Label Multiset'] = []
            for nv in v.neighbors():
                v['Label Multiset'].append(nv['Previous Label'])
            # Set current label as the sum of neighbours labels
            v['Current Label'] = v['Label Multiset']

    def check_isomorphism(self, g1, g2, n):

        # Initialize algorithm by labeling C(0,n) = 1 for all nodes n
        for v in g1.vs:
            v['Current Label'] = v['Previous Label'] = 1
            v['Label Multiset'] = []
        # Initialize algorithm by labeling C(0,n) = 1 for all nodes n
        for v in g2.vs:
            v['Current Label'] = v['Previous Label'] = 1
            v['Label Multiset'] = []

        for index in range(1, n):
            print("\nIteration #%d" % index)
            plot(g1, layout = g1.layout("kk"), target=g1['name'] + '_' + str(index) + '.png')
            plot(g2, layout = g2.layout("kk"), target=g2['name'] + '_' + str(index) + '.png')

            # Generate Compressed Labels for G1 and G2
            self.generateCompressedLabels(g1)
            self.generateCompressedLabels(g2)

            # Create hash to each label
            g1 = self.to_hash(g1)
            g2 = self.to_hash(g2)
            
            # Generate set of current labels to comparison
            compressed_labels_g1 = set([ self.hash[str(v['Current Label'])] for v in g1.vs ])
            compressed_labels_g2 = set([ self.hash[str(v['Current Label'])] for v in g2.vs ])

            # Compare set of labels, if are different interrupt algorithm
            if(compressed_labels_g1 != compressed_labels_g2):
                print ("Compressed Labels Mismatch!\n")
                print(compressed_labels_g1)
                print(compressed_labels_g2)

                return False

        return True