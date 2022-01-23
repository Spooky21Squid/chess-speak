from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains

import os

from scipy.io.wavfile import write
import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

from deepgram import Deepgram
import asyncio, json

DEEPGRAM_API_KEY = '799ecb2a772ef3c9b9d6c0259412ebe76520ddbe'
PATH_TO_FILE = 'output.wav'
wd = webdriver.Firefox()
wd.get("https://www.chess.com/play/computer/")

async def analyse():
    # Initializes the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    j = ''
    # Open the audio file
    with open(PATH_TO_FILE, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await dg_client.transcription.prerecorded(source, {'punctuate': False})
        #print(json.dumps(response, indent=4))
        j = json.loads(json.dumps(response, indent=4))
    words = list()
    for r in j["results"]["channels"][0]["alternatives"][0]["words"]:
        words.append(r["word"])
    print("words:")
    print(words)
    if len(words) != 5:
        print("Audio did not record correctly...")
        return
    source = Chess.convert2(words[0], words[1])
    destination = Chess.convert2(words[3], words[4])
    print("source: " + source)
    print("destination: " + destination)
    Chess.move(wd, words[0], words[1], words[3], words[4])

        


class Chess:

    def convert2(x1, y1):
        """ Converts a text move like 'd three' to a readable move like square-43 """
        x2 = ""
        y2 = ""

        if x1 == "a":
            x2 = 1
        elif x1 == "b":
            x2 = 2
        elif x1 == "c":
            x2 = 3
        elif x1 == "d":
            x2 = 4
        elif x1 == "e":
            x2 = 5
        elif x1 == "f":
            x2 = 6
        elif x1 == "g":
            x2 = 7
        elif x1 == "h":
            x2 = 8
        
        if y1 == "one":
            y2 = 1
        elif y1 == "two":
            y2 = 2
        elif y1 == "three":
            y2 = 3
        elif y1 == "four":
            y2 = 4
        elif y1 == "five":
            y2 = 5
        elif y1 == "six":
            y2 = 6
        elif y1 == "seven":
            y2 = 7
        elif y1 == "eight":
            y2 = 8
        
        return "square-" + str(x2) + str(y2)


    def convert(move):
        """ Converts a text move like d3 to a readable move like square-43 """
        if move[0] == "a":
            return "square-1" + move[1]
        elif move[0] == "b":
            return "square-2" + move[1]
        elif move[0] == "c":
            return "square-3" + move[1]
        elif move[0] == "d":
            return "square-4" + move[1]
        elif move[0] == "e":
            return "square-5" + move[1]
        elif move[0] == "f":
            return "square-6" + move[1]
        elif move[0] == "g":
            return "square-7" + move[1]
        elif move[0] == "h":
            return "square-8" + move[1]
        else:
            return "invalid"


    def move(wd, x1, y1, x2, y2):
        """ Attempts to move the chess piece from the from_ square to the to square
        using selenium webdriver as wd.
        from_ and to are strings representing the squares, for example, from_ = d3.
        The chess piece will be picked up. If the move is possible, it will be moved.
        If the move is not possible, it will be put back down.
        If a square is invalid, it will quit."""

        f = Chess.convert2(x1, y1)
        t = Chess.convert2(x2, y2)

        if f == "invalid" or t == "invalid":
            return

        #piece = wd.find_elements_by_class_name(f)[0]
        for e in wd.find_elements_by_class_name(f):
            if "piece" in e.get_attribute("class"):
                piece = e

        piece.click()
        time.sleep(1)
        hints = wd.find_elements_by_class_name("hint")
        captureHints = (wd.find_elements_by_class_name("capture-hint"))
        valid_move = False
        
        for h in hints:
            if t in h.get_attribute('class'):
                valid_move = True
                dropTarget = h
                break
        
        for h in captureHints:
            if t in h.get_attribute('class'):
                valid_move = True
                dropTarget = h
                break
        
        if valid_move == False:
            print(x1 + " " + y1 + " to " + x2 + " " + y2 + " Failed: Invalid move")
            return

        print(x1 + " " + y1 + " to " + x2 + " " + y2 + " Succeeded")
        actions = ActionChains(wd)
        actions.drag_and_drop(piece, h).perform()


if __name__ == "__main__":
    # initialise
    fs = 44100  # Sample rate
    seconds = 4  # Duration of recording
    filename = "output.wav"

    while True:

        try:

            if os.path.exists('output.wav'):
                os.remove('output.wav')
            
            input("Press Enter to record your move...")
            print("Recording...")

            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            write(filename, fs, myrecording)  # Save as WAV file
            print("Recorded move.")
            #input("enter to continue...")

            # get dialog from deepgram
            asyncio.run(analyse())

            # process, turn into moves
            

            #Chess.move(wd, "e2", "e3")
        
        except KeyboardInterrupt:
            print("Bye")
            exit()

    input("Press the Enter key to continue...")