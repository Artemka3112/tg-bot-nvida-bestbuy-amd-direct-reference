# Telegram stock bot
Hi everybody. After a lot of time, I want to post the source code of this bot. As usual :)

So, this bot is a parser of the availability of video cards on sale from the BestBuy and Amd website. At first I thought to make something commercial out of it and now it's here.

In addition to the classic parsing, the bot can:
- accept commands from the console
- to launch a t-bot that will notify people added to a special list (it was done for the sale of subscriptions) and executes requests to check the availability of video cards at the command
- of the Linux version of the bot has its own server for clients who can connect and monitor the availability of goods in real time real time

### The bot has two versions:
- **linux**
- **windows**

the latest updates came to the Linux version, since the parser was originally written for Windows, and then moved to linux (ubuntu 20.04).

### The difference is that the Linux version has
- **improved verification for amd site**
- **availability of a server for clients(client has in client branch)**
- **changed the browser to chrome (windows version works with Mozilla browser). As far as I remember.
The main file for running the parser is pars.py .**

The settings should more or less be described on the Linux version of the bot.

If you have any questions, you can write in my telegram chat: https://t.me/temkas_chat

https://t.me/temkasik - telegram channel of my blog(that was remade from channel of this bot) ~~I hope I'll write something in it at least... Ha ha~~