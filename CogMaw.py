import json
from urllib import request as url


class Summoner:
    def __init__(self, key, **region, **name):
        self.name = name["name"]
        self.key = key
        self.loaded = None
        self.region = region

    def get_summoner_info(self):
        if self.region is None:
            self.region = "euw1"
        try:
            url_construct = 'https://%s.api.riotgames.com/lol/summoner/v3/summoners/by-name/%s?api_key=%s' % (self.region, self.name, self.key)
            url_data = url.urlopen(url_construct).read()
            self.loaded = json.loads(url_data)
        except url.HTTPError:
            return 1

    @staticmethod
    def get_icon(icon_id):
        url_construct = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/%d.png' % icon_id
        return url_construct

    def region_check(self):
        region_url = None
        if self.region == "euw":
            region_url = "euw1"
        if self.region == "na":
            region_url = "na1"
        return region_url


class Json(Summoner):
    def __init__(self, summoner_object):
        Summoner.__init__(self, summoner_object.key, name=summoner_object.name)
        self.profileIcon = summoner_object.loaded.get("profileIconId")
        self.name = summoner_object.loaded.get("name")
        self.level = summoner_object.loaded.get("summonerLevel")
        self.id = summoner_object.loaded.get("accountId")
