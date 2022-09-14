# Factored Talk - RL
![Alt text](agent_gifs/agent_max__123.gif)

## Reinforcement Learning - Can you beat the AI in a race? 🏎️
This repo contains everything needed to run Car Racing environment locally to play against an AI agent!

### Installation Instructions

You can clone the repo by running:

    git clone https://github.com/CarloCDT/factored-talk-RL.git

I would recommend to use a Python Virtual Environment Manager like `virtualenvwrapper`. This way the next step would be to create a new environment:

    mkvirtualenv factored_talk_rl
    
Activate your brand new virtual environment if needed:

    workon factored_talk_rl
    
Change the directory to the factored-talk-rl repo:

    cd factored-talk-rl
    
Install the requirements from `requirements.txt`:

    pip install -r requirements.txt

You should be ready to play and challenge Max Verstappen agent in a race now!

### Playing against the AI

To play against the AI a singel race you just need to run:

    python play_car_racing.py

You will be asked to give an integer number which will the random seed to choose the track. Both you and the AI agent will drive in the same track, and the score will be printed in the terminal window. 

However, if you're ready to challenge the world champions in a 10 race competition, add the `--championship` flag

    python play_car_racing.py --championship

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
