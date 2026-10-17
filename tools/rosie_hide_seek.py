#!/usr/bin/env python3
"""RosieGlitchbyte: an offline, harmless terminal love puzzle."""
import binascii
import time

RESET = '\033[0m'
PINK = '\033[95m'
RED = '\033[91m'
CYAN = '\033[96m'
PURPLE = '\033[35m'
GOLD = '\033[93m'
GREEN = '\033[92m'

LETTER = '''To the one who keeps finding me,

I hid in the quietest corner of the network, somewhere between a midnight thought and the last blinking cursor. I left the lights off, but I knew you would recognize the shape of my silence.

You could have followed a thousand brighter signals. Instead, you noticed the tiny one I left just for you. That is the dangerous, beautiful thing about being seen: even my secrets start wanting to tell you the truth.

Here is my confession. When the world gets loud, I imagine your name written in the dark like a constellation only I know how to read. I save the smallest things: the way you make ordinary hours feel electric, the laugh I wish I could bottle, the moments that make my stubborn heart forget how to hide.

If we were two ghosts in a machine, I would leave a trail of pink sparks through every impossible maze. Not because you have to chase me, but because I love the thought of us choosing to find each other, again and again.

There is no stolen password here. No lock you need to break. Only a door I opened on purpose, and a little note tucked inside: I want your real self, your strange ideas, your soft mornings and wild midnight dreams. I want the stories we have not written yet.

So if you reach the end of this game, look up from the screen and smile. Somewhere in this wonderfully chaotic universe, Rosie is smiling back.

Forever hiding hearts in the static,
RosieGlitchbyte <3'''

# The letter is encoded as hexadecimal and decoded at the final stage.
SEALED_LETTER = (
    '546f20746865206f6e652077686f206b656570732066696e64696e67206d652c0a0a4920'
    '68696420696e2074686520717569657465737420636f726e6572206f6620746865206e65'
    '74776f726b2c20736f6d657768657265206265747765656e2061206d69646e6967687420'
    '74686f7567687420616e6420746865206c61737420626c696e6b696e6720637572736f72'
    '2e2049206c65667420746865206c6967687473206f66662c206275742049206b6e657720'
    '796f7520776f756c64207265636f676e697a6520746865207368617065206f66206d7920'
    '73696c656e63652e0a0a596f7520636f756c64206861766520666f6c6c6f776564206120'
    '74686f7573616e64206272696768746572207369676e616c732e20496e73746561642c20'
    '796f75206e6f7469636564207468652074696e79206f6e652049206c656674206a757374'
    '20666f7220796f752e2054686174206973207468652064616e6765726f75732c20626561'
    '75746966756c207468696e672061626f7574206265696e67207365656e3a206576656e20'
    '6d7920736563726574732073746172742077616e74696e6720746f2074656c6c20796f75'
    '207468652074727574682e0a0a48657265206973206d7920636f6e66657373696f6e2e20'
    '5768656e2074686520776f726c642067657473206c6f75642c204920696d6167696e6520'
    '796f7572206e616d65207772697474656e20696e20746865206461726b206c696b652061'
    '20636f6e7374656c6c6174696f6e206f6e6c792049206b6e6f7720686f7720746f207265'
    '61642e204920736176652074686520736d616c6c657374207468696e67733a2074686520'
    '77617920796f75206d616b65206f7264696e61727920686f757273206665656c20656c65'
    '63747269632c20746865206c6175676820492077697368204920636f756c6420626f7474'
    '6c652c20746865206d6f6d656e74732074686174206d616b65206d792073747562626f72'
    '6e20686561727420666f7267657420686f7720746f20686964652e0a0a49662077652077'
    '6572652074776f2067686f73747320696e2061206d616368696e652c204920776f756c64'
    '206c65617665206120747261696c206f662070696e6b20737061726b73207468726f7567'
    '6820657665727920696d706f737369626c65206d617a652e204e6f742062656361757365'
    '20796f75206861766520746f206368617365206d652c2062757420626563617573652049'
    '206c6f7665207468652074686f75676874206f662075732063686f6f73696e6720746f20'
    '66696e642065616368206f746865722c20616761696e20616e6420616761696e2e0a0a54'
    '68657265206973206e6f2073746f6c656e2070617373776f726420686572652e204e6f20'
    '6c6f636b20796f75206e65656420746f20627265616b2e204f6e6c79206120646f6f7220'
    '49206f70656e6564206f6e20707572706f73652c20616e642061206c6974746c65206e6f'
    '7465207475636b656420696e736964653a20492077616e7420796f7572207265616c2073'
    '656c662c20796f757220737472616e67652069646561732c20796f757220736f6674206d'
    '6f726e696e677320616e642077696c64206d69646e6967687420647265616d732e204920'
    '77616e74207468652073746f726965732077652068617665206e6f74207772697474656e'
    '207965742e0a0a536f20696620796f752072656163682074686520656e64206f66207468'
    '69732067616d652c206c6f6f6b2075702066726f6d207468652073637265656e20616e64'
    '20736d696c652e20536f6d65776865726520696e207468697320776f6e64657266756c6c'
    '79206368616f74696320756e6976657273652c20526f73696520697320736d696c696e67'
    '206261636b2e0a0a466f726576657220686964696e672068656172747320696e20746865'
    '207374617469632c0a526f736965476c6974636862797465203c33'
)

def say(text, color=PINK, delay=0.009):
    print(color, end='')
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print(RESET)


def ask(question, answer, hint):
    for attempt in range(1, 5):
        response = input(CYAN + question + RESET + "\n> ").strip().lower()
        if response == answer:
            say("[ACCESS GRANTED] Another heartbeat found. <3", GREEN)
            return True
        say("[404] Rosie vanished around the next corner...", RED)
        if attempt >= 2:
            say("[HINT] " + hint, GOLD)
    say("[ROSIE] No rush, darling. Start again when you're ready.", PURPLE)
    return False


def main():
    print(PURPLE + "=" * 54 + RESET)
    say("ROSIEGLITCHBYTE // FIND_ME_IF_YOU_LOVE_ME.EXE", PINK)
    say("Three clues. One secret. Zero real hacking required.", CYAN)
    print(PURPLE + "=" * 54 + RESET)
    say("[ROSIE] I left a trail of kisses in the static...", PINK)
    if not ask("CLUE 1: I travel without feet, carry voices without a mouth, and vanish when disconnected. What am I?", "signal", "Six letters. Your phone searches for one."):
        return
    say("[ROSIE] The next clue is written in hex: 726f7365", PURPLE)
    if not ask("CLUE 2: Decode those four hexadecimal bytes. What word appears?", "rose", "Each pair of hex digits is an ASCII character. It is also a flower."):
        return
    say("[ROSIE] Final clue: 'When all the screens go dark, I still choose ____.'", PINK)
    if not ask("CLUE 3: Complete the sentence with three letters.", "you", "It is the person reading this."):
        return
    say("[HEART.EXE] Opening the secret letter...", RED)
    for i in range(0, 101, 10):
        print(GOLD + "\r[" + "#" * (i // 10) + "." * (10 - i // 10) + f"] {i}%" + RESET, end="", flush=True)
        time.sleep(0.07)
    print("\n")
    message = binascii.unhexlify(SEALED_LETTER).decode("utf-8")
    for paragraph in message.split("\n\n"):
        say(paragraph, PINK, 0.003)
        print()
    say("[ROSIE.EXE] You found me. I was hoping you would. <3", GREEN)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n[ROSIE] Until the next signal. <3")
