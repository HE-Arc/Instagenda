from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def backend_status(request):
    return JsonResponse({"status": 'Working!'})