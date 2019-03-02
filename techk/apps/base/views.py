# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer
from rest_framework import generics
from django.http import Http404
from rest_framework.response import Response
from rest_framework.request import clone_request


class AllowPUTAsCreateMixin(generics.UpdateAPIView):
    """
    The following mixin class may be used in order to support PUT-as-create
    behavior for incoming requests.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance is None:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup_value = self.kwargs[lookup_url_kwarg]
            extra_kwargs = {self.lookup_field: lookup_value}
            self.perform_create(serializer, **extra_kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.perform_udpate(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            if self.request.method == 'PUT':
                # For PUT-as-create operation, we need to ensure that we have
                # relevant permissions, as if this was a POST request.  This
                # will either raise a PermissionDenied exception, or simply
                # return None.
                self.check_permissions(clone_request(self.request, 'POST'))
            else:
                # PATCH requests where the object does not exist should still
                # return a 404 response.
                raise



    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)

        def perform_udpate(self, serializer):
            serializer.save()


class CategoryCreate(AllowPUTAsCreateMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookCreate(AllowPUTAsCreateMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookList(generics.ListAPIView, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
