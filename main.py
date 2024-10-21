import time
import requests
import valclient
from valclient.client import Client
from pystyle import Colors, Colorate
import os
import base64
import json

import valclient.exceptions

titletext = "[-- MINTYTOOL --] Made by Minty"

red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"

failed_task = f"{red}[! MINTYTOOL !]{white} Failed Task!!"
invalid_option = f"{red}[! MINTYTOOL !]{white} Invalid Option. Please choose from 1 ~ 3!!"

with open('config.json', 'r') as file:
    config = json.load(file)
        
api_key = config.get('api_key')
region = config.get('region')

class Player:
    agentMap = {
        "add6443a-41bd-e414-f6ad-e58d267f4e95": "Jett",
        "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc": "Reyna",
        "f94c3b30-42be-e959-889c-5aa313dba261": "Raze",
        "7f94d92c-4234-0a36-9646-3a87eb8b5c89": "Yoru",
        "eb93336a-449b-9c1b-0a54-a891f7921d69": "Phoenix",
        "bb2a4828-46eb-8cd1-e765-15848195d751": "Neon",
        "0e38b510-41a8-5780-5e8f-568b2a4f2d6c": "Iso",
        "5f8d3a7f-467b-97f3-062c-13acf203c006": "Breach",
        "6f2a04ca-43e0-be17-7f36-b3908627744d": "Skye",
        "320b2a48-4d9b-a075-30f1-1f93a9b638fa": "Sova",
        "601dbbe7-43ce-be57-2a40-4abd24953621": "KAY/O",
        "1e58de9c-4950-5125-93e9-a0aee9f98746": "Killjoy",
        "117ed9e3-49f3-6512-3ccf-0cada7e3823b": "Cypher",
        "569fdd95-4d10-43ab-ca70-79becc718b46": "Sage",
        "22697a3d-45bf-8dd7-4fec-84a9e28c69d7": "Chamber",
        "8e253930-4c05-31dd-1b6c-968525494517": "Omen",
        "9f0d8ba9-4140-b941-57d3-a7ad57c6b417": "Brimstone",
        "41fb69c1-4189-7b37-f117-bcaf1e96f1bf": "Astra",
        "707eab51-4836-f488-046a-cda6bf494859": "Viper",
        "1dbf2edd-4729-0984-3115-daa5eed44993": "Clove",
        "dade69b4-4f5a-8528-247b-219e5a1facd6": "Fade",
        "95b78ed7-4637-86d9-7e41-71ba8c293152": "Harbor",
        "e370fa57-4757-3604-3648-499e1f642d3f": "Gekko",
        "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235": "Deadlock",
        "efba5359-4016-a1e5-7626-b1ae76895940": "Vyse",
        "1": "Player 1",
        "2": "Player 2",
        "3": "Player 3",
        "4": "Player 4",
        "5": "Player 5"
    }

    def __init__(self, client, puuid, agentID, incognito, team):
        self.client = client
        self.puuid = puuid
        try:
            self.agent = self.agentMap[agentID]
        except:
            self.agent = "Player"
        self.incognito = incognito
        self.team = self.side(team)
        self.name = "N/A"
        self.tag = "N/A"
        self.full_name = "N/A#N/A"

    def side(self, color):
        if color == "Blue":
            return "Defending"
        else:
            return "Attacking"

    def set_name(self, puuid):
        try:
            playerData = requests.get(
                f"https://api.henrikdev.xyz/valorant/v1/by-puuid/account/{puuid}?api_key={api_key}"
            ).json()
        except Exception as e:
            print(e)
            print("Error fetching player data")

        try:
            name = playerData["data"]["name"]
            tag = playerData["data"]["tag"]
        except:
            name = "N/A"
            tag = "N/A"

        self.name = self.filter_name(name)
        self.tag = tag
        self.full_name = f"{name}#{tag}"

    def filter_name(self, name):
        if 'twitch' in name:
            return name.replace('twitch', '').strip()
        if 'ttv' in name:
            return name.replace('ttv', '').strip()
        return name

class Game:
    def __init__(self, party, matchID, players, localPlayer):
        self.matchID = matchID
        self.players = players
        self.localPlayer = localPlayer
        self.teamPlayers = self.find_team_players(self.localPlayer, self.players)
        self.partyPlayers = self.find_party_members(party)

    def find_hidden_names(self, players):
        self.found = False
        for player in players:
            if player.incognito:
                self.found = True
                player.set_name(player.puuid)
                if player in self.teamPlayers:
                    teamtext = f"{green}TEAM"
                else:
                    teamtext = f"{red}ENEMY"
                print(f"{blue}[+ MINTYTOOL +]{white} {player.full_name} | {player.team} {player.agent} ({teamtext}{white})")
        if not self.found:
            print(f"{red}[+ MINTYTOOL +]{white} No hidden names found")

    def find_team_players(self, localPlayer, players):
        team_players = [player for player in players if player.team == localPlayer.team]
        return team_players

    def find_party_members(self, party):
        members = [member['Subject'].lower() for member in party['Members']]
        return members

maps = {
    "7eaecc1b-4337-bbf6-6ab9-04b8f06b3319": {
        "display_name": "Ascent",
        "map_url": "/Game/Maps/Ascent/Ascent"
    },
    "d960549e-485c-e861-8d71-aa9d1aed12a2": {
        "display_name": "Split",
        "map_url": "/Game/Maps/Bonsai/Bonsai"
    },
    "b529448b-4d60-346e-e89e-00a4c527a405": {
        "display_name": "Fracture",
        "map_url": "/Game/Maps/Canyon/Canyon"
    },
    "2c9d57ec-4431-9c5e-2939-8f9ef6dd5cba": {
        "display_name": "Bind",
        "map_url": "/Game/Maps/Duality/Duality"
    },
    "2fb9a4fd-47b8-4e7d-a969-74b4046ebd53": {
        "display_name": "Breeze",
        "map_url": "/Game/Maps/Foxtrot/Foxtrot"
    },
    "2fe4ed3a-450a-948b-6d6b-e89a78e680a9": {
        "display_name": "Lotus",
        "map_url": "/Game/Maps/Jam/Jam"
    },
    "92584fbe-486a-b1b2-9faa-39b0f486b498": {
        "display_name": "Sunset",
        "map_url": "/Game/Maps/Juliett/Juliett"
    },
    "fd267378-4d1d-484f-ff52-77821ed10dc2": {
        "display_name": "Pearl",
        "map_url": "/Game/Maps/Pitt/Pitt"
    },
    "e2ad5c54-4114-a870-9641-8ea21279579a": {
        "display_name": "Icebox",
        "map_url": "/Game/Maps/Port/Port"
    },
    "ee613ee9-28b7-4beb-9666-08db13bb2244": {
        "display_name": "The Range",
        "map_url": "/Game/Maps/Poveglia/Range"
    },
    "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047": {
        "display_name": "Haven",
        "map_url": "/Game/Maps/Triad/Triad"
    },
    "224b0a95-48b9-f703-1bd8-67aca101a61f": {
        "display_name": "Abyss",
        "map_url": "/Game/Maps/Infinity/Infinity"
    },
    "690b3ed2-4dff-945b-8223-6da834e30d24": {
        "display_name": "District",
        "map_url": "/Game/Maps/HURM/HURM_Alley/HURM_Alley"
    },
    "12452a9d-48c3-0b02-e7eb-0381c3520404": {
        "display_name": "Kasbah",
        "map_url": "/Game/Maps/HURM/HURM_Bowl/HURM_Bowl"
    },
    "2c09d728-42d5-30d8-43dc-96a05cc7ee9d": {
        "display_name": "Drift",
        "map_url": "/Game/Maps/HURM/HURM_Helix/HURM_Helix"
    },
    "de28aa9b-4cbe-1003-320e-6cb3ec309557": {
        "display_name": "Piazza",
        "map_url": "/Game/Maps/HURM/HURM_Yard/HURM_Yard"
    },
    "5914d1e0-40c4-cfdd-6b88-eba06347686c": {
        "display_name": "The Range",
        "map_url": "/Game/Maps/PovegliaV2/RangeV2"
    }
}

def get_display_name_from_url(map_url):
    for uuid, map_info in maps.items():
        if map_info["map_url"] == map_url:
            return map_info["display_name"]
    return "Unknown Map URL"

def get_data_from_presences(data, player_name, player_tag):
    results = []
    for presence in data.get('presences', []):
        if isinstance(presence, dict) and presence.get('state') in ['dnd', 'chat', 'away'] and presence.get('product') == "valorant":
            private_encoded = presence.get('private', '')
            try:
                private_decoded = base64.b64decode(private_encoded).decode('utf-8')
                private_data = json.loads(private_decoded)
            except (base64.binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as e:
                print(f"Decoding error: {e}")
                private_data = {}

            game_name = presence.get('game_name')
            game_tag = presence.get('game_tag')

            if game_name == player_name and game_tag == player_tag:
                continue

            result = {
                'game_name': game_name,
                'game_tag': game_tag,
                'pid': presence.get('pid'),
                'sessionLoopState': private_data.get('sessionLoopState'),
                'map': get_display_name_from_url(private_data.get('partyOwnerMatchMap')),
                'partyOwnerMatchScoreAllyTeam': private_data.get('partyOwnerMatchScoreAllyTeam'),
                'partyOwnerMatchScoreEnemyTeam': private_data.get('partyOwnerMatchScoreEnemyTeam'),
                'matchMap': private_data.get('matchMap'),
                'queueId': private_data.get('queueId'),
                'partyState': private_data.get('partyState'),
                'state': presence.get('state')
            }

            results.append(result)
    return results

def print_friend_presences(presences):

    clear()
    print()

    friend_count = len(presences)

    print(f"{purple}[+ MINTYTOOL +]{white} Friends : {friend_count}\n")


    for presence in presences:
        
        if isinstance(presence, dict):
            game_name = presence.get("game_name", "")
            game_tag = presence.get("game_tag", "")
            sessionLoopState = presence.get("sessionLoopState", "")
            map = presence.get("map", "")
            partyOwnerMatchScoreAllyTeam = presence.get("partyOwnerMatchScoreAllyTeam", "")
            partyOwnerMatchScoreEnemyTeam = presence.get("partyOwnerMatchScoreEnemyTeam", "")
            queueId = presence.get("queueId", "").capitalize()
            if queueId == "":
                queueId = "Custom"
                
            partyState = presence.get("partyState", "")
            state = presence.get("state", "")
            if partyState == "DEFAULT":
                inQueue = False
            elif partyState == "MATCHMAKING":
                inQueue = True

            if state == "away":
                print(f"{yellow}[+ MINTYTOOL +]{white} {game_name}#{game_tag} | AWAY | ")
                continue

            if sessionLoopState == "MENUS" and inQueue == False:
                print(f"{green}[+ MINTYTOOL +]{white} {game_name}#{game_tag} | MENUS | ")

            elif sessionLoopState == "MENUS" and inQueue == True:
                print(f"{blue}[+ MINTYTOOL +]{white} {game_name}#{game_tag} | {queueId} | IN QUEUE | ")
            
            elif sessionLoopState == "PREGAME":
                print(f"{blue}[+ MINTYTOOL +]{white} {game_name}#{game_tag} | {queueId} | {map} | AGENT SELECT | ")

            else:
                print(f"{cyan}[+ MINTYTOOL +]{white} {game_name}#{game_tag} | {queueId} | {map} | {partyOwnerMatchScoreAllyTeam} - {partyOwnerMatchScoreEnemyTeam} | IN GAME |")

logo = f"""
   *     (        )             )             )      )   (     
 (  `    )\ )  ( /(   *   )  ( /(   *   )  ( /(   ( /(   )\ )  
 )\))(  (()/(  )\())` )  /(  )\())` )  /(  )\())  )\()) (()/(  
((_)()\  /(_))((_)\  ( )(_))((_)\  ( )(_))((_)\  ((_)\   /(_)) 
(_()((_)(_))   _((_)(_(_())__ ((_)(_(_())   ((_)   ((_) (_))   
|  \/  ||_ _| | \| ||_   _|\ \ / /|_   _|  / _ \  / _ \ | |    
| |\/| | | |  | .` |  | |   \ V /   | |   | (_) || (_) || |__  
|_|  |_||___| |_|\_|  |_|    |_|    |_|    \___/  \___/ |____| 


"""

def printascii():
    print(Colorate.Horizontal(Colors.cyan_to_blue, logo, 1))

def clear():
    os.system("cls")
    printascii()

def intromenu():
    clear()
    os.system(f"title {titletext}")

def main():
    running = True
    seenMatches = []
    seenPregame = []

    client = Client(region=region)
    try:
        client.activate()
    except valclient.exceptions.HandshakeError:
        print(f"\n{red}[+ MINTYTOOL +]{white} Please launch Valorant before starting this program.")
        exit()
    
    
    printascii()
    
    
    stateInterval = 5

    
    player_name = client.player_name
    player_tag = client.player_tag

    print(f"\n{cyan}[+ MINTYTOOL +]{white} Waiting for a match to begin")

    while running:
        time.sleep(stateInterval)
        try:
            sessionState = client.fetch_presence(client.puuid)['sessionLoopState']

            if sessionState == "PREGAME":
                matchID = client.pregame_fetch_player()['MatchID']
            elif sessionState == "INGAME":
                matchID = client.coregame_fetch_player()['MatchID']
            else:
                friendPresenceData = client.fetch_all_friend_presences()
                filteredPresenceData = get_data_from_presences(friendPresenceData, player_name, player_tag)
                print_friend_presences(filteredPresenceData)


            if sessionState == "PREGAME" and matchID not in seenPregame:
                
                
                seenPregame.append(matchID)
                matchInfo = client.pregame_fetch_match(matchID)

                map_url = matchInfo["MapID"]
                map_name = get_display_name_from_url(map_url)
                print(f"\n{green}[+ MINTYTOOL +]{white} Agent Select Detected | {map_name}")


                players = []
                localPlayer = None
                player_index = 0

                for team in matchInfo['Teams']:

                    for player in team['Players']:

                        agent_id = str(player_index + 1)

                        if client.puuid == player['Subject']:
                            localPlayer = Player(
                                client=client,
                                puuid=player['Subject'].lower(),
                                agentID=agent_id,
                                incognito=player['PlayerIdentity']['Incognito'],
                                team=team['TeamID']
                            )
                        else:
                            players.append(Player(
                                client=client,
                                puuid=player['Subject'].lower(),
                                agentID=agent_id,
                                incognito=player['PlayerIdentity']['Incognito'],
                                team=team['TeamID']
                            ))
                        player_index += 1

                currentGame = Game(party=client.fetch_party(), matchID=matchID, players=players, localPlayer=localPlayer)
                print(f"{cyan}[+ MINTYTOOL +]{white} Finding hidden names\n")
                currentGame.find_hidden_names(players)

            elif sessionState == "INGAME" and matchID not in seenMatches:
                

                seenMatches.append(matchID)
                matchInfo = client.coregame_fetch_match(matchID)

                map_url = matchInfo["MapID"]
                map_name = get_display_name_from_url(map_url)
                print(f"\n{green}[+ MINTYTOOL +]{white} Match Detected | {map_name}")

                players = []
                for player in matchInfo['Players']:
                    if client.puuid == player['Subject']:
                        localPlayer = Player(
                            client=client,
                            puuid=player['Subject'].lower(),
                            agentID=player['CharacterID'].lower(),
                            incognito=player['PlayerIdentity']['Incognito'],
                            team=player['TeamID']
                        )
                    else:
                        players.append(Player(
                            client=client,
                            puuid=player['Subject'].lower(),
                            agentID=player['CharacterID'].lower(),
                            incognito=player['PlayerIdentity']['Incognito'],
                            team=player['TeamID']
                        ))

                currentGame = Game(party=client.fetch_party(), matchID=matchID, players=players, localPlayer=localPlayer)
                print(f"{cyan}[+ MINTYTOOL +]{white} Finding hidden names\n")
                currentGame.find_hidden_names(players)

        
        except Exception as e:
            if "core" not in str(e) and "pre-game" not in str(e) and "NoneType" not in str(e):
                exit()

if __name__ == "__main__":
    main()

