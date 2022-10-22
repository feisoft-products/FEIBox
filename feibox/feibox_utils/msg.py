# Error messages
ERR_SPACES = """Input and/or script error:ERROR 001
There should be a space.
Execution halted.
"""
ERR_NO_COMMAND = """Input and/or script error:ERROR 002
No such command
Execution halted.
"""
ERR_NOT_SPECIFIC_SCRIPT = """Input and/or script error:ERROR 003
Not specific script.
Execution halted.
"""
ERR_NO_FILE = """Input error:ERROR 004
No such file.
Execution halted.
"""
ERR_NOT_ENOUGH_ARGS = """Input and/or script error:ERROR 005
Arguments not enough.
Execution halted.
"""
def ERR_ENCODING(_e,/):
    print(f"""File error:ERROR 006
    Invalid Encoding at {_e}.
    Execution halted.
    """)
ERR_NOT_ENABLED = """Input and/or script error:ERROR 007
The function is not enabled.
Execution halted.
"""
FATAL_OS = """System fatal error:FATAL 001
Host OS Error.
Report this to https://github.com/devoter-fyc/fei-ros.
Execution halted.
"""
FATAL_UNKNOWN = """System fatal error:FATAL 000
Unknown Error.
Report this to https://github.com/devoter-fyc/fei-ros.
Execution halted.
"""
# Standard messages
STD_BOOT = """
          ===========   ===========   ===========  ==============        ========      ==        ==
          ==            ==                 =       ==           ===    ==       ==       ==     ==
          ==            ==                 =       ==             ==   ==        ==        == ==
          ===========   ===========        =       ==============      ==          ==       ===
          ==            ==                 =       ==             ==   ==        ==        == ==
          ==            ==                 =       ==            ==     ==      ==       ==     ==
          ==            ===========   ===========  ==============         ======     =====        ====
"""