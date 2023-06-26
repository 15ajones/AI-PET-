import pygame
import threading



def playSound():

    # Initialize Pygame
    pygame.init()

    # Set the audio device
    pygame.mixer.init()

    # Load the audio file
    sound = pygame.mixer.Sound("output.wav")

    # Play the audio file
    sound.play()

    # Wait until the sound finishes playing
    pygame.time.wait(sound.get_length() * 1000)

    # Quit Pygame
    pygame.quit()

def main():
    playSound_t = threading.Thread(target=playSound)
    playSound_t.start()


main()