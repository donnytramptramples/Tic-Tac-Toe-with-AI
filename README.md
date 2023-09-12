# ChromeDinoAI
Purpose of the project is to train pytorch model to playchrome dino game using own implementation of genetic algorithm.
### Project structure
<pre>
├── game    # game files
|     ├──  static
|     ├──  game.py 
|     ├──  player.py    
|     ├──  obstacles.py 
├── models     # trained models  
├── genetic_algorithm.py    # custom implementation of genetic algorithm
├── model.py    # pytorch model used in project
├── train.py     # training 
├── play.py     # playing vs trained model
</pre>
### How to run
TODO
### Model
As the task is not especially hard model used is quite simple. Input consists of 5 neurons, then fully connected 10-neurons hidden layer, both with relu activation. At the output there is one neuron (also fully connected), because task is just a binary classification (jump or dodge) it uses sigmoid activation.
TODO
### Training
TODO

