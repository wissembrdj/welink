import nltk


class Tokenization:
    '''
    classdocs
    '''


    def __init__(self, sentence):
        '''
        Constructor
        '''
        self.sentence= sentence


    def tokenization(self):
        tokenize = nltk.word_tokenize(self.sentence)
        return tokenize    