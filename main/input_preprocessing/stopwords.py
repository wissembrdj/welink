from nltk.corpus import stopwords


class Stopwords:
    '''
    classdocs
    '''
    def __init__(self, words):
        '''
        Constructor
        '''
        self.words = words
        
    def stop_words(self):
        stop_words_list= set(stopwords.words("english"))
        filtred_words=[]
        for word in self.words:
            if word not in stop_words_list:
                filtred_words.append(word)
        return(filtred_words)

#print(stop_words(["to", "be", "or","not", "happy","be","test"]))    