"""The next generation FEIBox API.
"""
# Imports.
import sys
import warnings
from . import msg
import re
import os
import time
import toml
import getpass
import pathlib
import hashlib
import argparse
os.chdir(os.path.dirname(os.path.realpath(__file__)))
# Constants.
version = (0,8,1)
versuffix = "build 444 (0.8.1.fprvint.ginger_pre.5chk)"
__null__ = None
__osenv__ = os.name
indev_name = "Ginger"
lev =  False

# Functions.
def out(t :str):
    "Printing within line. TODO: Deprecation: Will be deprecated in 0.8.1."
    warnings.warn("Will be deprecated in 0.8.1", DeprecationWarning)
    print(t,end="")
    return

def outl(t :str):
    "Printing and start another line."
    print(t)
    return

def out_cmd(t :str):
    "TODO: Feature-002: improved `out`."

def set_env(cmdargs):
    "TODO: Feature-003: `set`."
    pass

def run_expr(expr :str):
    "Run an expression using exec()."
    exec(expr)

def clear():
    _cls_cmd = 'cls' if os.name=='nt' else 'clear'
    os.system(_cls_cmd)
    return None

def _get_passwd_from_file(pwd :str):
    pwd = bytes(pwd,encoding='utf-8')
    pth = _get_file(r"/usr/passwd/SHA256.sig")
    hsh = open(pth,'r').read()
    calc = hashlib.sha256()
    calc.update(pwd)
    return calc.hexdigest() == hsh

def _change_passwd(oldpwd :str,newpwd :str):
    a = 0
    if not isinstance(oldpwd,str) and isinstance(newpwd,str): return 3
    if len(newpwd) <= 6: a = 1
    if not _get_passwd_from_file(oldpwd): return 1
    calc = hashlib.sha256()
    newpwd = bytes(newpwd,encoding='utf-8')
    calc.update(newpwd)
    write_to_file(r"/usr/passwd/SHA256.sig",calc.hexdigest())
    if a == 0: return 0
    else: return 2


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

def reboot_sys(msg :str,secs=5):
    print(msg)
    print(f"Your system is going to reboot in {secs} seconds.")
    print("Close all applications.")
    def get_start_command():
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        run = sys.executable + " " + r"..\feibox.py"
        return run
    def restart_on_posix():
        if os.fork(): sys.exit()
        else: time.sleep(secs); os.system(get_start_command())
    def restart_on_nt():
        os.system("start" + " " + get_start_command())
        sys.exit(time.sleep(5))
    if os.name == 'nt': 
        restart_on_nt()
    else:
        restart_on_posix()

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
    print(msg.STD_BOOT)
    print(f"FEIBox Version {version[0]}.{version[1]}.{version[2]} {versuffix}")
    print("This program and its library is licensed under GPLv3.0+.")
    print(f"Code name {indev_name}.")
    print("DO NOT DISTRIBUTE ILLEGALLY.")

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
        lev = True
        print("Running in levtitated mode.")
        return
    else:
        print("Uh-oh,you entered the wrong password.")
        print("Retry? [Y/N]")
        s = input()
        if s in ['y','Y','yes']:_su()
        else: shutdown_sys("Shutting down...",3)
        return

def _unsu():
    lev = False
    print("Switched to normal user.")

def _identify():
    if _get_passwd_from_file(getpass.getpass("Please enter main password: ")):
        return True
    else:
        return False

def _get_input_line(msg=''):
    ret = input(msg)
    return ret

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


def _write_file(pth,content='',mode="str"):
    rpth = _get_file(pth)
    f = open(rpth,'w')
    f.write(content)

def _write_cmd(cmdargs=None):
    """Command Line WriteFile."""
    def _inner_cmd():
        p = argparse.ArgumentParser(prog='writefile',description='Tool to write data to a file.')
        p.add_argument("POF", type=str, help="The path to the destination file.")
        p.add_argument("DATA", help="The data to be written.")
        args = p.parse_args(cmdargs)
        _write_file(args.POF, args.DATA)
        print("Done, errno 0")

def write_to_file(dest,content='',mode='str'):
    """High level interface for file writing."""
    _write_file(dest,content,mode)

def read_from_file(pth,mode='str'):
    """High level interface for file reading."""
    realpth = _get_file(pth)
    f = open(realpth,'r')
    content = f.read()
    return content

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
    """Run a list of str."""
    for line in l:
        if line.startswith('#'):
            continue
        elif line.startswith("run"):
            _a = runbatch(line[4:])
            continue
        elif line.startswith("write"):
            if len(line) <= 6: print(msg.ERR_NOT_ENOUGH_ARGS); return
            else: _write_cmd(line[6:]); return
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
        elif cmd.startswith("shutdown"):
            shutdown_sys(cmd[9:])
        elif cmd.startswith("reboot"):
            reboot_sys(cmd[7:])
        elif cmd.startswith("run"):
            _a = runbatch(cmd[4:])
            return
        elif cmd.startswith("write"):
            if len(cmd) <= 6: print(msg.ERR_NOT_ENOUGH_ARGS); return
            else: _write_cmd(cmd[6:]); return
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
        elif cmd.startswith("unsu"):
            _unsu()
        elif cmd.startswith("identify"):
            if _identify(): print("Continue.")
            else: print("This is wrong.Try again.")
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
        print("Oops, your interrupt is not graceful!")
        print("To exit,simply `exit`.")
        print("Or end it in taskmgr (NT) or kill it (POSIX).")
        return