import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from tests.models import User, Group, Questions, Answer, Result, UserAnswers

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"test_{self.room_code}"

        self.user = self.scope['user'] if self.scope['user'].is_authenticated else None
        self.role = "admin" if self.user and self.user.is_admin else "student"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{self.user.username if self.user else 'Guest'} ({self.role}) qo'shildi"
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        # Admin boshqaruvi
        if self.role == "admin":
            if action == "start_test":
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "test_started",
                    "message": "Test boshlandi!"
                })
            elif action == "next_question":
                question_id = data.get("question_id")
                question_data = await self.get_question_data(question_id)
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "send_question",
                    "question": question_data
                })
            elif action == "finish_test":
                group_id = data.get("group_id")
                results = await self.get_final_results(group_id)
                await self.channel_layer.group_send(self.room_group_name, {
                    "type": "final_results",
                    "results": results
                })

        # Student javob yuboradi
        elif self.role == "student" and action == "submit_answer":
            question_id = data.get("question_id")
            answer_id = data.get("answer_id")
            score, is_correct = await self.check_answer_and_save(question_id, answer_id, self.user.id)

            # Javobdan keyin real-time admin va studentlarga yuborish
            leaderboard = await self.get_leaderboard(self.room_code)
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "student_answer",
                "user": self.user.username,
                "question_id": question_id,
                "score": score,
                "is_correct": is_correct,
                "leaderboard": leaderboard
            })

    @database_sync_to_async
    def get_question_data(self, question_id):
        question = Questions.objects.get(id=question_id)
        answers = [{"id": a.id, "text": a.answer} for a in question.answers.all()]
        return {
            "id": question.id,
            "text": question.question,
            "answers": answers
        }

    @database_sync_to_async
    def check_answer_and_save(self, question_id, answer_id, user_id):
        question = Questions.objects.get(id=question_id)
        answer = Answer.objects.get(id=answer_id, question=question)
        score = 10 if answer.is_correct else 0

        UserAnswers.objects.create(
            user_id=user_id,
            question=question,
            answer=answer,
            is_correct=answer.is_correct,
            score=score
        )

        result, created = Result.objects.get_or_create(user_id=user_id, group=question.group)
        result.score += score
        result.save()
        return score, answer.is_correct

    @database_sync_to_async
    def get_leaderboard(self, room_code):
        group = Group.objects.get(code=room_code)
        leaderboard = Result.objects.filter(group=group).values("user__username", "score").order_by("-score")
        return list(leaderboard)

    @database_sync_to_async
    def get_final_results(self, group_id):
        results = Result.objects.filter(group_id=group_id).values("user__username", "score").order_by("-score")
        return list(results)

    # WebSocket orqali yuboriladigan eventlar
    async def student_answer(self, event):
        await self.send(text_data=json.dumps({
            "type": "student_answer",
            "user": event["user"],
            "question_id": event["question_id"],
            "score": event["score"],
            "is_correct": event["is_correct"],
            "leaderboard": event["leaderboard"]
        }))

    async def send_question(self, event):
        await self.send(text_data=json.dumps({
            "type": "question",
            "question": event["question"]
        }))

    async def final_results(self, event):
        await self.send(text_data=json.dumps({
            "type": "final_results",
            "results": event["results"]
        }))

    async def test_started(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"]
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"]
        }))
