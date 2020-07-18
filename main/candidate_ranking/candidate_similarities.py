from sklearn.feature_extraction.text import TfidfVectorizer

# from test import all_documents
class Candidate_similarities:
    '''
    This class returns the cosine similarity between the entity mention context and each candidate context 
    '''


    def __init__(self, m, c):
        '''
        Constructor
        '''
        self.m=m
        self.c=c 
      
    def cosine(self):
        sim_cosine=[]
        t=0
        candidates=self.c
        all_documents=[]
        all_documents.append(self.m.context)
        for i in candidates:
#             for i in ci:
            all_documents.append(i.ec_context)
            
        if all('' == s or s.isspace() for s in all_documents):
            while t < len(all_documents):
                sim_cosine.append(0)
                t=t+1
        else:    
            sklearn_tfidf = TfidfVectorizer(min_df=1, use_idf=True, stop_words="english")
            sklearn_representation = sklearn_tfidf.fit_transform(all_documents)
            #print(sklearn_tfidf.get_feature_names())
            sim_cosine=(sklearn_representation * sklearn_representation.T).A[0]
        return(sim_cosine)



'''
corpus=["I love Paris","I want to go to Paris","I want to travel to Algeria"]
tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tfidf_matrix =  tf.fit_transform([content in corpus])
print(tfidf_matrix)
# test=Candidate_similarities("life learning")    
# tests=test.moy_cosine()   
# print(tests)'''