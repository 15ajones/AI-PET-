import pygame
import time

# Initialize Pygame
pygame.init()

# Initialize Pygame audio
pygame.mixer.init()

# Load the audio file
audio_file = "output.wav"
pygame.mixer.music.load(audio_file)

# Play audio
pygame.mixer.music.play()

# Event handling loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # Limit the frame rate to avoid high CPU usage
    clock.tick(30)

# Exit mixer
pygame.mixer.quit()
pygame.quit()