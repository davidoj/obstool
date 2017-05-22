from django.shortcuts import render
from wq.db.rest.views import ModelViewSet
from rest_framework.decorators import detail_route
from .models import DataObservation
from .serializers import SimpleDataObservationSerializer
from rest_pandas import PandasView

class DataObservationView(PandasView):
    queryset = DataObservation.objects.all()
    serializer_class = SimpleDataObservationSerializer

    def filter_queryset(self,qs):
        d = self.request.GET.dict()
        for param in d:
            if param in ('teacher','observer','date','obsnum'):
                qs = qs.filter(**{param:d[param]})
            elif param=='school':
                qs = qs.filter(teacher__school=d['school'])
            elif param=='region':
                qs = qs.filter(teacher__school__region=d['region'])
            elif param in ('kti','fb','ipt'):
                qs = qs.filter(**{param:True})

        return qs


class QStringModelViewSet(ModelViewSet):

    @detail_route()
    def edit(self, request, *args, **kwargs):
        """
        Generates a context appropriate for editing a form
        """
        response = super(QStringModelViewSet, self).edit(request, *args, **kwargs)
        parms = request.GET.dict()
        for arg in self.ignore_kwargs:
            parms.pop(arg,None)
        for key in parms:
            response.data[key] = parms[key]
        return response

    def new(self, request):
        """
        new is a variant of the "edit" action, but with no existing model
        to lookup.
        """
        response = super(QStringModelViewSet, self).new(request)
        parms = request.GET.dict()
        for arg in self.ignore_kwargs:
            parms.pop(arg,None)
        for key in parms:
            response.data[key] = parms[key]
        return response

