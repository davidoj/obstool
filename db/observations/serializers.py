from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
from .models import InteractionObservation, Observation

class InteractionObservationSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = InteractionObservation
        exclude = ('observation',)
        object_field = 'observation'
        wq_config = {
            'initial': 20,
        }

class ObservationSerializer(patterns.AttachedModelSerializer):
    interactionobservations = InteractionObservationSerializer(many=True)
    class Meta:
        model = Observation
        fields = '__all__'
