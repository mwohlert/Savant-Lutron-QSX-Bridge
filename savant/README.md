# Savant to Lutron QSX adapter

## On the Savant side
Savant requires a Lutron QSX profile with configured lighting table to be able to talk to the LEAP server on the Savant host. <br>
First, add the provided driver to your Racepoint Blueprint configuration. Configure the host address as "LOCALHOST" and leave the port as default. <br>
Next we take a look at the Lutron Integration Table, see the example below: <br> <br>
<img src="Integration Report Sample.png" alt="Integration Report Sample" width="1000"/> <br> <br>
We only care about the Button and LED IDs in our case and remember them for the next step. <br>
Now we open the lighting table under "Tools > Settings > Lighting" and start filling it in: <br> <br>
First half: <br>
<img src="Lighting table p1.png" alt="Lighting table p1" width="1000"/> <br> <br>
Second half: <br>
<img src="Lighting table p2.png" alt="Lighting table p2" width="1000"/> <br> <br>

**Enabled:** Check this box<br>
**Identifier:** An ongoing id<br>
**Controller:** Select the name for the profile instance<br>
**Location:** Select Savant location where the Keypad Button is present<br>
**Entity:** Select "Keypad Button"<br>
**Type:** Leave blank<br>
**Technology:** Leave blank<br>
**Button Label:** Type the name of the Button label<br>
**Toggle Label:** Type the name of the Button label<br>
**Label:** Type the name of the Button label<br>
**Savant Keypad:** Leave blank<br>
**UI Type:** Select "Toggle"<br>
**Command Type:** Select "Push Command"<br>
**Command:** Select "ButtonPressAndRelease"<br>
**Address [1]:** Fill in the ID of the /button/{id} part of Integration report<br>
**Address [2]:** Fill in the ID of the /led/{id} part of Integration report<br>
**Address [3]:** Leave blank<br>
**Address [4]:** Leave blank<br>
**Address [5]:** Leave blank<br>
**Address [6]:** Leave blank<br>
**Lights Are On:** Uncheck this box<br>
**Savant App Scene:** Uncheck this box<br>
**Savant App Group:** Select "Button"<br>
**Room Off Scene:** Select "Don't control"<br>
**Whole House Off Scene:** Select "Don't control"<br>
**Dimmer Level:** Leave blank<br>
**Fade Time:** Leave blank<br>
**Delay Time:** Leave blank<br>
**State [1]:** Open this field and fill the LED ID field with /led/{id} part of Integration report<br>
**State [2]:** Leave blank<br>
**Network Key:** Leave "0"<br>
**BLE ID:** Leave blank<br> <br>

After configuring everything the configuration can be uploaded the lighting buttons will populate in their respective rooms.