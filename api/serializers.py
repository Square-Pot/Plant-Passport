from plants.models import Plant
from rest_framework import serializers


# class PlantSerializer(serializers.HyperlinkedModelSerializer):
    # class Meta:
    #     model = Plant
    #     fields = ['uid', 'access_type']     

# class PlantSerializer(serializers.Serializer):
#     uid = serializers.CharField()
#     id = serializers.IntegerField()
#     creation_date = serializers.DateTimeField()

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'uid', 'access_type')
