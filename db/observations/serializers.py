from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
from .models import MbMData, DataObservation, NumberedResult, ReviewObservation, Item, Obsform, School, SIData

class SISerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = SIData
        exclude = ('observation',)
        object_field = 'observation'
        wq_config = {
            'initial': 3
        }

class ItemSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Item
        exclude = ('form',)
        object_field= 'form'

class ObsformSerializer(patterns.AttachedModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Obsform
        fields = '__all__'

class MbMSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = MbMData
        exclude = ('observation',)
        object_field = 'observation'
        wq_config = {
            'initial': 15,
        }

class DataObservationSerializer(patterns.AttachedModelSerializer):
    interactions = MbMSerializer(many=True)
    studentinterviews = SISerializer(many=True)

    class Meta:
        model = DataObservation
        fields = '__all__'
        wq_field_config = {
            'teacher' : {'filter': {'school_id' : '{{school}}'}}
        }

class NumberedResultSerializer(patterns.TypedAttachmentSerializer):
    class Meta(patterns.TypedAttachmentSerializer.Meta):
        model = NumberedResult
        exclude = ('observation',)
        object_field = 'observation'
        type_field = 'item'
        type_filter = {'form_id' : '{{form_id}}'}


class ReviewObservationSerializer(patterns.AttachedModelSerializer):
    results = NumberedResultSerializer(many=True)


    class Meta:
        model = ReviewObservation
        fields = '__all__'
