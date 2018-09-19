import json
from urllib import request as url


class Summoner:
    def __init__(self, key, name=str, region=str):
        self.name = name
        self.key = key
        self.loaded = None
        self.region = region
        self.region_url = None

    def get_summoner_info(self):
        if self.region_url is None:
            self.region_url = "euw1"
        url_construct = 'https://%s.api.riotgames.com/lol/summoner/v3/summoners/by-name/%s?api_key=%s' % (self.region_url, self.name, self.key)
        url_data = url.urlopen(url_construct).read()
        self.loaded = json.loads(url_data)

    @staticmethod
    def get_icon(icon_id):
        url_construct = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/%d.png' % icon_id
        return url_construct

    def region_check(self):
        if self.region == "euw" or "euwest":
            self.region_url = "euw1"
        elif self.region == "na":
            self.region_url = "na1"
        elif self.region == "eune" or "eun":
            self.region_url = "eun1"
        elif self.region == "ru" or "russia":
            self.region_url = "ru"
        elif self.region == "jp" or "japan":
            self.region_url = "jp1"
        elif self.region == "kr" or "korea":
            self.region_url = "kr"
        elif self.region == "br" or "brazil":
            self.region_url = "br1"
        elif self.region == "lan":
            self.region_url = "la1"
        elif self.region == "las":
            self.region_url = "la2"
        elif self.region == "oc" or "oce" or "oceania":
            self.region_url = "oc1"
        elif self.region == "tr" or "turkey" or "tur":
            self.region_url = "tr1"
        elif self.region == "pbe" or "beta":
            self.region_url = "pbe1"


class JsonSummoner(Summoner):
    def __init__(self, summoner_object):
        Summoner.__init__(self, summoner_object.key, name=summoner_object.name)
        self.profileIcon = summoner_object.loaded.get("profileIconId")
        self.name = summoner_object.loaded.get("name")
        self.level = summoner_object.loaded.get("summonerLevel")
        self.id = summoner_object.loaded.get("accountId")


class Status(Summoner):
    def __init__(self, key, region):
        Summoner.__init__(None, key, None, region)

    def get_status(self):
        if self.region_url is None:
            self.region_url = "euw1"
        url_construct = 'https://%s.api.riotgames.com/lol/status/v3/shard-data?api_key=%s' % (self.region_url, self.key)
        url_data = url.urlopen(url_construct).read()
        self.loaded = json.loads(url_data)


class JsonStatus(Status):
    def __init__(self, status_object):
        Status.__init__(status_object.key, status_object.region)
        self.game_status = status_object.loaded.get[0].get("status")
        print(self.game_status)


if __name__ == "__main__":
    summoner_name = input("Summoner name: ")
    summoner_region = input("Region: ")
    riot_token = open("riot_token.txt", "r")
    RIOT_TOKEN = riot_token.read()
    summoner = Summoner(RIOT_TOKEN, region=str(summoner_region), name=str(summoner_name))
    summoner.region_check()
    summoner.get_summoner_info()

    print(summoner.loaded)
