from rest_framework import serializers
from apps.aidetect.main import check_for_anomaly

from apps.aidetect.models import HumanHelth

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
