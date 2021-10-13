# Savant-Lutron-QSX-Bridge

This project aims to bring rudamentary HomeWorks QSX compatiblity to Savant using a python server, translating telnet style savant lighting driver commands to the new Lutron LEAP protocol used with the QSX.

## Usage

Run setup.py

```shell
python setup.py install
```

After that run get_lutron_cert.py to generate a client cert with the lutron processor.
Now you can start the lutron server.

Modify the plist with your paths and move it to ~/Library/LaunchAgents and load it using `launchctl load ~/Library/LaunchAgents/lutron_bridge_launcher.plist`

## Contributing
Pull requests are always welcome


## License
[MIT](https://choosealicense.com/licenses/mit/)