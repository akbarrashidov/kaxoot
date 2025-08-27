from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from tests.models import *
from django.db.models import Sum

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
        group = Group.objects.get(code=group_id)
        serializers = GroupSerializer(group)
        return Response(serializers.data)

    def put(self, request, group_id):
        group = Group.objects.create(code=group_id)
        serializer = GroupSerializer(instance=group, data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        group = Group.objects.get(code=group_id)
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
            group = Group.objects.get(code=group_id)
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditQuestion(APIView):
    serializer_class = QuestionsSerializer

    def get(self, request, group_id, question_id):
        question = Questions.objects.get(id=question_id, group__code=group_id)
        serializers = QuestionsSerializer(question)
        return Response(serializers.data)

    def put(self, request, group_id, question_id):
        question = Questions.objects.get(id=question_id, group__code=group_id)
        serializers = QuestionsSerializer(instance=question, data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, group_id, question_id):
        question = Questions.objects.get(id=question_id, group__code=group_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class AllQuestions(APIView):
    serializer_class = QuestionsSerializer
    def get(self, request):
        questions = Questions.objects.all()
        serializers = QuestionsSerializer(questions, many=True)
        return Response(serializers.data, status = status.HTTP_200_OK)

