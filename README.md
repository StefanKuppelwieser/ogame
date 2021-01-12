# pyogame
<img src="https://github.com/alaingilbert/pyogame/blob/develop/logo.png?raw=true" width="300" alt="logo">

OGame is a browser-based, money-management and space-war themed massively multiplayer online browser game with over 
two million accounts.

This application is based on the lib from https://github.com/alaingilbert/pyogame.
With this application you can loot in the inactive player, automatically send expeditions and send messages to attackers. The application is gradually expanded over time. It's learning project for me.

## Run
The application runs with python in the version 3.7. At first install all missing pip packages. After that you have to create the config file. The config file is placed in the root folder and ist named ```config.cfg```. The content of the file is:

```
[Login]
Uni = NAME_OF_UNI
Username = NAME_OF_USER
Password = PASSWORT_OF_USER

[Telegram]
Token = TELEGRAM_TOKEN
Chat = CHAT_ID
```
Now are all preconditions finished. You can start the application with one line

```python3 application\__init__.py```

## Properties
You can edit the properties in the file ```appliction\properties.py```. The properties should be self-explanatory.


## Built With

* [PyCharm](https://www.jetbrains.com/de-de/pycharm/) - PyCharm: the python IDE


## Authors

* **Stefan Kuppelwieser** - [Github](https://github.com/StefanKuppelwieser) - [Website](https://wwww.kuppelwieser.net)

See also the list of [contributors](https://github.com/StefanKuppelwieser/ogame/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
