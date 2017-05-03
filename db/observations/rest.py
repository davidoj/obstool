from wq.db import rest
from .models import Teacher, School, DataObservation, Observer, Obsform, ReviewObservation, Item
from .serializers import DataObservationSerializer, ObsformSerializer, ReviewObservationSerializer

rest.router.register_model(Teacher, fields='__all__')
rest.router.register_model(School, fields='__all__')
rest.router.register_model(DataObservation, serializer=DataObservationSerializer)
rest.router.register_model(Observer, fields='__all__')
rest.router.register_model(Obsform, serializer=ObsformSerializer)
rest.router.register_model(ReviewObservation, serializer=ReviewObservationSerializer)
rest.router.register_model(Item, fields='__all__')