from django.http import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Artist, Song
from .serializers import SampleSerializer, ArtistSerializer, SongSerializer, ArtistSongsSerializer
import ipdb


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello Django"})

    def post(self, request):
        serializer = SampleSerializer(data=request.data)  
        serializer.is_valid()  
        serializer.data  
        # ipdb.set_trace()

        return Response(serializer.data)


class ParamView(APIView):
    def get(self, request, name):
        return Response({"message": f"Hello {name}"})
        
    def post(self, request, name):
        return Response({"message": f"Hello {name}"})


class MusicfyArtistView(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        # ipdb.set_trace()

        serialized = ArtistSerializer(artists, many=True)
        # sem attrib many: AttributeError
        # artists: list => many=True
        # ipdb.set_trace()

        return Response(serialized.data)

    def post(self, request):
        serializer = ArtistSerializer(data=request.data)
        # data indica não tratar-se de uma instância de objeto

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # ipdb.set_trace()
        # ipdb> request.data
        # {'name': 'Teste38', 'formed_in': 2006, 'status': 'Active', 'outro': 'pudim'}
        # ipdb> serializer.data
        # {'name': 'Teste38', 'formed_in': 2006, 'status': 'Active'}
        # ipdb> serializer.validated_data
        # OrderedDict([('name', 'Teste38'), ('formed_in', 2006), ('status', 'Active')])
        artist = Artist.objects.get_or_create(**serializer.validated_data)[0]
        
        serializer = ArtistSerializer(artist)

        return Response(serializer.data)


class MusicfySongView(APIView):
    def get(self, request):
        songs = Song.objects.all()

        serialized = SongSerializer(songs, many=True)

        return Response(serialized.data) 
    
    def post(self, request):
        serializer = ArtistSongsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        artist = Artist.objects.get_or_create(**serializer.validated_data)[0]
        
        serializer = ArtistSongsSerializer(artist)
        # ipdb.set_trace()
        return Response(serializer.data)