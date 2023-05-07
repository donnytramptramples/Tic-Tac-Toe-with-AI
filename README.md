# ChromeDinoAI
Training neural network to play chrome dino using genetic algorithm
## Run
```
git clone https://github.com/witek3100/ChromeDinoAI
pip install requirements.txt
```
## Project scopes 
### 
run
```
python player_only.py
```
to see how game works.
### Train neural network 
run
```
python training_nn.py
```
to see training process (patience recommended), you can pass optional arguments to change training parameters:

. Afterwards result is saved to trained_nn.pkl, you'll use it in next scope.
### play vs AI
```
python player_vs_ai.py
```
to challange model you've trained.
