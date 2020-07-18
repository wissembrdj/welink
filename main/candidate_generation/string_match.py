from SPARQLWrapper import SPARQLWrapper, JSON
from nltk import tokenize
from main.input_preprocessing.normalize import Normalize
from main.models.candidat import Candidat 
import time

class StringMatch():
    def __init__(self, entity):
        self.entity=entity
#         self.e_type=e_type
     
    def string_match(self):
        tim=time.time()
        entity= self.entity.name
        if " " in self.entity.name: 
            normalise=Normalize(self.entity.name)
            normalized_ne=normalise.normalize()
        else:
            if entity[0].islower():
                entity=entity.capitalize()
                normalized_ne=entity
            else:
                normalized_ne=entity    
          
                
            
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        c_entities=[]
        sparql.setQuery(''' 
        SELECT DISTINCT ?y ?s ?na (concat(group_concat(distinct ?label; separator=' ')) as ?props) (concat(group_concat(distinct ?olabel; separator=' ')) as ?objs) WHERE {
             {<http://dbpedia.org/resource/''' + normalized_ne + '''> dbo:wikiPageDisambiguates ?y }
           UNION {<http://dbpedia.org/resource/''' + normalized_ne + '''_(disambiguation)> dbo:wikiPageDisambiguates ?y}
           UNION {?y rdfs:label "'''+ entity +'''"@en  }
           UNION {?y dbo:wikiPageRedirects <http://dbpedia.org/resource/''' + normalized_ne + '''> }
           UNION {<http://dbpedia.org/resource/''' + normalized_ne + '''> dbo:wikiPageRedirects ?y}
           UNION {?y foaf:name "''' + entity + '''"@en}
           ?y ?p ?o.
           ?y rdf:type ?types FILTER (contains(str(?types), "Place") || contains(str(?types), "Agent")  || contains(str(?types), "Event") || contains(str(?types), "Biomolecule") || contains(str(?types), "Work") || contains(str(?types), "Species") || contains(str(?types), "Animal") || contains(str(?types), "Road") || contains(str(?types), "Colour") || contains(str(?types), "language") || contains(str(?types), "Food") || contains(str(?types), "Award") || contains(str(?types), "Ship") || contains(str(?types), "Settlement") || contains(str(?types), "Aircraft")  ) . 
           ?y dbo:abstract ?s FILTER (lang(?s) = "en").
           OPTIONAL{ ?p rdfs:label ?label FILTER (lang(?label) = "en").}
           OPTIONAL{ ?o rdfs:label ?olabel FILTER (lang(?olabel) = "en").  }
            OPTIONAL {?y rdfs:label ?na FILTER (lang(?na) = "en").}      

         }
         group by ?y ?s ?na
        ''')    
#                       ?y rdf:type ?types FILTER (contains(str(?types), "Location") || contains(str(?types), "Person") || contains(str(?types), "Organisation") || contains(str(?types), "Agent") ||  contains(str(?types), "Movie") || contains(str(?types), "Book") ||  contains(str(?types), "Software") || contains(str(?types), "Work")  || contains(str(?types), "Artwork") || contains(str(?types), "Road") || contains(str(?types), "PoliticalParty") || contains(str(?types), "Food") || contains(str(?types), "Animal") || contains(str(?types), "Plant") || contains(str(?types), "Language") || contains(str(?types), "Colour") || contains(str(?types), "Biomolecule") || contains(str(?types), "Ship")  ) .
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print('Requete sparql ', time.time()- tim )
#         entity_properties=[]
#         entity_objects=[]
        if results["results"]["bindings"]:
            for result in results["results"]["bindings"]:
                entity = result["y"]["value"]
                abstract = result["s"]["value"]
                abstract= tokenize.sent_tokenize(abstract)
                abstract=abstract[0]
                if "na" in result:
                    name_ec= result["na"]["value"]
                else:
                    name_ec= self.entity.name    
                objects_en=result["objs"]["value"] 
                entity_objects= objects_en.split(" ")
                label_property=result["props"]["value"]        
                entity_properties= label_property.split(" ") 
                ce=Candidat(entity, name_ec, abstract, entity_properties, entity_objects)  
                c_entities.append(ce)
            print('Pars time ', time.time()- tim )     
            
#         else:
#             sparql.setQuery('''ASK {
#                 VALUES (?r) { (<http://dbpedia.org/resource/''' + normalized_ne + '''>) }
#                     { ?r ?p ?o }
#                 }  ''')
#             sparql.setReturnFormat(JSON)
#             results = sparql.query().convert()
#             if(results["boolean"]==True):
#                 entity = '''http://dbpedia.org/resource/''' + normalized_ne
#                 abstract = ""
#                 name_ec= self.entity.name    
#                 entity_objects= ""      
#                 entity_properties= ""
#                 ce=Candidat(entity, name_ec, abstract, entity_properties, entity_objects)  
#                 c_entities.append(ce)
               
        return c_entities 

