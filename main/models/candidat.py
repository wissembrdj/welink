class Candidat:
    '''
    DBpedia resultat
    '''


    def __init__(self, ec_uri, ec_name, ec_context, properties, objects):
        '''
        Constructor
        '''
        self.ec_uri=ec_uri # URI of a candidate
        self.ec_name=ec_name #name of a candidate
        self.ec_context=ec_context # the abstract of a candidate
        self.properties=properties # properties of a candidate
        self.objects=objects # direct entities of a candidate
#         self.priority=priority
#         self.types=types # direct entities of a candidate
