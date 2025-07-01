import LiveApex
import asyncio
from obswebsocket import obsws, requests

in_folder = False # Set to True if you want to have both the text_box and name_plate in a folder
folder_name = "" # This is the name of the folder where both elements are placed, not required if elements are not in a folder
observer_name = "" # This is the name of the observer in Apex Legends, required as multiple observers can be present in the game
scene = "" # This is the name of the scene in OBS
text_box = "" # This is the name of the text box in OBS
name_plate = "" # This is the name of the nameplate in OBS
host = "localhost"
port = 4455
password = "PASSWORD" # This is the password for the OBS WebSocket server, set in the OBS WebSocket settings

ws = obsws(host, port, password)

async def filter_events(event):
    if event != None:
        if 'category' in event:
            if event['category'] == "init":
                print("[LiveApex] Connected to Apex Legends")
            if event['category'] == "gameStateChanged":
                if event['state'] == "Playing": # Show plate and text when game state is Playing
                    ws.connect()

                    target = [text_box, name_plate]
                    if in_folder == True:
                        response = ws.call(requests.GetGroupSceneItemList(sceneName=folder_name))

                        scene_items = response.getSceneItems()
                        scene_item_ids = [item['sceneItemId'] for item in scene_items if item.get('sourceName') in target and 'sceneItemId' in item]
                        
                        for id in scene_item_ids:
                            ws.call(requests.SetSceneItemEnabled(sceneName=folder_name, sceneItemId=id, sceneItemEnabled=True)) # Enable item

                    else:
                        for item in target:
                            response = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName=item)) # Enable item
                            itemId = response.datain['sceneItemId']
                            ws.call(requests.SetSceneItemEnabled(sceneName=scene, sceneItemId=itemId, sceneItemEnabled=True))

                    ws.disconnect()

                if event['state'] == "Resolution": # Hide plate and text when game state is Resolution
                    ws.connect()

                    target = [text_box, name_plate]
                    if in_folder == True:
                        response = ws.call(requests.GetGroupSceneItemList(sceneName=folder_name))

                        scene_items = response.getSceneItems()
                        scene_item_ids = [item['sceneItemId'] for item in scene_items if item.get('sourceName') in target and 'sceneItemId' in item]

                        for id in scene_item_ids:
                            ws.call(requests.SetSceneItemEnabled(sceneName=folder_name, sceneItemId=id, sceneItemEnabled=False)) # Disable item

                    else:
                        for item in target:
                            response = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName=item)) # Disable item
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
