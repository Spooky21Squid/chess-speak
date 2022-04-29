# chess-speak
Solution for Hack Cambridge - Chess Speak

Converts voice moves into Chess.com moves using the Deepgram Python API and Selenium

***Note***: You may need your own Deepgram API key

# How to run
- Clone
- Install requirements from requirements.txt
- Run chessSpeak.py

# chessSpeak.py Execution
When running chessSpeak, the terminal will remain open (Don't close it) and chess.com will open in a new browser. From here you can:

1. Firstly close all the annoying popups
2. Choose which player to play against. Click on their face, then and click Choose
3. Pick your challenge
4. Click Play

The game is on! When it's your turn, click 'Enter' inside the terminal and say a move, for example, 'A2 to A4'. Be quick because you only have 4 seconds.

Sometimes, the program won't quite recognise your move. If so, it will say 'Invalid move' in the terminal, and you can try again by repeating the above.

When a valid move has been entered, your chess piece will move, then the opponent will move, rinse and repeat.

# Future Prospects
I can see this program being useful for people that are sight-impaired or have limited motor functions, as chess.com currently doesn't have the option for voice commands. This program could be turned into a browser extension, and the way it interacts with Deepgram could be refined to real-time voice analysis using sockets to avoid a time limit. Maybe some voice feeback would be helpful too.
