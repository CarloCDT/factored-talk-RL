import gym
import numpy
import pygame
import numpy as np

from max_verstappen import run_max

if __name__ == "__main__":
    a = np.array([0.0, 0.0, 0.0])

    def register_input():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    a[0] = -1.0
                if event.key == pygame.K_RIGHT:
                    a[0] = +1.0
                if event.key == pygame.K_UP:
                    a[1] = +1.0
                if event.key == pygame.K_DOWN:
                    a[2] = +0.8  # set 1.0 for wheels to block to zero rotation
                if event.key == pygame.K_RETURN:
                    global restart
                    restart = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    a[0] = 0
                if event.key == pygame.K_RIGHT:
                    a[0] = 0
                if event.key == pygame.K_UP:
                    a[1] = 0
                if event.key == pygame.K_DOWN:
                    a[2] = 0

    # Select a track
    try:
        track_num = int(input("Enter a track (Any number!): "))
    except:
        print("Error: Invalid track number.")

    # Initialize environment
    env = gym.make('CarRacing-v2', render_mode = 'human')
    pygame.init()

    isopen = True
    
    env.reset(seed=track_num)
    total_reward = 0.0
    steps = 0
    restart = False
    
    while True:
        register_input()
        s, r, terminated, truncated, info = env.step(a)
        total_reward += r
        steps += 1
        isopen = env.render()
        if terminated or truncated or restart or isopen is False:
            print(f"Final Score: {total_reward:.2f}")

            # Max Verstappen Run
            print("World Champion is running...")
            verstappen_score = run_max(track_num=track_num)
            print(f"World Champion Score: {verstappen_score:.2f}")
            isopen = False
            break
    
    env.close()

    if total_reward > verstappen_score:
        print("Congratulations!! You beat the world champion.")
    else:
        print("You're fast... But Max is faster.")
