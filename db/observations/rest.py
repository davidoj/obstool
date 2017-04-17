from wq.db import rest
from .models import Teacher, School, FeedbackObservation, Observer
from .serializers import FBObservationSerializer

rest.router.register_model(Teacher, fields='__all__')
rest.router.register_model(School, fields='__all__')
rest.router.register_model(FeedbackObservation, serializer=FBObservationSerializer)
rest.router.register_model(Observer, fields='__all__')