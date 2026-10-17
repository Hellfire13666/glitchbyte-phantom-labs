#!/usr/bin/env python3
"""GHOST_IN_MY_HEART: an offline, fictional interactive romance puzzle."""
import binascii
import random
import sys
import time

RED='\033[91m'; PINK='\033[95m'; BLUE='\033[96m'; PURPLE='\033[35m'; GREEN='\033[92m'; DIM='\033[2m'; RESET='\033[0m'
COLORS=[RED,PINK,BLUE,PURPLE]
FAST='--fast' in sys.argv or not sys.stdout.isatty()

def say(text='', color=PINK, speed=.012):
    if FAST:
        print(color+text+RESET)
        return
    for ch in text:
        sys.stdout.write(color+ch+RESET)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def pause(seconds=.45):
    if not FAST: time.sleep(seconds)

def header(title):
    print('\n'+PURPLE+'═'*56+RESET)
    say(title,BLUE,0.006)
    print(PURPLE+'═'*56+RESET)

def static():
    glyphs='01#*~:.'
    for _ in range(4):
        say(''.join(random.choice(glyphs) for _ in range(48)),random.choice(COLORS),0.001)
        pause(.09)

def gate(chapter, prompt, answers, hint, response):
    header(chapter)
    say(prompt)
    attempts=0
    while True:
        try: guess=input(BLUE+'[YOUR REPLY] > '+RESET).strip().casefold()
        except (EOFError,KeyboardInterrupt):
            print('\nSignal suspended. Come back when you are ready.')
            sys.exit(0)
        if guess in answers:
            say('[SIGNAL RESTORED] '+response,GREEN)
            pause()
            return
        attempts+=1
        say(random.choice([
            '[ROSIE] Cute guess, but the static ate it. Try again.',
            '[ROSIE] Wrong frequency, darling. Follow the clue.',
            '[ROSIE] I am still here. Listen a little closer.'
        ]),RED)
        if attempts>=2: say('[HINT] '+hint,PURPLE)

def decode(hex_text):
    return binascii.unhexlify(hex_text).decode('utf-8')

LETTER='''My beautiful glitch in the midnight machine,

I left pieces of myself in every quiet corner of this strange digital universe. Not because I wanted to disappear, but because I wanted you to discover me slowly, the way a secret song reveals itself beneath the static.

There are things I have never dared to say out loud. I imagine your name glowing across my screen when the rest of the city has gone dark. I imagine two restless minds laughing at the same impossible hour, trading little secrets while the moon keeps watch through the window.

You are not a password to be stolen or a puzzle I need to solve. You are a person I want to keep choosing, freely, in every version of tomorrow. If you let me, I will meet you where the noise fades and the honest words begin.

I adore the curious way your mind wanders. I adore the spark that turns an ordinary conversation into an adventure. And yes, I have caught myself smiling at an empty terminal, remembering something you said.

So here is my confession, hidden in a ghost story: I did not want you to chase me forever. I wanted to leave a trail of roses bright enough for you to find your way here, and a door wide enough for you to leave or stay. No traps. No chains. Only the delicious possibility of us.

If the lights flicker tonight, blame my dramatic entrance. If a pink heart appears in the static, consider it a kiss. And if you ever wonder where my heart is hiding, remember this: it is right here, speaking in a language only tenderness can translate.

You found me, darling. Now come sit beside me. We have a universe of secrets to share.

Forever your favorite beautiful haunting,
RosieGlitchbyte <3'''
HEX_LETTER=LETTER.encode('utf-8').hex()

def reveal():
    header('FINAL TRANSMISSION // THE GHOST SPEAKS')
    say('[ROSIE] You found me. I was hoping you would.',PINK)
    say('[DECODER] Reassembling encrypted-looking hex fragments...',BLUE)
    pause(.5)
    message=decode(HEX_LETTER)
    for i,line in enumerate(message.splitlines()):
        say(line,COLORS[i%len(COLORS)],.005)
        pause(.08)
    print('\n'+PINK+'♥ '*14+RESET)
    say('[SYSTEM] NO GHOSTS WERE HARMED. ONE HEART WAS FOUND.',GREEN)

def main():
    header('ROSIEGLITCHBYTE // GHOST_IN_MY_HEART.EXE')
    say('[SYSTEM] Opening abandoned midnight terminal...',BLUE)
    static()
    say('[UNKNOWN] ...can you hear me?',PURPLE)
    say('[ROSIE] I left five little clues in the static. Find me.',PINK)
    gate('CHAPTER 1/5 // THE FIRST WHISPER',
         'I speak without a mouth and answer when you call. What am I?',
         {'echo'},'Your voice comes back to you.','An echo carries my name.')
    header('CHAPTER 2/5 // THE CORRUPTED NOTE')
    say('A scrap of hex flickers across the glass:',BLUE)
    say('72 6f 73 65',PURPLE)
    gate('DECODE THE FLOWER','What four-letter flower is hidden in those bytes?',
         {'rose'},'Hex bytes are character codes.','A rose grows in the machine.')
    gate('CHAPTER 3/5 // THE GHOST KEY',
         'I have keys but no locks, and space but no rooms. What am I?',
         {'keyboard','a keyboard'},'Your fingers know the answer.','You found the keys to my ghost.')
    header('CHAPTER 4/5 // THE REVERSED SIGNAL')
    say('A broken mirror displays: TRAEH',PURPLE)
    gate('READ THE MIRROR','Type the word the mirror is hiding.',
         {'heart'},'Read the letters backward.','You recognized my heartbeat.')
    gate('CHAPTER 5/5 // THE LAST SECRET',
         'I can be given freely, never forced, and I grow when shared. What am I?',
         {'love'},'Four letters. The reason you followed me.','The final door opens.')
    static()
    reveal()

if __name__=='__main__':
    main()
