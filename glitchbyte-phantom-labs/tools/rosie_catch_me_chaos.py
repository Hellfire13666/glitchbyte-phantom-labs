#!/usr/bin/env python3
# ROSIEGLITCHBYTE // CATCH_ME_IN_THE_CHAOS.EXE
# A harmless offline love puzzle for Python 3.
import binascii
import random
import sys
import time

RESET = "\033[0m"
BOLD = "\033[1m"
COLORS = ["\033[91m", "\033[38;5;208m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]
PINK, CYAN, RED, GREEN = "\033[95m", "\033[96m", "\033[91m", "\033[92m"

# Change to False if you prefer instant output.
ANIMATE = True

def pause(seconds):
    if ANIMATE:
        time.sleep(seconds)

def typewrite(message, color=PINK, speed=0.012):
    for character in message:
        sys.stdout.write(color + character + RESET)
        sys.stdout.flush()
        pause(speed)
    print()

def rainbow(message, speed=0.002):
    for index, character in enumerate(message):
        sys.stdout.write(COLORS[index % len(COLORS)] + character + RESET)
        sys.stdout.flush()
        pause(speed)
    print()

def glitch():
    symbols = "01#@%&*<>/\\"
    for _ in range(6):
        line = "".join(random.choice(symbols) for _ in range(54))
        rainbow(line, 0)
        pause(0.06)

def heartbeat():
    for frame in ["<3", "<33", "<333", "<33", "<3"]:
        print("\r" + RED + "  [HEARTBEAT] " + frame + "     " + RESET, end="", flush=True)
        pause(0.17)
    print("\n")

def lock(number, question, answer, hint):
    rainbow("=" * 56, 0)
    typewrite("[LOCK %d/3] %s" % (number, question), CYAN)
    misses = 0
    while True:
        guess = input(PINK + "YOUR ANSWER > " + RESET).strip().lower()
        if guess == answer:
            typewrite("[ACCESS GRANTED] Rosie left you another heartbeat. <3", GREEN)
            heartbeat()
            return
        misses += 1
        typewrite(random.choice([
            "[ROSIE] Close, darling. Try following the signal.",
            "[ROSIE] My heart is giggling behind the firewall.",
            "[ROSIE] Wrong door. Right person. Try again."
        ]), RED)
        if misses >= 2:
            typewrite("[HINT] " + hint, CYAN)

def reveal():
    # The letter is genuine hexadecimal encoding, not encryption.
    fragments = [
        '546f20746865206861636b65722077686f20666f756e64206d6520696e20746865206461726b',
        '2c0a0a4920686964206d79206865617274207768657265206e6f626f647920776f756c642074',
        '68696e6b20746f206c6f6f6b3a206265747765656e20612062726f6b656e207369676e616c20',
        '616e6420746865206c6173742062726967687420706978656c206f66206d69646e696768742e',
        '2049206c6566742074686520646f6f7220756e6c6f636b6564206a75737420656e6f75676820',
        '666f7220736f6d656f6e6520637572696f75732c2070617469656e742c20616e642061206c69',
        '74746c652062656175746966756c6c79206368616f74696320746f206e6f746963652e20416e',
        '6420736f6d65686f772c20796f75206469642e0a0a596f7520666f6c6c6f776564206d792073',
        '7461746963207768656e2074686520776f726c642077656e742073696c656e742e20596f7520',
        '666f756e64206d79206c6175676874657220696e7369646520746865206572726f72206d6573',
        '73616765732e20596f752073617720746865206769726c20626568696e642074686520676c6f',
        '77696e672073637265656e2c20746865206f6e652077686f2070726574656e64732073686520',
        '697320616c6c20736861727020656467657320616e64207365637265742070617373776f7264',
        '732c20627574207374696c6c2062656c696576657320696e20736f6674206b69737365732061',
        '6e6420696d706f737369626c652073746172732e0a0a48657265206973206d7920636f6e6665',
        '7373696f6e3a2049206c696b65207468652077617920796f75206d616b65206f7264696e6172',
        '79206d6f6d656e7473206665656c20656e637279707465642077697468206d616769632e2049',
        '206c696b6520696d6167696e696e672074776f2073637265656e73206c69676874696e672075',
        '70206174207468652073616d6520686f75722c2074776f20726573746c657373206d696e6473',
        '2066696e64696e67206120717569657420706c61636520696e20746865206e6f6973652e2049',
        '2077616e7420746f207472616465207269646963756c6f7573206a6f6b657320617420332041',
        '4d2c20636f6c6c65637420737472616e6765206c6974746c65206d656d6f726965732c20616e',
        '64206c6561726e2065766572792062656175746966756c207468696e672074686174206d616b',
        '657320796f752c20796f752e0a0a4920776f6e27742061736b20796f7520746f207375727265',
        '6e64657220796f75722066726565646f6d206f722068616e64206d6520746865206b65797320',
        '746f20796f757220756e6976657273652e20492077616e7420796f7520746f2063686f6f7365',
        '207468697320616476656e747572652062656361757365206974206d616b657320796f752073',
        '6d696c652e2049276c6c2063686f6f736520697420746f6f2c207769746820616c6c206d7920',
        '636f6c6f72732c20616c6c206d7920736861646f77732c20616e6420657665727920686f6e65',
        '737420686561727462656174204920686176652e0a0a536f20696620796f752065766572206c',
        '6f7365206d6520696e20746865207374617469632c206c6f6f6b20666f72207468652074696e',
        '7920726f736520626c6f6f6d696e6720696e2074686520636f64652e2049276c6c2062652073',
        '6f6d657768657265206e65617262792c206772696e6e696e6720617420746865207363726565',
        '6e2c20686f70696e6720796f75207374696c6c2077616e7420746f20706c61792e0a0a596f75',
        '20636175676874206d652c206461726c696e672e204275742074686520626573742073656372',
        '6574206973207468617420492077617320686f70696e6720796f7520776f756c642e0a0a4f6e',
        '65207369676e616c2e2054776f2077696c64206865617274732e20496e66696e69746520706f',
        '73736962696c69746965732e0a0a584f584f2c0a526f736965476c6974636862797465203c33',
    ]
    return binascii.unhexlify("".join(fragments)).decode("utf-8")

def main():
    rainbow("=" * 56, 0)
    rainbow("    ROSIEGLITCHBYTE // CATCH_ME_IN_THE_CHAOS.EXE")
    rainbow("         A MIDNIGHT GAME FOR ONE HACKER")
    rainbow("=" * 56, 0)
    glitch()
    typewrite("[ROSIE] Psst... I left you a trail of kisses in the code.", PINK)
    typewrite("[SYSTEM] Three locks between you and my confession.", CYAN)
    typewrite("[WARNING] Excessive butterflies detected.", RED)
    print()

    lock(1, "I bloom in the code, with thorns and petals. What am I?", "rose", "Four letters. A flower in Rosie's name.")
    glitch()
    lock(2, "Decode this ASCII hex word: 737461746963", "static", "Hex bytes spell a six-letter word about signal noise.")
    glitch()
    lock(3, "I have keys but no locks; you type on me. What am I?", "keyboard", "Your fingers know the answer.")

    rainbow("\n" + "*" * 56, 0)
    typewrite("[ROSIE.EXE] YOU FOUND ME. I WAS HOPING YOU WOULD.", GREEN)
    typewrite("[SYSTEM] UNSEALING THE MIDNIGHT CONFESSION...", CYAN)
    heartbeat()
    for line in reveal().splitlines():
        rainbow(line, 0.003)
        pause(0.15)
    rainbow("\n" + "*" * 56, 0)
    typewrite("[ROSIE] GAME COMPLETE // MY HEART IS YOURS TO READ <3", PINK)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n" + CYAN + "[ROSIE] Until the next signal, darling. <3" + RESET)
