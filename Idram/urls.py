from django.urls import path
from .views import PAYAPIView, PayForEvaluate, PayForVoting


urlpatterns = [
    path("i-pay/", PAYAPIView.as_view()),
    path("pay_evaluate/", PayForEvaluate.as_view()),
    path("pay_voting/", PayForVoting.as_view()),
]
