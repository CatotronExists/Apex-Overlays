import LiveApex
import asyncio
from obswebsocket import obsws, requests

#per_legend_plate = False # Set to True if you want to have a different nameplate for each legend, otherwise a single nameplate will be used for all legends/players
observer_name = "" # This is the name of the observer in Apex Legends, required as multiple observers can be present in the game
scene = ""  # This is the name of the scene in OBS
text_box = "" # This is the name of the text box in OBS
name_plate = "" # This is the name of the nameplate in OBS
host = "localhost"
port = 4455
password = "PASSWORD" # This is the password for the OBS WebSocket server, set in the OBS WebSocket settings

ws = obsws(host, port, password)

async def filter_events(event):
    if event != None:
        if 'category' in event:
            if event['category'] == "gameStateChanged":
                if event['state'] == "Playing": # Show plate and text when game state is Playing
                    ws.connect()
                    response = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName=name_plate)) # Enable nameplate
                    print(response)
                    itemId = response.datain['sceneItemId']
                    ws.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=itemId, sceneItemEnabled=True))

                    response = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName=text_box)) # Enable text box
                    itemId = response.datain['sceneItemId']
                    ws.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=itemId, sceneItemEnabled=True))
                    ws.disconnect()

                if event['state'] == "Resolution": # Hide plate and text when game state is Resolution
                    ws.connect()
                    response = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName=name_plate)) # Disable nameplate
                    itemId = response.datain['sceneItemId']
                    ws.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=itemId, sceneItemEnabled=False))

                    response = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName=text_box)) # Disable text box
                    itemId = response.datain['sceneItemId']
                    ws.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=itemId, sceneItemEnabled=False))
                    ws.disconnect()

            if event['category'] == "observerSwitched": # Change text to new player name when observer switches
                if event['observer']['name'] == observer_name: # Check if the observer is the one we are interested in
                    player_username = event['target']['name']
                    ws.connect()
                    ws.call(requests.SetInputSettings(inputName=text_box, inputSettings={"text": player_username})) # Change text to new player name
                    ws.disconnect()

async def main():
    # Start the API
    api_task = asyncio.create_task(LiveApex.Core.startLiveAPI())
    listener_task = asyncio.create_task(LiveApex.Core.startListener(filter_events))

    await asyncio.gather(api_task, listener_task)

asyncio.run(main())