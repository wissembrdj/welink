class Normalize:

    def __init__(self, phrase):
        self.phrase=phrase 
    
    def normalize(self):
        phrase=self.phrase
        phrase_split= phrase.split(" ")
        phrase_capitalise = []
        parenthese=["("]
        for pn in phrase_split:
            if pn[0].isupper() or pn[0] in parenthese or pn=="of" or pn=="and" :
                phrase_capitalise.append(pn)
            else:
                phrase_capitalise.append(pn.capitalize())    
        phrase_normalize=""
        for ps in phrase_capitalise: 
            phrase_normalize= phrase_normalize + ps+"_"
        phrase_normalize=phrase_normalize[:-1]
        return phrase_normalize
    
    def capitilize(self):
        phrase=self.phrase
        phrase_capitalise= phrase.capitalize()
        return phrase_capitalise

# n=Normalize("REP Parasol")
# nn=n.normalize()
# print(nn)
