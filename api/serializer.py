# serializers.py
from rest_framework import serializers
from tests.models import *

class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer', 'is_correct']
        read_only_fields = ['id']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Questions
        fields = '__all__'
        read_only_fields = ('id', 'group')

    def validate(self, data):
        answers = self.initial_data.get('answers', [])

        # Har bir savolda aniq 4 ta javob bo'lishi kerak
        if len(answers) != 4:
            raise serializers.ValidationError("Har bir savolda aniq 4ta javob bo‘lishi kerak.")

        # Javoblardan faqat bittasi True bo'lishi kerak
        true_count = sum(1 for ans in answers if ans.get('is_correct') == True)
        if true_count != 1:
            raise serializers.ValidationError("Har bir savolda faqat bitta javob True bo‘lishi kerak.")

        return data

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        question = Questions.objects.create(**validated_data)
        for answer in answers:
            Answer.objects.create(question=question, **answer)
        return question

    def update(self, instance, validated_data):
        answers = validated_data.pop('answers', [])
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        instance.answers.all().delete()
        for answer in answers:
            Answer.objects.create(question=instance, **answer)
        return instance

class GroupSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('id', 'admin', 'start_time', "end_time")

    def create(self, validated_data):
        questions = validated_data.pop('questions', [])
        group = Group.objects.create(**validated_data)
        for question in questions:
            Questions.objects.create(group=group, **question)
        return group
# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from tests.models import *

class GroupAdd(APIView):
    serializer_class = GroupSerializer

    def get(self, request):
        groups = Group.objects.all()
        serializers = GroupSerializer(groups, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = GroupSerializer(data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save(admin=request.user)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupEditor(APIView):
    serializer_class = GroupSerializer

    def get(self, request, group_id):
        group = get_object_or_404(Group, code=group_id)
        serializers = GroupSerializer(group)
        return Response(serializers.data)

    def put(self, request, group_id):
        group = get_object_or_404(Group, code=group_id)
        serializer = GroupSerializer(instance=group, data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        group = get_object_or_404(Group, code=group_id)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddQuestion(APIView):
    serializer_class = QuestionsSerializer

    def get(self, request, group_id):
        questions = Questions.objects.filter(group__code=group_id)
        serializers = QuestionsSerializer(questions, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, group_id):
        serializer = QuestionsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            group = get_object_or_404(Group, code=group_id)
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditQuestion(APIView):
    serializer_class = QuestionsSerializer

    def get(self, request, group_id, question_id):
        question = get_object_or_404(Questions, id=question_id, group__code=group_id)
        serializers = QuestionsSerializer(question)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, group_id, question_id):
        question = get_object_or_404(Questions, id=question_id, group__code=group_id)
        serializers = QuestionsSerializer(instance=question, data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id, question_id):
        question = get_object_or_404(Questions, id=question_id, group__code=group_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllQuestions(APIView):
    serializer_class = QuestionsSerializer

    def get(self, request):
        questions = Questions.objects.all()
        serializers = QuestionsSerializer(questions, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

class Result(APIView):
    def get(self, request, user_id):
        results = Result.objects.filter(user=user_id)
        serializers = ResultSerializer(results, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
