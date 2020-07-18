# if you don't have WordNet you can use the nltk.download('wordnet')
# we adapted the https://www.tutorialspoint.com/python/python_synonyms_and_antonyms.htm code
from nltk.corpus import wordnet


class Synonyms():
    '''
    classdocs
    '''


    def __init__(self, words):
        '''
        Constructor
        '''
        self.words = words
        
    def definition(self):
        words_def=""  
        syns = wordnet.synsets(self.words)
        if syns:
            word_definition=syns[0].definition()
        else:
            word_definition=""   
        words_def=self.words+" "+words_def+word_definition
          
        return words_def       
    
    def synonyms(self):
        synonyms=[]
        for word in self.words:
            if wordnet.synsets(word):
                for syn in wordnet.synsets(word):
                    for name in syn.lemma_names():
                        synonyms.append(name)
            synonyms.append(word)        
        vrep=""

        for rep in synonyms:
            if rep not in vrep:
                vrep=vrep+" "+rep
        return vrep    

       


# sss=Synonyms(["Bill Finger"]).definition()
# print(sss)
 