from rest_framework import serializers
from apps.aidetect.main import check_for_anomaly
from rest_framework.serializers import Serializer, CharField

from apps.aidetect.models import HumanHelth, FirstStep

class HumanHelthSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanHelth
        fields = '__all__'
        read_only_fields = ['anomaly_message']

    def create(self, validated_data):
        validated_data['anomaly_message'] = check_for_anomaly(
            [validated_data['calorie'], validated_data['step_count'], validated_data['active_time']]
        )['message']
        return super().create(validated_data)

class FirstStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstStep
        fields = '__all__'
        read_only_fields = ['detected_emotion']

    def create(self, validated_data):
        validated_data['detected_emotion'] = "daw"
        return super().create(validated_data)

class GPTSerializer(Serializer):
    message = CharField(required=True, allow_blank=False, max_length=1000)
