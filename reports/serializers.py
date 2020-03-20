from rest_framework import routers, serializers, viewsets
from reports.models import GlobalProtectEvent
class GlobalProtectEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GlobalProtectEvent
        fields = '__all__'