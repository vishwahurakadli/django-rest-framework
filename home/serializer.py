from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = ['color_name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    # color_info = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = '__all__'


        # depth = 1

    def validate(self, data):
        
        if data.get('age') and data['age']<18:
            raise serializers.ValidationError("Age should be more than 18")
        
        return data
    
    # def get_color_info(self,obj):
    #     color_obj = Color.objects.get(id=obj.color.id)

    #     return {'color_name':color_obj.color_name, 'hex_code': '#000'}

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username is taken')
            
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email is taken')

        return data
    
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data