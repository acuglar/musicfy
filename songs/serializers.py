from rest_framework import serializers
from collections import OrderedDict


class SampleSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField(required=True)

class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    formed_in = serializers.IntegerField()
    status = serializers.CharField()


class SongSerializer(serializers.Serializer):
    title = serializers.CharField()

    # artist_id = serializers.IntegerField()
    # artist = serializers.CharField() 
    artist = ArtistSerializer() 


class SongSimpleSerializer(serializers.Serializer):    
    title = serializers.CharField()
    
    
class ArtistSongsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    formed_in = serializers.IntegerField(write_only=True)
    status = serializers.CharField()
    musics = SongSerializer(many=True, read_only=True, source='songs')
    # source indica que o atributo musics será referenciado como songs
    
    total_songs = serializers.SerializerMethodField()
    
    def get_total_songs(self, obj):
        if (isinstance(obj, OrderedDict)):
            return 0
        return { 'count': obj.songs.count()}