from rest_framework.viewsets import ModelViewSet
from core.models import UserAiQuestion, UserImageAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer

class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

