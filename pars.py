from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading, time
import sys ,signal
import amd, bc, commands, settings, tg, bestbuy, restarter, userdata
from userdata import User
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions, executor


def signal_handling(signum,frame):
	settings.inputcommands = False
	amd.stopAmd()
	bestbuy.stopBestbuy()
	bc.stopBroadcaster()
	restarter.stopRestarter()
	userdata.writeUsers()
	sys.exit()

commands.startCommands()
bc.startBroadcaster()
restarter.startRestarter()
userdata.loadUsers()
signal.signal(signal.SIGINT,signal_handling)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.call_later(1,tg.repeat,tg.pedant,loop)
	#dp.loop.create_task(broadcaster())
	executor.start_polling(tg.dp, skip_updates=True, loop=loop)
