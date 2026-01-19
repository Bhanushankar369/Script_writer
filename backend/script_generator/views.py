from django.shortcuts import render

from .script_graph import graph_build

from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class ScriptView(APIView):
    def get(self, request):
        message = request.data.get('message')
        
        response = graph_build.invoke(message)
        
        return Response({"Response": response})