# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
#import uos, machine
#import time
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

# Always connect to wifi
import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("CRCiberneticaVisitas", "C1rcu1t0s")