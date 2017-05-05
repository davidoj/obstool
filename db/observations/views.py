from django.shortcuts import render
from wq.db.rest.views import ModelViewSet
from rest_framework.decorators import detail_route



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