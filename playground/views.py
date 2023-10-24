import http
from django.shortcuts import render
from django.core.mail import EmailMessage, BadHeaderError
from templated_mail.mail import BaseEmailMessage
from playground.tasks import notify_customers
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

class HelloView(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, request):

        try:
            logger.info("Calling httpbin")
            response = requests.get('https://httpbin.org/delay/2')       
            return render(request, "hello.html", {"name": "Courtney"})
            logger.info("returned response")
        
        except requests.ConnectionError:
            logger.critical("Httpbin is offline")