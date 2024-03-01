from rest_framework import viewsets, permissions
from apps.aidetect.models import HumanHelth
from apps.aidetect.serializer import HumanHelthSerializer

class HumanHelthViewSet(viewsets.ModelViewSet):
    queryset = HumanHelth.objects.all()
    serializer_class = HumanHelthSerializer
    permission_classes = [permissions.AllowAny]
