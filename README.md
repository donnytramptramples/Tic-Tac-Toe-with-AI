# ChromeDinoAI
Purpose of the project is to train neural network to play chrome dino game
## Game
Pygame implementation of popular chrome no-internet game where you are running dinosaur and have to avoide cactuses and birds by jumping and bending.
While dodgeing obstacles your score increases as well as game speed.
## How does AI work
Dino brain used to control actions is neural network with three layers, layers are implemented as numpy arrays with weights values. First layer, given input vector with current game state (of length 5, where v[0]-game speed, v[1]-distance to first obstacle, v[2]-heights of first obstacle, v[3]-distance to second obstacle, v[4]-height of second obstacle), computes and passes it to hidden layer which produces output value, based on this value dino brain decides to jump, bend or do nothing. To train it, number of games is played (specified by num_of_generations parameter), in each one, number of dinos (specified by population_size parameter) participates, the one with the best score is used for creating population for next game by mutations. Best dino from last generation is saved and can be later used to compete with human player. Video showing training process (num_of_generations= , population_size= ):
## Run
```
git clone https://github.com/witek3100/ChromeDinoAI
pip install requirements.txt
```
<br/><br/>
```
python player_only.py
```
To see how game works.
<br/><br/>
```
python training_nn.py
```
To see training process, you can pass optional arguments to change training parameters:  
num_of_generations - default 500  
population_size - default 40  
like that:
```
python training_nn.py num_of_generations=500 population_size=40
```
. Afterwards result is saved to trained_nn.pkl, you'll use it in next scope.
<br/><br/>
```
python player_vs_ai.py
```
to challange saved model.
