from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
from .models import FBInteraction, FeedbackObservation

class FBSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = FBInteraction
        exclude = ('observation',)
        object_field = 'observation'
        wq_config = {
            'initial': 15,
        }

class FBObservationSerializer(patterns.AttachedModelSerializer):
    interactions = FBSerializer(many=True)
    class Meta:
        model = FeedbackObservation
        fields = '__all__'
