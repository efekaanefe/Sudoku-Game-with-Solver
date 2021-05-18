# Sudoku-Game-with-Solver

# Requirements
python 3
pygame

# How To Play
run sudoku.py

# Controls
You can select a square by clicking on it with mouse.

After you selected a square you can change it with arrow keys or again mouseclick

If you press a keypad button in range of 1-9 assigns a possible value to that square. You can assign max 3 value to one square.

If you press return or keypad_enter and if sq_selected has only one assigned value, it will try to put that value in that square if possible. 
If not possible, there will be a message in the terminal saying it is invalid to put that value there.

You can delete assigned values or valid values which you put into the square by pressing backspace.

If you press space, sudoku solver algorithm will solve the board with back tracking, and you will be able to see its process.

# PROS
Good example of visulazation of backtracking

# CONS
There is only one default board. 

It finds only a one solution ,if there is, and must quit immediately after (after finding solution, it says press enter to quit to user in terminal). This is because algorithm doesn´t return solved board, it just solves and shows, and may possibly look for other solutions, but I couldn´t figure it out to show other solutions, (there is only one solution to default board, but this wouldn´t be the case always), with GUI stuff. So I make it quit after finding one solution. It can be improved.

There is "pygame.error: Library not initialized" error after it solves and quits.

It is not fully GUI. There are three terminal outputs. First one for checking if the value valid or not to selected square, second one is endgame message, and last one is to quit after using sudoku solver.





<img src="Sudoku Game (+Solver)/screenshot.png" width="500">

