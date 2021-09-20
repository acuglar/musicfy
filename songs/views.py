from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.utils import IntegrityError

from songs.models import Artist, Song, Playlist
from songs.serializers import SampleSerializer, ArtistSerializer, ArtistSongsSerializer, PlaylistSerializer
from songs.permissions import NeverPermit, OnlyAdmin, StaffOnlyGet, OnlyArtistOwner, PlaylistEdition

import ipdb


class SampleView(APIView):
    def get(self, request):
        return Response({"message": "Hello Django"})

    def post(self, request):
        serializer = SampleSerializer(data=request.data)  
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)


class ArtistView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated | OnlyAdmin]
    
    """ query_params ? objeto : lista de objetos """
    def get(self, request):
        if request.query_params:
            artist = Artist.objects.filter(name__icontains=request.query_params.get('name', ''))
        else:
            artist = Artist.objects.all()
        
        serialized = ArtistSongsSerializer(artist, many=True)
        return Response(serialized.data)

    def post(self, request):
        serializer = ArtistSongsSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        songs = validated_data.pop('songs')
        
        try:
            artist = Artist.objects.get_or_create(**serializer.validated_data, user=request.user)[0]
        except IntegrityError:
            return Response({ 'error': 'User already link to an artist'}, status=status.HTTP_400_BAD_REQUEST)

        song_list = []
        for song in songs:
            # Song.objects.get_or_create(**song, artist=artist)
            song = Song(**song, artist=artist)
            song_list.append(song)
            
        Song.objects.bulk_create(song_list)    
            
        serializer = ArtistSongsSerializer(artist)
        return Response(serializer.data)


class ArtistDetailView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyArtistOwner]

    def get(self, request, artist_id=''):
        artist = get_object_or_404(Artist, id=artist_id)
        serializer = ArtistSongsSerializer(artist)

        return Response(serializer.data)

    def put(self, request, artist_id=''):
        serializer = ArtistSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        artist = get_object_or_404(Artist, id=artist_id)
        
        self.check_object_permissions(self.request, artist)
        
        artist.name = serializer.validated_data['name']
        artist.formed_in = serializer.validated_data['formed_in']
        artist.status = serializer.validated_data['status']

        artist.save()
        
        serializer = ArtistSongsSerializer(artist)
        
        return Response(serializer.data)

    def patch(self, request, artist_id=''): 
        serializer = ArtistSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
        artist = Artist.objects.filter(id=artist_id)

        if not artist.exists():
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        artist.update(**serializer.validated_data)
        
        serializer = ArtistSongsSerializer(artist, many=True)
        
        return Response(serializer.data)

    def delete(self, request, artist_id):
        artist = get_object_or_404(Artist, id=artist_id)
        artist.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PlaylistView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [StaffOnlyGet]
    
    def get(self, request):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
    
        serializer = PlaylistSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        songs = validated_data.pop('songs')

        song_list = []
        
        for song in songs:
            artist = song.pop('artist')
            
            artist = Artist.objects.get_or_create(**artist)[0]
            
            song = Song.objects.get_or_create(title=song['title'], artist=artist)[0]
            
            song_list.append(song)

        collaborators = request.data.pop('collaborators')
        
        playlist = Playlist.objects.get_or_create(**validated_data, owner=request.user)[0]
        playlist.songs.set(song_list)
        playlist.collaborators.set(collaborators)
            
        serializer = PlaylistSerializer(playlist)
        
        return Response(serializer.data)


class PlaylistDetailView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [PlaylistEdition]
    
    def put(self, request, playlist_id):
        serializer = PlaylistSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        self.check_object_permissions(request, playlist)
        
        songs = request.data.pop('songs')
        
        song_list = []
        for song in songs:
            artist = song.pop('artist')
            
            artist = Artist.objects.get_or_create(**artist)[0]
            
            song = Song.objects.get_or_create(title=song['title'], artist=artist)[0]
            
            song_list.append(song)
            
        playlist.songs.set(song_list)
        serializer = PlaylistSerializer(playlist)
        
        return Response(serializer.data)
