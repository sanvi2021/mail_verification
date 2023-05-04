from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class DomainRecordSerializer(serializers.Serializer):
    domain_name = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    
    def validate_domain_name(self,value):
        if not value.endswith('.com'):
            raise ValidationError('Invalid url. Please upload correct Url.')
        return value