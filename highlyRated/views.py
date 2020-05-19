from json import loads
from django.shortcuts import render
from requests import get, put
from highlyRated.models import HighlyRatedAlbums
from index.models import Tokens
from index.get_ip import get_client_ip
from databases.models import AllHighlyRatedAlbums
from databases.views import updateDatabases


def highly_rated(request):
    ip_address = get_client_ip(request)
    access_token = Tokens.objects.get(ip_address=ip_address).access_token

    if request.method == 'POST':
        for album in request.POST:
            try:
                HighlyRatedAlbums.objects.get(
                    ip_address=ip_address, album=album).delete()
            except HighlyRatedAlbums.DoesNotExist:
                continue

    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        updateDatabases()
        HighlyRatedAlbums.objects.filter(ip_address=ip_address).delete()
        page = 1

    upperbound = int(10 * page)
    lowerbound = upperbound - 10
    text_albums = AllHighlyRatedAlbums.objects.all().order_by(
        '-date')[lowerbound:upperbound]
    for album in text_albums:
        try:
            HighlyRatedAlbums.objects.get(
                album=album.album, artist=album.artist)
            continue
        except HighlyRatedAlbums.DoesNotExist:
            head = {"authorization": "Bearer " + access_token}
            parms = {"q": "album:" + album.album + " artist:" + album.artist,
                     "type": "album", "market": "US", "limit": "1", "offset": "0"}
            result = loads(get("https://api.spotify.com/v1/search",
                               params=parms, headers=head).text)
            try:
                alb = HighlyRatedAlbums(
                    album=album.album,
                    artist=album.artist,
                    spotifyID=result["albums"]["items"][0]["id"],
                    ip_address=ip_address,
                )
                alb.save()
            except (KeyError, IndexError):
                continue

    page += 1
    context = {
        "albums": text_albums,
        "page": page,
    }

    return render(request, "highly-rated.html", context)


def added(request):
    ip_address = get_client_ip(request)
    tokens = Tokens.objects.get(ip_address=ip_address)
    for album in request.POST:
        try:
            HighlyRatedAlbums.objects.get(
                ip_address=ip_address, album=album).delete()
        except HighlyRatedAlbums.DoesNotExist:
            continue

    ids = "ids="
    id_list = []
    for album in HighlyRatedAlbums.objects.filter(ip_address=ip_address):
        id_list.append(album.spotifyID)
    for id_num in id_list:
        ids += id_num + ','
    ids = ids[:-1]

    head = {"authorization": "Bearer " + tokens.access_token}
    skips = loads(get("https://api.spotify.com/v1/me/albums/contains?" + ids,
                      headers=head).text)

    ids = "ids="
    for i in range(len(id_list)):
        if skips[i]:
            continue
        ids += id_list[i] + ','
    if len(ids) > 4:
        ids = ids[:-1]
        result = put("https://api.spotify.com/v1/me/albums?" +
                     ids, headers=head)
        if result.status_code >= 200:
            outcome = "added albums to library"
        else:
            outcome = "unable to add to library"
    else:
        outcome = "all albums already in library"
    context = {
        "outcome": outcome
    }
    HighlyRatedAlbums.objects.filter(ip_address=ip_address).delete()
    return render(request, "added.html", context)
