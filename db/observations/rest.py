from wq.db import rest
from django.db.models import Q
from .models import School, DataObservation, Obsform, ReviewObservation, Item, Profile
from .serializers import DataObservationSerializer, ObsformSerializer, ReviewObservationSerializer
from .views import QStringModelViewSet

def my_observations(qs, request):
    return qs.filter(Q(teacher=request.user.profile) | Q(observer=request.user.profile))

def teacher_by_school(qs, request):
    rq = request.GET.dict()
    if 'school' in rq:
        return qs.filter(school=rq['school'])
    return qs

rest.router.register_model(
    School, 
    fields='__all__')

rest.router.register_model(
    DataObservation, 
    serializer=DataObservationSerializer, 
    viewset=QStringModelViewSet,
    cache_filter=my_observations)

rest.router.register_model(
    Profile,
    fields='__all__',
    cache='all',
    filter=teacher_by_school)

rest.router.register_model(
    Obsform, 
    serializer=ObsformSerializer)

rest.router.register_model(
    ReviewObservation, 
    serializer=ReviewObservationSerializer)

rest.router.register_model(
    Item, 
    fields='__all__')