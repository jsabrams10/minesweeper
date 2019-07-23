John Abrams
5/12/2019
CS 314 (Prin. Prog.) - Final Project
readme.txt

This application is a Python program for the classic game "Minesweeper". It's designed to be run through the command line and offers a small but simple graphical user interface. I've completely customized the 16x16 images that appear on each square of the board, which are provided in a library called "spaceImages". The program imports "Tkinter" in order to access the "Tk" GUI toolkit; other imports include "deque", "random", and "tkMessageBox". The program can be run on most machines as follows:

[from the command line, within "johnsGame"]$ python johnsMinesweeper

A dialog box labeled "John's Minesweeper" will appear displaying a fresh board. The user may then click on any of the square spaces in order to reveal what lies beneath: either a number - denoting how many mines surround the square - or a flame - indicating a mine (quickly followed by a message box indicating a loss). Optionally, the user may right-click on still-covered squares to place a flag on them, symbolizing the assumption that there's a bomb underneath. If the user loses the game, all incorrectly placed flags will be replaced with crossed-out flags representing an incorrect assumption. Upon winning/losing the game, it's up to the user to exit the board's dialog box - this decision was made in order to provide the user the option of analyzing both the locations of the mines and their successes/mistakes.
