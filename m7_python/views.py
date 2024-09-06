from django.shortcuts import render
from .services import get_all_inmuebles


def indexView(req):
    inmuebles=get_all_inmuebles()
    return render(req, 'index.html',{'inmuebles':inmuebles})