import pygame
import sys
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 100)

load_dotenv()

ibm_watson_apikey = os.getenv('apikey')
ibm_watson_url = os.getenv("url")

# textsurface = myfont.render('ABC game started...', False, (255, 255, 255))

def display_string(text):
    textsurface = myfont.render(text, True, (255, 255, 255))
    screen.fill(black)
    screen.blit(textsurface, (0, 0))
    pygame.display.flip()


def play_string(text):
    audio_path = "audios/" + text + '.wav'
    if not Path(audio_path).exists():
        print("Translating the {} to audio...".format(text))
        with open(audio_path, 'wb') as audio_file:
            payload = {'text': text}
            headers = {'Accept': 'audio/wav'}
            response = requests.get(ibm_watson_url + "/v1/synthesize",
                                    auth=('apikey', ibm_watson_apikey),
                                    headers=headers,
                                    params=payload)
            response.raise_for_status()  # ensure we notice bad responses
            audio_file.write(response.content)
        print("Translating the text to audio done.")

    print("Playing audio file {}".format(audio_path))
    pygame.mixer.init()
    s = pygame.mixer.Sound(audio_path)
    s.play()


while 1:
    # gets a single event from the event queue
    event = pygame.event.wait()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if the 'close' button of the window is pressed
            play_string("good bye")
            sys.exit()
        elif event.type == pygame.TEXTINPUT: # Detects the 'INPUT' events
            # gets the key name
            key_name = event.text
            # # converts to uppercase the key name
            key_name = key_name.upper()
            print(u'"{}" key input'.format(key_name))
            display_string(key_name)
            play_string(key_name)



