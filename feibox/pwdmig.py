"""Password Changer."""
# Import
import feibox_utils.stdapi as stdapi
print("Welcome to pwdmig.")
print("Type c to start, v to verify and x to exit.")
a = input(">>>> ")
if a in ['c', 'v', 'x']:
    if a == 'c':
        q = stdapi._change_passwd(input("Old password:"), input("New password:"))
        if q == 0:pass
        elif q == 1:print("Old password wrong.")
        elif q == 2:print("Warning: password weak.")
        else:print("Internal error.")
        input("Press any key to finish.")
        exit()
    elif a == 'v':
        if stdapi._get_passwd_from_file(input("Password:")): print("ok")
        else: print("Wrong")
        input("Press any key to finish.")
        exit()
    else:
        exit()
else: exit()