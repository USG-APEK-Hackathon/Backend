from rest_framework import viewsets, permissions
from apps.aidetect.llm import process_message
from apps.aidetect.models import FirstStep, HumanHelth
from apps.aidetect.serializer import FirstStepSerializer, GPTSerializer, HumanHelthSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
import requests
from decouple import config

class HumanHelthViewSet(viewsets.ModelViewSet):
    queryset = HumanHelth.objects.all()
    serializer_class = HumanHelthSerializer
    permission_classes = [permissions.AllowAny]


class FirstStepViewSet(viewsets.ModelViewSet):
    queryset = FirstStep.objects.all()
    serializer_class = FirstStepSerializer
    permission_classes = [permissions.AllowAny]


class ProcessMessageView(CreateAPIView):
    serializer_class = GPTSerializer
    queryset = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = GPTSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data["message"]
            ans = process_message(message)
            return Response(
                {"message": ans},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
