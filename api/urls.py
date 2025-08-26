from django.urls import path, include
from .views import *
urlpatterns = [
    path('/group/', GroupAdd.as_view(), name='add'),
    path('/group/<int:group_id>/', GroupEditor.as_view(), name='edit group'),
    path('/group/<int:group_id>/questions/', AddQuestion.as_view(), name='addtest'),
    path('/group/<int:group_id>/questions/<int:question_id>/', EditQuestion.as_view(), name='edit test'),
    path('/all/', AllQuestions.as_view(), name='allQuestions'),
    path('/jointest/<int:group_id>/<int:question_id>/', TestGame.as_view(), name='jointest'),
    path('/results/<int:group_id>/', GroupResultsUser.as_view(), name='results_user'),
]