version = "0.0.0" # DO NOT TOUCH
logLevel = "DEBUG" # can be DEBUG, LOG, WARN, ERROR, CRITICAL
botType = "afkBot" # DO NOT TOUCH

botInfo = { # will be forwarded into mineflayer.createBot, except for "useEnvironmentVar"
    'host': 'mc.hypixel.net', 
    'port': 25565, 
    'username': "MapleAFK", 
    'hideErrors': False, 
    "useEnvironmentVar": True, # if True, instead of putting the password in plaintext, you can specify an Environment Variable. If False, just put the password in plaintext.
    "version": "1.8.8",
    "auth": "offline",
    "password": "MAPLEBOTPASSWORD"
}
