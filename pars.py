from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading, time
import sys ,signal
import amd, bc, commands, settings, tg, bestbuy, restarter, userdata, server
from userdata import User
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions, executor


def signal_handling(signum,frame):
	settings.inputcommands = False
	amd.stopAmd()
	bestbuy.stopBestbuy()
	server.stopServer()
	bc.stopBroadcaster()
	restarter.stopRestarter()
	userdata.writeUsers()
	sys.exit(0)

commands.startCommands()
bc.startBroadcaster()
restarter.startRestarter()
userdata.loadUsers()
server.startServer()
signal.signal(signal.SIGINT,signal_handling)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.call_later(1,tg.repeat,tg.pedant,loop)
	#dp.loop.create_task(broadcaster())
	executor.start_polling(tg.dp, skip_updates=True, loop=loop)
