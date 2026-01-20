from rest_framework import serializers
from .models import Script

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = '__all__'
        
    def create(self, validated_data):
        newScript = Script.objects.create(
            title=validated_data['title'],
            context = validated_data['context'],
            category = validated_data['category'],
            video_length = validated_data['video_length'],
            ai_message = validated_data['ai_message']
        )
        
        return newScript