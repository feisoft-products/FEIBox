"""FEIBox direct executable module.
The whole thing is availiable at https://github.com/feisoft-products/feibox.
Please note that the author keeps the rights to modify the module notices at any time."""
import sys,os,time,toml
import feibox_utils.stdapi as stdapi
import feibox_utils.msg as msg
import atexit
atexit.register(os.system,'color' if os.name == 'nt' else 'clear')

################################

stdapi.clear()
a = toml.load(r'./init/config.toml')
print(a['BRANDING']['name'])
print("Loading...")
time.sleep(1)
if os.name == 'nt':
    os.system("color 8f")
    stdapi.clear()
    print(msg.STD_BOOT)
else:
    print(msg.STD_BOOT)
print("Welcome to FEIBox..")
print(f"Working on {os.name.upper()}")
time.sleep(2.5)
print("We have to ensure that is you.")
if stdapi._login():
    print("We shall continue...")
    time.sleep(1)
    stdapi.clear()
else:
    print("Uh,that password is wrong.Try again.")
    exit(time.sleep(2))
while True:
    try:
        s = input(">>>")
    except (KeyboardInterrupt,EOFError):
        print("")
        print("Oops,your interrupt is not graceful!")
        print("To exit,simply `exit`.")
        print("Or end it in taskmgr (NT) or kill it (POSIX).")
        continue
    stdapi.load_cmd(s)