
#Amd direct
amdenable = True
amd = {
"6900 XT":"https://www.amd.com/en/direct-buy/5458372200/us",
"6800 XT":"https://www.amd.com/en/direct-buy/5458372800/us",
"6800":"https://www.amd.com/en/direct-buy/5458373400/us",
"6700 XT":"https://www.amd.com/en/direct-buy/5498471500/us"}# url of order by proxy
timeoutrefresh = 3#timeout refresh page
amdtimeout = 4#time that need wait script after click button "add to cart"
close = True# wait to pay in browser
loggerout = True # if need logs
loggingexceptions = False#idk
amdsimplemode = True #test adding to cart

# BestBuy
bbenable = True # wait for bestbuy available
bestbuy = {
"3070":"https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p",
"3060ti":"https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p",
"3090":"https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p",
"3080":"https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p"
#"10400":"https://www.bestbuy.com/site/intel-core-i5-10400-10th-generation-6-core-12-thread-2-9-ghz-4-3-ghz-turbo-socket-lga1200-locked-desktop-processor/6411498.p"
}
#"razyn 3700x" : "https://www.bestbuy.com/site/amd-ryzen-7-3700x-3rd-generation-8-core-16-thread-3-6-ghz-4-4-ghz-max-boost-socket-am4-unlocked-desktop-processor/6356277.p"
bbtimeoutrefresh = 0 # analog of amd timeout
bbtimeout = 10 # analog of amd timeout


# rstarter
restarting = True #restarter, make restart threads that searching drops
restartcooldown = 9000#sec

#server
server = True # if need start server for debug founding from client application check client branch
connecttimeout = 5.0
ip = ('127.0.0.1',9090)
listeners = 1 # amout of clients that could be conected

#commands
inputcommands = True # need input commands in console

#tg
token = ""# your telegram bot token
# def get_users():
#     yield from (0,453495818)

#broadcaster
broadcasting = True #broadcasting is system of sending message that videcard found for peoples that bought subscribtion(mb that)
msgtimeout = 180

#proxy for 
proxy = "172.67.182.61"#http
port = 80
# proxys = "159.203.84.241"#https
# ports = 3128
# proxys = "68.183.102.196"#https
# ports = 3128
proxys = "176.113.73.96"#https
ports = 3128