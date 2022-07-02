import time
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions, executor
import settings, amd, bestbuy, restarter, userdata

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')
bot = Bot(token=settings.token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply("Hi!\nI'm stock bot!\nTo get more information, write /info.\nPowered by aiogram\nv0.0.1")

@dp.message_handler(commands=['drop'])
async def send_welcome(message: types.Message):
    await message.reply("There is no exact information when there will be a drop. But most often it takes place on Thursday at 12:00 pm.")
    
@dp.message_handler(commands=['info'])
async def send_welcome(message: types.Message):
    await message.reply("✅ This bot checks for drops of sites with reference GPUs. We check the sites where drops occur most often.\n\
\n\
✅ The bot also has its own subscription. If you pay for a subscription, then with each drop, the bot will send you messages about the availability of goods from the general list (list of goods /urls) approximately every 5 seconds. The subscription costs 1$ and is purchased for 30 days.\n\
\n\
❗️Purchases are made through the DonationAlerts website. To purchase, you need to send a donation in USD and attach your id in the comments. You can get the id from the @userinfobot bot. It is quite easy to write /start. The accrual is done manually. Therefore, it may take some time. The amount received from the donation is converted as 1$ = 30 days.\n\
\n\
⚠️ The amount sent without an id is considered a donation to the project. If you forgot to indicate the id, then just write to me in private messages and attach proof that it was you who made the payment.\n\
\n\
❗️You can check for a subscription with the /follow command.\n\
\n\
⚡️Link to pay for the subscription: https://www.donationalerts.com/r/artemka3112")# Such as: Amd Direct, BestBuy.

@dp.message_handler(commands=['check'])
async def start_checking(message: types.Message):
	msg = ""
	for item in amd.threads:
	    if (item.found):
	    	msg+=(f"\n[amd] {item.order_name} - ready for adding to cart")
	    else:
	    	msg+=(f"\n[amd] {item.order_name} - out")
	for item in bestbuy.threads:
	    if (item.found):
	    	msg+=(f"\n[bb] {item.order_name} - ready for adding to cart")
	    else:
	    	msg+=(f"\n[bb] {item.order_name} - out")
	if not(msg == ""):
		await message.reply(msg)
	else:
		await message.reply("Empty")

testvalue = 1337
testing = False
@dp.message_handler(commands=['test'])
async def test_broadcast(message: types.Message):
	global testing
	testing = True
	await message.reply("Tested!")

@dp.message_handler(commands=['follow'])
async def test_broadcast(message: types.Message):
	msg = ""
	for user in userdata.users:
		if (user.id == message.from_user.id):
			if user.ordertime  - time.time() <= 0:
				msg+=f"Your subscription has expired: {time.ctime(user.ordertime)}"
			elif user.ordertime  - time.time() > 0:
				msg+=f"Your subscription is about to expire: {time.ctime(user.ordertime)}"


	if not(msg == ""):
		await message.reply(msg)
	else:
		await message.reply("You don't have a subscription")


@dp.message_handler(commands=['status'])
async def test_broadcast(message: types.Message):
	msg = ""
	msg+=(f"\nAmd checking enable - {settings.amdenable}")
	msg+=(f"\nBestbuy checking enable - {settings.bbenable}")
	msg+=(f"\nBroadcasting enable - {settings.broadcasting}")
	msg+=(f"\nRestart enable - {settings.restarting}")
	msg+=(f"\nRestart cooldown - {settings.restartcooldown}(seconds)")
	msg+=(f"\nLast restart - {time.ctime(restarter.timestart)}")
	if not(msg == ""):
		await message.reply(msg)
	else:
		await message.reply("Empty")

@dp.message_handler(commands=['urls'])
async def test_broadcast(message: types.Message):
	msg = ""
	for name, order in settings.amd.items():
		msg+=(f"\n[amd] {name} - {order}")
	for name, order in settings.bestbuy.items():
		msg+=(f"\n[bb] {name} - {order}")
	if not(msg == ""):
		await message.reply(msg)
	else:
		await message.reply("Empty")

@dp.message_handler(commands=['history'])
async def test_broadcast(message: types.Message):
	msg = ""
	try:
		my_file = open("history.txt", 'r')
		my_string = my_file.read().split("\n")
		if len(my_string) >= 6:  
			for x in range(1,6):
				msg+=f"\n{my_string[len(my_string)-x]}"
		elif len(my_string) > 1 and len(my_string) <= 5:
			for x in range(1,len(my_string)):
				msg+=f"\n{my_string[x]}"
		my_file.close()
	except Exception as e:
		pass
	if not(msg == ""):
		await message.reply(msg)
	else:
		await message.reply("Empty")



async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:


    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
	
	
	count = 0
	try:
		if settings.broadcasting:
			for user in userdata.users:
				if user.ordertime  - time.time() <= 0:
					continue
				for item in amd.threads:
					end = time.time()
					if (item.found) and (end - user.timer > settings.msgtimeout):
						if await send_message(user.id, f"\n[amd] {item.order_name} - IN STOCK BRO!!!!"):
							#print(end - timer[i])
							count+=1
							user.timer = end
						await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
				for item in bestbuy.threads:
					end = time.time()
					if (item.found) and (end - user.timerbb > settings.msgtimeout):
						if await send_message(user.id, f"\n[bb] {item.order_name} - IN STOCK BRO!!!!"):
							#print(end - timer[i])
							count+=1
							user.timerbb = end
						await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
	finally:
		global testing
		if testing:
			log.info(f"{count} messages successful sent.")
			testing = False
		else:
			pass

	return count
async def pedant():
    await broadcaster()


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(1, repeat, coro, loop)

