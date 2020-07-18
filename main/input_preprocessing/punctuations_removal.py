import string


class Punctuations_removal:
    '''
    classdocs
    '''


    def __init__(self, tokens):
        '''
        Constructor
        '''     
        self.tokens=tokens
        
    def punctuations_removal(self):
        exclude = set(string.punctuation)
        supp_exclude=["``", "''"]
        punctuation=[]
        for token in self.tokens:
            if token not in exclude and token not in supp_exclude:        
                punctuation.append(token)
        return punctuation

'''
ppp=Punctuations_removal(["test", "si", "c'est", "?", "ou", "''", "`"])
p=ppp.punctuations_removal()
print(p)      '''