import json
import csv
from result import Result
import requests
import time
import re
import io
from extract_entities import entities 
 
writer = csv.writer(open("earl_results_qald7.csv", 'a',  newline=''))
url = 'https://earldemo.sda.tech/earl/api/processQuery'
headers = {'Content-type': 'application/json'} 
with open('qald-7.json', encoding='UTF-8') as data_file:
    data = json.loads(data_file.read()) 
    nb=0
    for distro in data['questions']:
        entities_dataset=entities(distro['query']['sparql'])
        entity_mentions=0
        correctly_linked=0
        n=1
        system_result=0
        result=[]
        tmp=time.time()
        for d in distro['question']:
            if d["language"]=='en':
                question_en=d["string"]
        print(question_en)        
        print(entities_dataset)        
        query = {'nlquery': str(question_en)}
        data_json = json.dumps(query)
        response = requests.post(url, data=data_json, headers=headers)
        detected_entity=0
 
        if response:
            execution_time=time.time()-tmp
            response_json=response.json()
            if 'ertypes' in response_json:
                position=response_json["ertypes"]
                if response_json['rerankedlists']:
#                     system_result=len(response_json['results'])  
                     
                    entity_mentions=len(entities_dataset)
                    for i in range(len(response_json["rerankedlists"])):
                        if 'http://dbpedia.org/resource/' in response_json["rerankedlists"][str(i)][0][1]:
                            system_result=system_result+1
                    for em in entities_dataset:
                        for i in range(len(response_json["rerankedlists"])):
                            if 'http://dbpedia.org/resource/' in response_json["rerankedlists"][str(i)][0][1]:
                                rj=response_json["rerankedlists"][str(i)][0][1]
                                print("system response",rj)
                                if rj==em:
#                                     if rj not in result:
                                    correctly_linked=correctly_linked+1     
                                    result.append(rj)                                                    
                                          
                    #print(correctly_linked, system_result, entity_mentions)
                    res= Result(correctly_linked, system_result, entity_mentions)
                    fmeasure=0
                    if system_result!=0:
                        entity_precision=res.precision()
                    else:
                        entity_precision=0   
                    if entity_mentions!=0:    
                        entity_recall=res.recall()  
                    else:
                        entity_recall=0   
                    if entity_recall!=0 and entity_precision!=0:
                        fmeasure= (2*entity_precision*entity_recall)/(entity_precision + entity_recall)   
                       
                    for i in result:
                        print("id question: ", distro['id'], "result n: ",  system_result, detected_entity, result)  
                    print("Precision:", entity_precision," Recall:", entity_recall )          
                    print("____________________________________")
                    myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "0", "0", execution_time] ]               
                    myFile = open('earl_results_qald7.csv', 'a', encoding='utf-8')
                    with myFile:
                        writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                        writer.writerows(myData) 
                      
                else:
                    #No string match
                    system_result=0    
                    entity_precision=0 
                    entity_recall=0 
                    nsm=nsm+1
                    myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, "0", "0",nsm, execution_time] ]                
                    print("____________________________________No string match")    
                    myFile = open('earl_results_qald7.csv', 'a', encoding='utf-8')
                    with myFile:
                        writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                        writer.writerows(myData)    
            else:          
                #No detected named entity:
                if entities_dataset:
                    nbem=0
                    system_result=0    
                    entity_precision=0 
                    entity_recall=0 
                    correctly_linked=0
                    detected_entity=0
                    if 'entity mapping' in distro:
                        for em in distro["entity mapping"]:
                            nbem=nbem+1
                    myData=[[distro['id'],question_en,nbem,detected_entity,system_result,correctly_linked, entity_precision,entity_recall,"0", "1", "0", execution_time] ]                
                    print("____________________________________No detected named entity")    
                     
                else:  
                    nbem=0
                    system_result=1    
                    entity_precision=1 
                    entity_recall=1 
                    correctly_linked=1
                    detected_entity=0
                    fmeasure=1
                    if 'entity mapping' in distro:
                        for em in distro["entity mapping"]:
                            nbem=nbem+1
                    myData=[[distro['id'],question_en,nbem,detected_entity,system_result,correctly_linked, entity_precision,entity_recall,fmeasure, "3", "3", execution_time] ]                
                    print("____________________________________No mention + No results")  
                myFile = open('earl_results_qald7.csv', 'a', encoding='utf-8')
                with myFile:
                    writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                    writer.writerows(myData)  
        else:         
            #Unknown error from the web service
            execution_time=time.time()-tmp
            system_result=0    
            entity_precision=0 
            entity_recall=0 
            fmeasure= 0          
            entity_mentions=0
            detected_entity=0
            correctly_linked=0
            print("____________________________________Unknown error from the web service")
            myData=[[distro['id'],question_en,entity_mentions,detected_entity,system_result,correctly_linked, entity_precision,entity_recall, fmeasure, "2", "2", execution_time] ]               
            myFile = open('earl_results_qald7.csv', 'a', encoding='utf-8')
            with myFile:
                writer = csv.writer(myFile, delimiter =";", lineterminator='\r')
                writer.writerows(myData)  
     

print("EARL process completed")         
 







