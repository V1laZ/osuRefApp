import socket

SERVER = "irc.ppy.sh"
PORT = 6667
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

nick = ""
lobby = ""

win_cond = 0
num_slots = 0
mode = 0