import pygame
import keyboard
import os
import time

def updateConsole():
    os.system('cls' if os.name=='nt' else 'clear')
    print()
    print("Aktueller Track: ", tracks[currentIndex] if currentIndex >= 0 and currentIndex < len(tracks) and isPlaying else "")
    print()
    print("Nächster  Track: ", tracks[nextIndex] if nextIndex >= 0 and nextIndex < len(tracks) else "")
    print()
    print()
    print()
    if isFadingOut and pygame.mixer.music.get_busy():
        print("Leertaste:                  Fading Out ...")
    elif pygame.mixer.music.get_busy():
        print("Leertaste:                  Fadeout und Pause")
    else: 
        print("Leertaste:                  Starten")
    print("Pfeiltaste rechts/links:    Auswählen des nächsten Tracks")
    print()
    print("q:                          Beenden")


isPlaying = False
isFadingOut = False
currentIndex = -1
nextIndex = 0   

tracks_ = os.listdir("./")
tracks = []
for track in tracks_:
    if track.endswith(".mp3"):
        tracks.append(track)

tracks.sort()


pygame.mixer.init()

updateConsole()

while True:
    if (not pygame.mixer.music.get_busy()) and (isFadingOut or isPlaying):
        isFadingOut = False
        isPlaying = False
        updateConsole()

    # fuktioniert mit keyboard.read_key() nicht !! (Triggert 2x)
    keyboardEvent = keyboard.read_event()
    key = keyboardEvent.name

    if not keyboardEvent.event_type == "down":
        pass

    elif(key == "space" and not pygame.mixer.music.get_busy()):
        isFadingOut = False
        if nextIndex >= len(tracks):
            break
        pygame.mixer.music.load(os.path.abspath("./" + tracks[nextIndex]))
        pygame.mixer.music.play()
        isPlaying = True
        currentIndex = nextIndex
        nextIndex += 1
        if nextIndex >= len(tracks):
            nextIndex = 0

    elif(key == "space" and not isFadingOut):
        isFadingOut = True
        updateConsole()
        pygame.mixer.music.fadeout(3*1000)
        time.sleep(3-0.1)
        pygame.mixer.music.stop()
        isPlaying = False
        isFadingOut = False

    elif(key == "q" or key == "Q"):   
        break

    elif(key == "nach-rechts"):
        nextIndex += 1
        if nextIndex >= len(tracks):
            nextIndex = 0
        time.sleep(0.2)
    
    elif(key == "nach-links"):
        nextIndex -= 1
        if nextIndex < 0:
            nextIndex = len(track)
        time.sleep(0.2)
    
    updateConsole()