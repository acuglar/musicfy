from rest_framework import serializers
from collections import OrderedDict


class SampleSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField(required=True)


class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) 
    name = serializers.CharField(required=False)
    formed_in = serializers.IntegerField(required=False)  
    status = serializers.CharField(required=False) 


class SongSerializer(serializers.Serializer):
    title = serializers.CharField()
    artist = ArtistSerializer() 


class SongSimpleSerializer(serializers.Serializer):    
    title = serializers.CharField()
    
    
class ArtistSongsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    formed_in = serializers.IntegerField()
    status = serializers.CharField()
    musics = SongSimpleSerializer(many=True, read_only=True, source='songs')
    total_songs = serializers.SerializerMethodField()
    
    def get_total_songs(self, obj):
        if (isinstance(obj, OrderedDict)):
            return 0
        return { 'count': obj.songs.count()}


class PlaylistSerializer(serializers.Serializer):
    title = serializers.CharField()
    songs = SongSerializer(many=True)