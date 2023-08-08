from django.shortcuts import render, redirect

from dal import autocomplete
from .models import Brands

class BrandAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Brands.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs