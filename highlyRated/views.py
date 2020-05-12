from json import loads
from django.shortcuts import render
from requests import get, put
from highlyRated.models import HighlyRatedAlbums
from highlyRated.getPitchfork import getArtistsAndAlbums
from index.models import Tokens
from index.get_ip import get_client_ip


def highly_rated(request):
    text_albums = getArtistsAndAlbums()
    while len(text_albums) > 10:
        text_albums.pop(-1)
    ip_address = get_client_ip(request)
    access_token = Tokens.objects.get(ip_address=ip_address).access_token
    for album in text_albums:
        head = {"authorization": "Bearer " + access_token}
        parms = {"q": "album:" + album[1] + " artist:" + album[0],
                 "type": "album", "market": "US", "limit": "1", "offset": "0"}
        result = loads(get("https://api.spotify.com/v1/search",
                           params=parms, headers=head).text)
        try:
            alb = HighlyRatedAlbums(
                album=album[1],
                artist=album[0],
                spotifyID=result["albums"]["items"][0]["id"],
                ip_address=ip_address,
            )
            alb.save()
        except KeyError:
            continue

    albums = HighlyRatedAlbums.objects.filter(ip_address=ip_address)[:10]
    context = {
        "albums": albums,
    }

    return render(request, "highly-rated.html", context)


def added(request):
    ip_address = get_client_ip(request)
    tokens = Tokens.objects.get(ip_address=ip_address)
    skip_these = request.POST
    ids = "ids="
    id_list = []
    for album in HighlyRatedAlbums.objects.filter(ip_address=ip_address)[:10]:
        if album.album in skip_these:
            continue
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
