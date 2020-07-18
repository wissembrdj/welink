import re

def extract_entities(query):
    pattern="http://dbpedia.org/resource/[^>]+"
    return re.findall(pattern,query)
def entities(query):
    firstModified=[]
    if query=="OUT OF SCOPE":
        return firstModified
    whereString = query[query.index('{')+1:query.rfind('}')-1]
    if "no_query" in whereString:
        return firstModified
    whereString=whereString.replace("\n","")
    whereString=whereString.replace("\t"," ")
    query=whereString
    pattern="res:[^\s]+"
    first=re.findall(pattern,query)
     
    for entity in first:
        firstModified.append(entity.replace("res:","http://dbpedia.org/resource/"))
         
    pattern="http://dbpedia.org/resource/[^>]+"
    second=re.findall(pattern,query)
    return firstModified+second   