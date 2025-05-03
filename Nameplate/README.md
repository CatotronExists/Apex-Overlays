# Apex Overlays: Nameplate
This is a basic nameplate overlay that dynamically updates the username on a custom nameplate based on who is currently being spectated.

## Usage
1. Follow setup instructions below to set up the overlay.
2. Start Apex Legends
3. Run ```main.py``` and it will automatically detect when a game begins and ends.
4. Thats it!

## Setup
On top of these [basic requirements](https://github.com/CatotronExists/Apex-Overlays/tree/main#requirements), you will also need to install:\
obs-websocket-py ```pip install obs-websocket-py```

In OBS import your nameplate overlay as an image and adjust as needed.\
Then, add a new text box and adjust the font and size as needed then postion it on the nameplate.\
(Make sure the text box is above the nameplate image in the sources list)

Now download and open ```main.py``` and adjust the following variables:
- ```observer_name``` - The name of the observer. 
- ```scene``` - The name of the scene in OBS where the nameplate is located.
- ```text_box``` - The name of the text box in OBS.
- ```nameplate``` - The name of the nameplate image in OBS.

Optionally you can also adjust:
- ```password```

*You can open python files using VSCode or open in notepad*

![Guide](https://github.com/user-attachments/assets/9e04ecd3-a6a4-46ac-a0f6-3cec5ff3acb5)

In OBS, go to Tools > WebSocket Server Settings and "Enable WebSocket server".\
Ensure the port is set to 4455 and the password is set to the same password as in ```main.py```.\
Click "Apply" and "OK".

Setup is now complete.\
*You can also now hide both the nameplate image and text box in OBS if you want as they automatically show when the game begins.*

## Example Video
https://github.com/user-attachments/assets/f685470f-d05a-45a4-a874-1ff0b13ddbf5

*Nameplate and text box both appear when a game begins and then both disappear when the game ends.*\
*Here I am reading data from a file to simulate what this looks like*