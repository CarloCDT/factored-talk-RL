# Factored Talk - RL
## Reinforcement Learning - Can you beat the AI in a race? 🏎️
This repo contains everything needed to run Car Racing environment locally to play against an AI agent!

### Installation Instructions

Instructions for installing, for example command of package manager like:

    git clone https://github.com/CarloCDT/factored-talk-RL.git

I would recommend to use a virtualenv. You can create a virtual env with:

    mkvirtualenv factored_talk_rl
    
Activate your brand new virtual environment if needed:

    workon factored_talk_rl
    
Change the directory to the factored-talk-rl repo:

    cd factored-talk-rl
    
Install the requirements from ´requirements.txt´:

    pip install -r requirements.txt

You should be ready to play and challenge Max Verstappen agent in a race now!

### Playing against the AI

To play against the AI simply run

    python play_car_racing.py

You will be asked to give an integer number which will the random seed to choose the track. Both you and the AI agent will drive in the same track, and the score will be printed in the terminal window. 

### World Championship

These are the tracks in which the AI drivers were tested: The World Championship. Can you beat the AI?

| Track ID      | World Champion Score  | Random Seed | 
| ------------- | --------------------- | ----------- | 
| 1             | 879.66                |32           |
| 2             | 893.63                |45           |
| 3             | 867.32                |46           |
| 4             | 881.82                |83           |
| 5             | 856.52                |123          |
| 6             | 823.08                |934          |
| 7             | 875.0                 |563          |
| 8             | 772.61                |1023         |
| 9             | 873.58                |27546        |
| 10            | 882.14                |32450        |

**Average Score:** 860.53
