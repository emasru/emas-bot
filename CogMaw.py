import json
from urllib import request as url
import asyncio
import aiohttp


class Summoner:
    def __init__(self, key, name=str):
        self.name = name
        self.key = key
        self.loaded = None
        self.profileIcon = None
        self.loaded_name = None
        self.level = None
        self.id = None

    async def get_summoner_info(self, region_url):
        try:
            url_construct = 'https://%s.api.riotgames.com/lol/summoner/v3/summoners/by-name/%s?api_key=%s' % (region_url, self.name, self.key)
            async with aiohttp.get(url_construct) as url_data:
                self.loaded = await url_data.json()
        except:
            pass

    @staticmethod
    def get_icon(icon_id):
        url_construct = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/profileicon/%s.png' % icon_id
        return url_construct

    @staticmethod
    def region_check(region):
        print("para", region)
        if region == "euw" or "euwest":
            region_url = "euw1"
        elif region == "na":
            region_url = "na1"
        elif region == "eune" or "eun":
            region_url = "eun1"
        elif region == "ru" or "russia":
            region_url = "ru"
        elif region == "jp" or "japan":
            region_url = "jp1"
        elif region == "kr" or "korea":
            region_url = "kr"
        elif region == "br" or "brazil":
            region_url = "br1"
        elif region == "lan":
            region_url = "la1"
        elif region == "las":
            region_url = "la2"
        elif region == "oc" or "oce" or "oceania":
            region_url = "oc1"
        elif region == "tr" or "turkey" or "tur":
            region_url = "tr1"
        elif region == "pbe" or "beta":
            region_url = "pbe1"
        else:
            region_url = "euw1"  # TODO ?????
        print("url", region_url)
        return region_url

    def json(self):
        self.profileIcon = self.loaded.get("profileIconId")
        self.loaded_name = self.loaded.get("name")
        self.level = self.loaded.get("summonerLevel")
        self.id = self.loaded.get("id")


class Status:
    def __init__(self, key):
        self.key = key
        self.loaded = None
        self.game_status = None
        self.store_status = None
        self.website_status = None
        self.client_status = None

    async def get_status(self, region_url):
        url_construct = 'https://%s.api.riotgames.com/lol/status/v3/shard-data?api_key=%s' % (region_url, self.key)
        async with aiohttp.get(url_construct) as url_data:
            self.loaded = await url_data.json()

    def json(self):
        self.game_status = self.loaded["services"][0]["status"]
        if self.game_status == "online":
            self.game_status = "Online"
        self.store_status = self.loaded["services"][1]["status"]
        if self.store_status == "online":
            self.store_status = "Online"
        self.website_status = self.loaded["services"][2]["status"]
        if self.website_status == "online":
            self.website_status = "Online"
        self.client_status = self.loaded["services"][3]["status"]
        if self.client_status == "online":
            self.client_status = "Online"


class Match:
    def __init__(self, key, player_id):
        self.player_id = player_id
        self.key = key
        self.loaded = None
        self.game_start_time = None
        self.game_length = None
        self.champion_id = None
        self.icon_id = None

    async def get_match(self, region_url):
        url_construct = 'https://%s.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/%s?api_key=%s' % (region_url, self.player_id, self.key)
        print(url_construct)
        async with aiohttp.get(url_construct) as url_data:
            self.loaded = await url_data.json()

    def json(self):
        self.game_start_time = self.loaded.get("gameStartTime")
        self.game_length = self.loaded.get("gameLength")

        i = 0
        while True:
            if self.loaded["participants"][i]["summonerId"] == self.player_id:
                break
            i += 1

        self.champion_id = self.loaded["participants"][i]["championId"]
        self.icon_id = self.loaded["participants"][i]["profileIconId"]  # TODO


if __name__ == "__main__":
    summoner_name = input("Summoner name: ")
    summoner_region = input("Region: ")
    riot_token = open("riot_token.txt", "r")
    RIOT_TOKEN = riot_token.read()
    summoner = Summoner(RIOT_TOKEN, region=str(summoner_region), name=str(summoner_name))
    summoner.region_check()
    summoner.get_summoner_info()

    print(summoner.loaded)
