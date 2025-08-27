from django.urls import path, include
from .views import *
urlpatterns = [
    path('rooms/', GroupAdd.as_view(), name='add'),
    path('rooms/<int:group_id>/', GroupEditor.as_view(), name='edit group'),
    path('rooms/<int:group_id>/questions/', AddQuestion.as_view(), name='addtest'),
    path('rooms/<int:group_id>/questions/<int:question_id>/', EditQuestion.as_view(), name='edit test'),
    path('all/tests/', AllQuestions.as_view(), name='allQuestions'),\

]