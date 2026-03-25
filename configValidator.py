import sys
import os
import logging
from dotenv import load_dotenv

load_dotenv()

conf = """
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

postLogin = {
    "useCommandToJoinMainServer": True,
    "rejoinOnException": True,
    "joinMainServerCommand": "/server main"
}

"""

def validate():
    try:
        import config
    except ImportError as e:
        logging.critical("Ran into error while loading config.")
        logging.critical(f"    Exception info: {e}")
        if input("Create config file? (y/n): ") == "y":
            with open("config.py", "w") as f:
                f.write(conf)
        else:
            logging.critical("CRITICAL: User did not create config file or entered invalid response to prompt.")
            sys.exit(1)

    try:
        if not config.logLevel in ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]:
            raise Exception
        testConf = config.botInfo["host"] + "" # check if botInfo is str
        testConf = config.botInfo["port"] + 1
        testConf = config.botInfo["username"] + ""
        if not type(config.botInfo["hideErrors"]) == bool:
            raise Exception
        if not type(config.botInfo["useEnvironmentVar"]) == bool:
            raise Exception
        testConf = config.botInfo["password"] + ""
    except Exception:
        logging.critical("Invalid config found.")
        logging.critical(f"Line: {sys.exc_info()[2].tb_lineno}")
        if input("Create config file? (y/n): ") == "y":
            with open("config.py", "w") as f:
                f.write(conf)
            logging.critical("Please configure and run the program again.")
            sys.exit(0)
        else:
            logging.critical("User did not create config file or entered invalid response to prompt.")
            sys.exit(1)
    
    try:
        if os.environ["ENV"] == "development":
            config.botInfo["host"] = os.environ["AFKBOT_HOST"]
            config.botInfo["port"] = os.environ["AFKBOT_PORT"]
    except Exception:
        pass
    
    return config
