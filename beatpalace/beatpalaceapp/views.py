from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse

def Index(request):
    return HttpResponse("Hello")
