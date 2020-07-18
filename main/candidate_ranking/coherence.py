
class Coherence:
    '''
    Class to compute coherence between entities or relations
    '''


    def __init__(self, v1, v2):
        self.v1=v1
        self.v2= v2
        
    
    def jaccard_similarity(self):    
        v1 = set(self.v1)
        v2 = set(self.v2)
        jaccard_sim= len(v1.intersection(v2)) / len(v1.union(v2))
        return jaccard_sim
    
    def jaccard_variation(self):
        v1 = set(self.v1)
        v2 = set(self.v2)
        jaccard_sim= len(v1.intersection(v2)) / len(v1)
        return jaccard_sim
    
# m_p=['', 'curate', 'minister', 'of', 'religion', 'parson', 'pastor', 'rector', 'government', 'minister', 'diplomatic', 'minister']  
# c_p='Link from a Wikipage to another Wikipage after alongside as before birth place death place deputy honorific prefix monarch office predecessor prime minister primeminister successor title'
# c_p=c_p.split(" ")
# print(c_p)
# coh= Coherence(m_p, c_p)
# test= coh.jaccard_similarity()
# test1= coh.jaccard_variation()
# print("Coherence with jaccard:", test, "Coherence with jaccard variation:", test1)