import gym
import pygame
import numpy as np
import argparse

from max_verstappen import run_max

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Play Car Racing')
    parser.add_argument('--championship', action='store_true')
    args = parser.parse_args()

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

    if not args.championship:

        # Select a track
        try:
            track_num = int(input("Enter a track (Input the random seed): "))
        except:
            assert False, "Error: Invalid track number."

        # Initialize environment
        env = gym.make('CarRacing-v2', render_mode = 'human')
        pygame.init()

        print(f"---------------------------------")
        print(f"Single Race")
        print(f"---------------------------------")

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
            print("Congratulations!! You beat the world champion in a race")
        else:
            print("You're fast... But Max is faster.")

        print(f"---------------------------------")

    else:

        scores = []
        tracks = [32, 45, 46, 83, 123, 934, 563, 1023, 27546, 32450]
        verstappen_scores = [879.66, 893.63, 867.32, 881.82, 856.52, 823.08, 875.0, 772.61, 873.58, 882.14]

        # Initialize environment
        env = gym.make('CarRacing-v2', render_mode = 'human')
        pygame.init()

        for idx,track in enumerate(tracks):

            print(f"---------------------------------")
            print(f"Race {idx+1} out of {len(tracks)}")
            print(f"---------------------------------")

            isopen = True
            env.reset(seed=track)
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
                    scores.append(total_reward)

                    # Max Verstappen Run
                    verstappen_score = verstappen_scores[idx]
                    print(f"World Champion Score: {verstappen_score:.2f}")
                    isopen = False
                    break
            
            if total_reward > verstappen_score:
                print("You won this race!")
            else:
                print("Sorry, Max won this race.")

        env.close()

        average_score = np.mean(scores)
        average_max_score = np.mean(verstappen_scores)

        print(f"---------------------------------")
        print(f"---------------------------------")
        print(f"Your average result: {average_score:.2f} points")
        print(f"Max's average result: {average_max_score:.2f} points")

        if average_score > average_max_score:
            print("Congratulations!! You're the new world champion")
        else:
            print("Sorry mate, Max keeps the crown... maybe try it again?")

        print(f"---------------------------------")
