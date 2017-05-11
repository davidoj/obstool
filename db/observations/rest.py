from wq.db import rest
from .models import School, DataObservation, Obsform, ReviewObservation, Item, Profile
from .serializers import DataObservationSerializer, ObsformSerializer, ReviewObservationSerializer
from .views import QStringModelViewSet

rest.router.register_model(
    School, 
    fields='__all__')

rest.router.register_model(
    DataObservation, 
    serializer=DataObservationSerializer, 
    viewset=QStringModelViewSet)

rest.router.register_model(
    Profile,
    fields='__all__',
    cache='all')

rest.router.register_model(
    Obsform, 
    serializer=ObsformSerializer)

rest.router.register_model(
    ReviewObservation, 
    serializer=ReviewObservationSerializer)

rest.router.register_model(
    Item, 
    fields='__all__')