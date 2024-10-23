import pygame
import time
import random

# Initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Set up display
window_width = 600
window_height = 400
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)

# Load sounds
eat_sound = pygame.mixer.Sound("eat_sound.wav")  # Ensure you have this sound file
game_over_sound = pygame.mixer.Sound("game_over.wav")  # Ensure you have this sound file
background_music = pygame.mixer.Sound("background_music.mp3")  # Ensure you have this sound file

# Snake properties
snake_block = 10
snake_speed = 15

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Difficulty settings (snake speeds)
difficulty_levels = {"Easy": 10, "Medium": 20, "Hard": 30}
difficulty = "Medium"  # Default difficulty

# Function to display score
def display_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    game_window.blit(value, [0, 0])

# Function to draw a rounded rectangle
def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

# Function to draw the snake
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(game_window, white, (segment[0], segment[1], snake_block, snake_block))

# Function to display game over message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_window.blit(mesg, [window_width / 6, window_height / 3])

# Function to draw the menu
def draw_menu(options, selected_index):
    game_window.fill(black)
    for i, option in enumerate(options):
        if i == selected_index:
            color = green  # Highlight the selected option
        else:
            color = white
        text = font_style.render(option, True, color)
        game_window.blit(text, [window_width // 3, window_height // 3 + i * 40])
    pygame.display.update()

# Function for the main menu
def main_menu():
    options = ["Start Game", "Choose Difficulty", "Set Speed", "Adjust Volume", "Quit"]
    selected_index = 0

    menu_running = True
    while menu_running:
        draw_menu(options, selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Enter key
                    if selected_index == 0:  # Start Game
                        game_loop()
                    elif selected_index == 1:  # Choose Difficulty
                        choose_difficulty()
                    elif selected_index == 2:  # Set Speed
                        set_speed()
                    elif selected_index == 3:  # Adjust Volume
                        adjust_volume_menu()
                    elif selected_index == 4:  # Quit
                        pygame.quit()
                        quit()

# Function for choosing the difficulty
def choose_difficulty():
    global snake_speed, difficulty
    options = list(difficulty_levels.keys())
    selected_index = options.index(difficulty)  # Start with the current difficulty
    menu_running = True

    while menu_running:
        draw_menu(options, selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    difficulty = options[selected_index]
                    snake_speed = difficulty_levels[difficulty]
                    return  # Go back to the main menu

# Function for setting custom speed
def set_speed():
    global snake_speed
    speed_options = [5, 10, 15, 20, 25]
    selected_index = speed_options.index(snake_speed)
    menu_running = True

    while menu_running:
        draw_menu([str(speed) for speed in speed_options], selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(speed_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(speed_options)
                elif event.key == pygame.K_RETURN:
                    snake_speed = speed_options[selected_index]
                    return  # Go back to the main menu

# Function for adjusting volume
def adjust_volume_menu():
    volume_options = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    selected_index = volume_options.index(background_music.get_volume())
    menu_running = True

    while menu_running:
        draw_menu([str(volume) for volume in volume_options], selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(volume_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(volume_options)
                elif event.key == pygame.K_RETURN:
                    background_music.set_volume(volume_options[selected_index])
                    return  # Go back to the main menu

# Main game loop

# Function to pause the game
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume game
                    paused = False
        game_window.fill(black)
        message("Paused. Press P to continue", green)
        pygame.display.update()

def game_loop():
    # Snake starting position
    snake_x = window_width // 2
    snake_y = window_height // 2
    snake_x_change = 0
    snake_y_change = 0

    # Snake body list
    snake_list = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    # Game clock (controls speed)
    clock = pygame.time.Clock()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Snake movement control
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_x_change == 0:
                    snake_x_change = -snake_block
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT and snake_x_change == 0:
                    snake_x_change = snake_block# ... (previous code)

                elif event.key == pygame.K_UP and snake_y_change == 0:
                    snake_y_change = -snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_DOWN and snake_y_change == 0:
                    snake_y_change = snake_block
                    snake_x_change = 0
                elif event.key == pygame.K_p:  # Pause the game
                    pause_game()

        # Update snake position
        snake_x += snake_x_change
        snake_y += snake_y_change

        # Fill screen with black before drawing
        game_window.fill(black)

        # Draw food using a rounded rectangle
        draw_rounded_rect(game_window, red, (food_x, food_y, snake_block, snake_block), 5)

        # Update snake's body (head is a list of coordinates)
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)

        # Keep the snake length fixed
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if the snake eats the food
        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
            snake_length += 1
            score += 10  # Increment score
            eat_sound.play()  # Play eating sound

        # Draw the snake
        draw_snake(snake_list)

        # Display score
        display_score(score)

        # Update the display
        pygame.display.update()

        # Control the speed of the game
        clock.tick(snake_speed)

        # Check for boundary collisions
        if snake_x >= window_width or snake_x < 0 or snake_y >= window_height or snake_y < 0:
            running = False

        # Check if the snake hits itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                running = False

    # Game over
    game_window.fill(black)
    game_over_sound.play()
    message("Game Over! Press C-Play Again or Q-Quit", red)
    pygame.display.update()
    time.sleep(2)

    # Check for restart (outside the game loop)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    game_loop()  # Call game_loop again to restart

# Start the game
background_music.play()  # Start playing background music
main_menu()