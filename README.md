# osuRefApp
Android app for osu! referees.

## Table of Contents
- [osuRefApp](#osurefapp)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Build and run](#build-and-run)
  - [Install on Android](#install-on-android)
- [Usage](#usage)
  - [Login](#login)
  - [Main menu](#main-menu)
    - [Join Lobby popup](#join-lobby-popup)
    - [Create Lobby popup](#create-lobby-popup)
  - [Mappools](#mappools)
    - [Remove Mappool popup](#remove-mappool-popup)
  - [Create Mappool](#create-mappool)
  - [Select Mappool](#select-mappool)
  - [Lobby](#lobby)

## Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [pipenv](https://pypi.org/project/pipenv/)

## Build and run
Open project folder in VS Code and type in terminal
```
pipenv shell
```
then to install project dependencies
```
pipenv install
```
open VS Code command pallete <kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>P</kbd> and type
```
Python: Select Interpreter
```
select interpreter corresponding to project name which should be something like *osuRefApp-O3zasd51*  
  
run the app with <kbd>F5</kbd>  

## Install on Android
Download apk from [releases](https://github.com/V1laZ/osuRefApp/releases/tag/v1.0) 

# Usage
## Login
![](https://imgur.com/eB7hmBm.png)
 - **Username** - your osu! username. Replace spaces with underscores (e.g., `beppy master 1000` becomes `beppy_master_1000`)
- **Password** - the password from [IRC Authentication](https://osu.ppy.sh/p/irc) page
- **Remember me** - locally stores your credentials for future starts
- **Login** - login to Bancho IRC with given credentials

## Main menu
![](https://imgur.com/syM0HPs.png)
- **Join Lobby** - opens [Join Lobby popup](#join-lobby-popup)
- **Create Lobby** - opens [Create Lobby popup](#create-lobby-popup)
- **Mappools** - switches to [Mappools](#mappools) screen

### Join Lobby popup
![](https://imgur.com/qcD3z0w.png)
- **Lobby ID** - numbers that can be found in URL of the match  
![](https://imgur.com/i7Ay5qR.png)
- **JOIN** - joins the lobby and switches to [Select Mappool](#select-mappool) screen

### Create Lobby popup
![](https://imgur.com/PUExenc.png)  
Used for creating tournament matches.  
Don't forget to close the lobby with `!mp close` after it is done!

## Mappools
![](https://imgur.com/PCnpg0p.png)
- **Table with mapools** - click on mappool name to view the mappool
- **Create Mappool** - switches to [Create Mappool](#create-mappool) screen
- **Remove Mappool** - opens [Remove Mappool popup](#remove-mappool-popup)

### Remove Mappool popup
![](https://imgur.com/rYr3pJ5.png)
- **Name** - name of the mappool you want to be removed
- **Remove** - removes given mappool from the mappool table

## Create Mappool
![](https://imgur.com/H8Othuy.png)
- **Type** - map type in mappool (e.g., NM1, HR2)
- **MapID/link** - link for the map or map ID
- **Add row** - adds map to the mappool table with given values
- Click **Save button** on bottom right to save the mappool

## Select Mappool
![](https://imgur.com/XksjZck.png)
- Select mappool which you want to use in the lobby
- Click **None** if you don't want to use mappool or you don't have any

## Lobby
![](https://imgur.com/PelhKA5.png)
- Click **Refresh** button on top right to send `!mp settings` command and update values on the screen
- Click **Abort** button on bottom left to send `!mp abort` command
- Click **Start** button on bottom right to send `!mp start 10` comamnd
- **SELECT MAP** 
    - opens popup of the previously selected mappool
    - click on map to send `!mp map` command with the selected map
- Above **SELECT MAP** is text input for sending messages to lobby

