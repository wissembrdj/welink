from django.shortcuts import render
from django.http import HttpResponse
from main.forms import UserQuery
from main.input_preprocessing import *
from main.candidate_generation import *
from main.candidate_ranking import *
from main.welink import Welink 
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
from rest_framework.renderers import JSONRenderer, PlainTextRenderer
import json
from .serializers import UserQuerySerializer
from pynif import NIFCollection
from rest_framework.parsers import PlainTextParser
from nifwrapper import *
from rdflib.serializer import Serializer
import mimetypes
from rest_framework.test import RequestsClient
import time

# Create your views here.

def homepage(request):
    if request.method == 'POST':
        form = UserQuery(request.POST)
    # check whether it's valid:
        if form.is_valid():
            userquery=form.cleaned_data['userquery']
            results= Welink(userquery).userquerymodel()
            args={'form': form, 'userquery': userquery, "results": results}
            return render(request, "pages/index.html", args)

        else:
            form = user_query()
    
    form= UserQuery()
    return render(request, "pages/index.html", {'form': form})

def api_welink(request):
    return render(request, "pages/api.html")

def presentation_welink(request):
    return render(request, "pages/presentation.html")
    
def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
   
class UserqueryApi(APIView):
    def post(self, request, format=None): 
        start_time = time.time()
        userquery= request.data
        print("query", userquery)
        print("--- %s seconds ---" % (time.time() - start_time))
        serilize_userquery= UserQuerySerializer(userquery).data
        query=serilize_userquery["query"]
        print("SERILIZE--- %s seconds ---" % (time.time() - start_time))
        results= Welink(query).userquerymodel()
        print("resultat--- %s seconds ---" % (time.time() - start_time))
        if results:
            n=0
            list=[]
            mentions=[]
            for res in results:
                for result in res: 
                    if result.em.name not in mentions:
                        mentions.append(result.em.name) 
                    list.append([result.em.name, result.ec.ec_uri])       
                    if 'results' in serilize_userquery:
                        serilize_userquery["results"].update({str(n) : list})
                    else:
                        serilize_userquery["results"]= {str(n) : list}
                list=[]
                n=n+1  
                 
            serilize_userquery["mentions"]= mentions    
              
        return Response(serilize_userquery)



