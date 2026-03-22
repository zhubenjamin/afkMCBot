# MAPLETHEDOG
from javascript import require, On, Once, AsyncTask, once, off, start, stop, abort
import logging
from datetime import datetime
import sys
import os
import asyncio
from dotenv import load_dotenv

mineflayer = require("mineflayer")
#mineflayerViewer = require("prismarine-viewer")

load_dotenv()

### CONFIG
import configValidator
config = configValidator.validate()
### END CONFIG

logFile = f"logs/{datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')}.log"
logLevel = eval("logging." + config.logLevel)
logging.basicConfig(format=f"%(levelname)s : %(name)s : %(asctime)s : %(process)d : %(thread)d : %(message)s", datefmt="%Y/%m/%d %H:%M:%S", encoding="utf-8", level=logLevel, handlers=[logging.FileHandler(logFile, mode="w"), logging.StreamHandler()]) #filename=f"logs/{datetime.strftime(datetime.now(), '%Y%m%d_%H%M%S')}.log", filemode="a", 
logging.debug("Hello! Logging init.")

if config.botInfo["useEnvironmentVar"]:
    PASSWORD = os.environ[config.botInfo["password"]]
else:
    PASSWORD = config.botInfo["password"]
    
botInfo = { 
    'host': config.botInfo["host"], 
    'port': config.botInfo["port"], 
    'username': config.botInfo["username"], 
    'hideErrors': config.botInfo["hideErrors"], 
    "password": PASSWORD,
    "auth": config.botInfo["auth"],
    "version": config.botInfo["version"]
}

bot = mineflayer.createBot(botInfo)

onListeners = []
asyncTasks = []

def end(code):
    bot.quit()
    for listener in onListeners:
        off(bot, *listener)
    for task in asyncTasks:
        abort(task)
    logging.debug("Goodbye! Logging shutdown.")
    logging.shutdown()
    sys.exit(0)

@AsyncTask(start=True)
def join(task):
    once(bot, "login")
    once(bot, "spawn")
    logging.info("Bot logged on to auth")

    global isLoggedIn
    global isLoginSent
    isLoggedIn = False
    isLoginSent = False
    task.sleep(0.1)
    @On(bot, "message")
    def recv_login_msg(this, msg_json, *args):
        global isLoginSent
        global isLoggedIn
        msg = msg_json.toString()
        logging.debug(f"CHAT : {msg}")
        if isLoginSent:
            if "Successful login!" in msg:
                logging.info("Bot is now logged in")
                isLoggedIn = True
            if isLoggedIn:
                if "Kicked whilst" in msg or "Could not connect" in msg:
                    logging.info(f"Bot was unable to connect to main server with reason '{msg}'")
                    end(1)
        else:
            if "/login" in msg:
                logging.debug("Bot detected login prompt")
                bot.chat(f"/login {PASSWORD}")
                isLoginSent = True
            elif "/register" in msg:
                logging.critical("Bot detected register prompt! Please register first")
                bot.quit()
                logging.shutdown()
                sys.exit(1)
    onListeners.append(("message", recv_login_msg))
    
    while True:
        msgJson = once(bot, "message")
        msg = msgJson.toString()
        if "Successful login!" in msg:
            break
        task.sleep(0.05)
    while True:
        msgJson = once(bot, "message")
        msg = msgJson.toString()
        if "joined the game" in msg:
            break
        task.sleep(0.05)
    once(bot, "spawn")
    logging.info("Bot spawned into main")
    off(bot, "message", recv_login_msg)
    onListeners.remove(("message", recv_login_msg))
    logging.debug("success")
asyncTasks.append(join)

@On(bot, "error")
def botError(this, error):
    logging.error(f"Bot encountered error {error}")
    end(1)
onListeners.append(("error", botError))
    
@On(bot, "kicked")
def botKick(this, reason, *args):
    try:
        logging.error(f"Bot was kicked with reason {reason}")
    except Exception:
        pass
    end(0)
onListeners.append(("kicked", botKick))