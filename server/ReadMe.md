1. `python3 gps.py` to start the python app
2. `node app.js` to start the server
3. connect the receiver, transmitter and the laptop to the same transmitter's wifi hotspot
4. Find the local IP of the laptop using ifconfig and setup the app send data to the specific IP
5. receiver sends data to the /rec path
6. transmitter sends data to the /trans path
7. send a get request to the /map path to get the map generated