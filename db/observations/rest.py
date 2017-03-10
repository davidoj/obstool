from wq.db import rest
from .models import Teacher, School, Observation, Observer
from .serializers import ObservationSerializer

rest.router.register_model(Teacher, fields='__all__')
rest.router.register_model(School, fields='__all__')
rest.router.register_model(Observation, serializer=ObservationSerializer)
rest.router.register_model(Observer, fields='__all__')