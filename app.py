import sys
import pygame
import pygame_gui
import yt_dlp
from ffpyplayer.player import MediaPlayer

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = (800, 600)
BACKGROUND_COLOR = (50, 50, 50)
FONT_COLOR = (255, 255, 255)
FPS = 60

# Screen Setup
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Modern Music Player")

# UI Manager
manager = pygame_gui.UIManager(SCREEN_SIZE)

# UI Elements
title_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((300, 20), (200, 30)),
    text="Music Player",
    manager=manager,
)

text_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 70), (400, 30)),
    manager=manager,
)
search_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 110), (180, 50)),
    text="Search & Play",
    manager=manager,
)
stop_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((420, 110), (180, 50)),
    text="Stop",
    manager=manager,
)

# Temp audio stream holder
player = None
is_playing = False

def fetch_and_play_audio(song_name):
    """Fetches the audio stream URL and plays it."""
    global player

    # Use yt_dlp to search and fetch audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            audio_url = results['url']
        except Exception as e:
            print(f"Error fetching audio: {e}")
            return False

    # Play the audio stream with ffpyplayer
    try:
        # Stop any previous process
        stop_audio()

        # Play the decoded audio with ffpyplayer
        player = MediaPlayer(audio_url)
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

def stop_audio():
    """Stops the currently playing audio."""
    global player, is_playing
    if player:
        player.close_player()
        player = None
    is_playing = False

# Main Loop
clock = pygame.time.Clock()
running = True

while running:
    time_delta = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # UI Event Handling
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == search_button:
                song_name = text_input.get_text()
                if song_name.strip():
                    fetch_and_play_audio(song_name)
            elif event.ui_element == stop_button:
                stop_audio()

        # Pass events to UI manager
        manager.process_events(event)

    # Update UI
    manager.update(time_delta)

    # Draw UI
    screen.fill(BACKGROUND_COLOR)
    manager.draw_ui(screen)
    pygame.display.update()

# Cleanup
stop_audio()
pygame.quit()
sys.exit()
