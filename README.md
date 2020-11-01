# AutoSnakeGame
A classic snake game, it's supposed to play itself.

FILES:

snake.py
	The base game.

snake-with-solver.py
	A manually coded solving algorithm. 
	It doesn't work very well

threading-snake.py:
	A solving algorithm that using the threading library
	and randomly generated paths to allow the snake to find the apple. 

TO PLAY:

On Linux, activate snake-env with:

$source newEnv/bin/activate

then run snake.py:

$python3 snake.py
