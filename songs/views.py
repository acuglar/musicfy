from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SampleSerializer

import ipdb


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello Django"})

    def post(self, request):
        serializer = SampleSerializer(data=request.data)  
        serializer.is_valid()  
        serializer.data  
        ipdb.set_trace()

        return Response(serializer.data)


class ParamView(APIView):
    def get(self, request, name):
        return Response({"message": f"Hello {name}"})
        
    def post(self, request, name):
        return Response({"message": f"Hello {name}"})