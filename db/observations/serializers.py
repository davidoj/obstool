from wq.db.rest.serializers import ModelSerializer
from wq.db.patterns import serializers as patterns
from .models import FBInteraction, FeedbackObservation, NumberedResult, ReviewObservation, Item, Obsform

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

class NumberedResultSerializer(patterns.TypedAttachmentSerializer):
    class Meta(patterns.TypedAttachmentSerializer.Meta):
        model = NumberedResult
        exclude = ('observation',)
        object_field = 'observation'
        type_field = 'item'
        type_filter = {'form_id' : '{{form_id}}'}
        # wq_config = {
        #     'initial':{'type_field': 'item_id', 'type_filter':{}}
        # }
        #{'form_id' : '{{form_id}}'}

class ReviewObservationSerializer(patterns.AttachedModelSerializer):
    results = NumberedResultSerializer(many=True)

    # def to_representation(self, obj):
    #     result = super(ReviewObservationSerializer, self).to_representation(obj)

    #     obsform_id = (
    #         'request' in self.context and
    #         self.context['request'].GET.get('form_id', None)
    #     )
    #     if not obsform_id:
    #         return result

    #     result['results'] = [
    #         {
    #             '@index': i,
    #             'item_label': str(item),
    #             'item_desc': item.description,
    #             'item_id': item.id,
    #             'score_choices' : [{'name':1,
    #                                 'label':'1 (No evidence)'},
    #                               {'name':2,
    #                                'label':'2 (Little evidence)'},
    #                               {'name':3,
    #                                'label':'3 (Some evidence)'},
    #                               {'name':4,
    #                                'label':'4 (Lots of evidence)'},
    #                               {'name':5,
    #                                'label':'5 (Great deal of evidence)'}]
    #         }
    #         for i, item in enumerate(Item.objects.filter(
    #             form__id=obsform_id
    #         ))
    #     ]
    #     return result

    class Meta:
        model = ReviewObservation
        fields = '__all__'
