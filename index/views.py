from urllib.parse import urlencode
from json import loads
from django.shortcuts import render
from requests import post
from index.secret import clientID, clientSecret
from index.models import Tokens
from index.get_ip import get_client_ip


def index(request):
    parms = {
        "client_id": clientID,
        "response_type": "code",
        "redirect_uri": "http://localhost:8000/option",
        "scope": "user-library-read user-library-modify"
    }
    parms = urlencode(parms)
    url = "https://accounts.spotify.com/authorize?"
    url = url + parms
    context = {
        "url": url,
    }
    return render(request, "index.html", context)


def option(request):
    code = request.GET['code']
    parms = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/option",
        "client_id": clientID,
        "client_secret": clientSecret
    }
    result = loads(
        post("https://accounts.spotify.com/api/token", data=parms).text)
    try:
        ip_address = get_client_ip(request)
        defaults = {
            'access_token': result["access_token"],
            'refresh_token': result["refresh_token"],
            'ip_address': ip_address,
        }
        Tokens.objects.update_or_create(
            ip_address=ip_address, defaults=defaults)
    except KeyError:
        return render(request, "error.html")
    return render(request, "option.html")
