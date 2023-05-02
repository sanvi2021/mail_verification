from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField(
        allow_empty_file=False,
        allow_null=False
    )

    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise ValidationError('Invalid file type. Please upload a CSV file.')
        return value

class SinglefieldSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=None, allow_blank=False)

