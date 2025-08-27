from tests.models import *
from rest_framework import serializers



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
        if len(answers) != 4:
            raise serializers.ValidationError("Har bir savolda aniq 4ta javob bo‘lishi kerak.")
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
            Answer.objects.create(questions=instance, **answer)
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
