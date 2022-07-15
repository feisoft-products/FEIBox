"""The next generation FEIOS API.
The old feios_utils.funcs will be deprecated soon in (at most) 0.5.0 and will be deleted in (at most) 0.8.0.
The new API is faster but uses (relatively) more RAM.
"""
# Imports.
from . import msg
import os
import time
import toml
import getpass
import pathlib
import hashlib
os.chdir(os.path.dirname(os.path.realpath(__file__)))
# Constants.
version = (0,7,0)
versuffix = "a2"
__null__ = None
indev_name = "Uranium"

# Functions.
def out(t :str):
    "Printing within line."
    print(t,end="")
    return

def outl(t :str):
    "Printing and start another line."
    print(t)
    return

def run_expr(expr :str):
    "Run an expression using exec()."
    exec(expr)

def clear():
    _cls_cmd = 'cls' if os.name=='nt' else 'clear'
    os.system(_cls_cmd)
    return None

def _out(line :str):
    if len(line) == 3:
        print("",end="")
        return 0
    else:
        if line[3] == " ":
            print(line[4:],end="")
            return 0
        else:
            print(msg.ERR_SPACES)
            return 2

def _outl(line :str):
    if len(line) == 4:
        print("")
        return 0
    else:
        if line[4] == " ":
            print(line[5:])
            return 0
        else:
            print(msg.ERR_SPACES)
            return 2

def shutdown_sys(msg :str,secs=5):
    print(msg)
    print("Your system is going to shutdown!")
    print(f"Shutting down in {secs} seconds.")
    print("Close all applications.")
    time.sleep(secs)
    exit()

def _exit(line :str):
    if len(line) == 4:
        exit()
    else:
        exit(line[4:])

def _help():
    with open(r".\help\init.txt") as f:
        a = f.read()
        print(a)

def _version():
    print(f"FEI OS Version {version[0]}.{version[1]}.{version[2]} {versuffix}")
    print("This program and its library is licensed under GPLv3.0+.")
    print(f"Code name {indev_name}.")

def _login():
    passwd = getpass.getpass("Password: ")
    if _get_passwd_from_file(passwd):
        return True
    else:
        return False
    
def _logout():
    exit()


def _get_file(pof):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    rawpth = os.path.dirname(os.path.realpath(__file__))
    tmp = pathlib.Path(rawpth)
    tmp2 = tmp.joinpath(".disk")
    finding = str(tmp2)
    realstr = finding + pof
    return realstr

def get_file(pof):
    pth = _get_file(pof)
    return pth

def _get_ext(pte: str):
    pth = _get_file(pte)
    if pth.endswith(".fsc") or pth.endswith(".ext") or pth.endswith(".py"):
        pass
    else:
        return -1
    fc = open(pth,'r').read()
    exec(fc)
    return 0

def _su():
    print("Enter Password to continue: ")
    passwd = getpass.getpass()
    if _get_passwd_from_file(passwd):
        print("Running in levtitated mode.")
        return
    else:
        print("Uh-oh,you entered the wrong password.")
        shutdown_sys("Computer is shutting down to protect your system.",3)
        return

def _calc(expr :str):
    a = run_expr(expr)
    print(a)
    return

def _cat(cmd :str):
    cmd = cmd.strip()
    if cmd == 'cat':
        print("Usage:  cat [file | --]")
        print("Like `cat` on POSIX systems,this `cat` can either read contents from a file or read from STDIN.")
        print("If you use `--`,that means you force to read from STDIN.")
        print("If no arguments given,print the help and read from STDIN.")
        s = input()
        print(s)
    elif cmd == 'cat --':
        s = input()
        print(s)
    else:
        realpth = _get_file(cmd[4:])
        f = open(realpth,'r')
        content = f.read()
        print(content)

def _get_passwd_from_file(pwd :str):
    pwd = bytes(pwd,encoding='utf-8')
    pth = _get_file(r"/usr/passwd/SHA256.sig")
    hsh = open(pth,'r').read()
    calc = hashlib.sha256()
    calc.update(pwd)
    return calc.hexdigest() == hsh

def _deep_load_ext(extpth,mode):
    if mode == 'python':
        import os
        ret = os.system(f"python {extpth}")
        return ret
    return 3

def load_ext(extpth,mode):
    """Load extensions."""
    ret = _deep_load_ext(extpth,mode)
    return ret

def runbatch(pof):
    """Read a batch script and execute it."""
    try:
        f = open(pof,'r')
    except FileNotFoundError:
        print(msg.ERR_NO_FILE)
        return 2
    except UnicodeDecodeError as e:
        print(msg.ERR_ENCODING(e))
    except OSError:
        print(msg.FATAL_OS)
        return 255
    except Exception:
        print(msg.FATAL_UNKNOWN)
        return 255
    content = f.readlines()
    ret = run(content)
    return ret


def run(l :list[str]):
    "Run a list of str."
    for line in l:
        if line.startswith('#'):
            continue
        elif line.startswith("run"):
            _a = runbatch(line[4:])
            continue
        elif line.startswith("cat"):
            _cat(line)
        elif line.startswith("outl"):
            _a = _outl(line)
            continue
        elif line.startswith('calc'):
            _calc(line[5:])
        elif line.startswith("out"):
            _a = _out(line)
            continue
        elif line.startswith("exit"):
            _exit()
        else:
            print(msg.ERR_NO_COMMAND)
    return

def load_cmd(cmd :str):
    """Load only one cmd."""
    try:
        if cmd.startswith("#"):
            return
        elif cmd.startswith("run"):
            _a = runbatch(cmd[4:])
            return
        elif cmd.startswith("cat"):
            _cat(cmd)
        elif cmd.startswith("outl"):
            _a = _outl(cmd)
            return
        elif cmd.startswith("calc"):
            _calc(cmd[5:])
        elif cmd.startswith("out"):
            _a = _out(cmd)
            return
        elif cmd == 'su':
            _su()
        elif cmd == 'ver' or cmd == 'version':
            _version()
        elif cmd.startswith("exit"):
            _exit(cmd)
        elif cmd.startswith("logout"):
            _logout()
        elif cmd.startswith("help"):
            _help()
        else:
            print(msg.ERR_NO_COMMAND)
        return
    except (KeyboardInterrupt,EOFError):
        print("Oops,your interrupt is not graceful!")
        print("To exit,simply `exit`.")
        print("Or end it in taskmgr (NT) or kill it (POSIX).")
        return