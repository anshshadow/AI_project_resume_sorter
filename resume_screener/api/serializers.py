from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JobDescription, Resume

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

class JobDescriptionSerializer(serializers.ModelSerializer):
    resumes = ResumeSerializer(many=True, read_only=True)

    class Meta:
        model = JobDescription
        fields = ('id', 'title', 'description', 'skills', 'resumes', 'created_at')

    def create(self, validated_data):
        job = JobDescription.objects.create(
            hr=self.context['request'].user,
            title=validated_data['title'],
            description=validated_data['description'],
            skills=validated_data['skills']
        )
        return job

