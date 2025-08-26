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
        group = get_object_or_404(Group, id=group_id)
        serializers = GroupSerializer(group)
        return Response(serializers.data)

    def put(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        serializer = GroupSerializer(instance=group, data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddQuestion(APIView):
    serializer_class = QuestionsSerializer

    def get(self, request, group_id):
        questions = Questions.objects.filter(group__id=group_id)
        serializers = QuestionsSerializer(questions, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, group_id):
        serializer = QuestionsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            group = get_object_or_404(Group, id=group_id)
            serializer.save(group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditQuestion(APIView):
    serializer_class = QuestionsSerializer

    def get(self, request, group_id, question_id):
        question = get_object_or_404(Questions, id=question_id, group__id=group_id)
        serializers = QuestionsSerializer(question)
        return Response(serializers.data)

    def put(self, request, group_id, question_id):
        question = get_object_or_404(Questions, id=question_id, group__id=group_id)
        serializers = QuestionsSerializer(instance=question, data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, group_id, question_id):
        question = get_object_or_404(Questions, id=question_id, group__id=group_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class AllQuestions(APIView):
    serializer_class = QuestionsSerializer
    def get(self, request):
        questions = Questions.objects.all()
        serializers = QuestionsSerializer(questions, many=True)
        return Response(serializers.data, status = status.HTTP_200_OK)
class TestGame(APIView):
    def post(self, request, group_id, question_id):
        question = Questions.objects.get( id=question_id, group__id=group_id)
        answer_id = request.data.get('answer_id')
        answer = Answer.objects.get(id=answer_id)
        if answer.is_correct:
            time = request.data.get('time')
        else:
            time =0
        score = time*10
        UserAnswers.objects.create(
            answer=answer,
            question=question,
            user=User.objects.get(id=request.user.id),
            is_correct=answer.is_correct,
            score = score
        )
        next_question = (
            Questions.objects.filter(group__id=group_id, id__gt=question_id)
            .order_by("id")
            .first()
        )

        if next_question is not None:
            return Response({
                "correct": answer.is_correct,
                "score": score,
                "next_question": QuestionsSerializer(next_question).data,
            })
        else:
            return Response({
                "correct": answer.is_correct,
                "score": score,
                "detail": "Test tugadi"
            }, status=status.HTTP_200_OK)
class GroupResultsUser(APIView):
    def get(self, request, group_id):
        score = UserAnswers.objects.filter(
            question__group_id=group_id,
        ).values('user__username').annotate(total_score = Sum('score')).order_by('-total_score')
        return Response(score, status=status.HTTP_200_OK)
