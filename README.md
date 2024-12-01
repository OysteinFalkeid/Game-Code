# Educational programing in Python ![alt text](https://github.com/OysteinFalkeid/GameCode/blob/main/source_code/imports/sprites/icon.png)
![alt text](https://github.com/OysteinFalkeid/GameCode/blob/main/source_code/imports/sprites/Screenshot.png)

this program is written in and runs in python.
current version suport is python 3.12.6 other versions shold work

# ownership
This project is created and oned by Øystein Falkeid.
The program is free to use and distribute for educational purpuses.
A 'GNU GENERAL PUBLIC LICENSE' Version 3, 29 June 2007 has been added and 
can be red on https://github.com/OysteinFalkeid/GameCode

# geting started
In the source_code directory run the main.py file in the your python interpreter. (python 3.12 has been tested)

The easyest metod of downloading the project is to run git clone. otherwise a simple download from GitHub will sufice.

# Missing implementations

## Move

The move function is implemented but is not adjustable
1. note the move function is adjustable but parameters ar not definable

Missing implementation of a time variable
1. time is implemented and adjust step_disst and number of steps

move must be implemented with a relative direction and options for x and y spesific movement


## Turn
1. has ben implemented with a relative and absolute value alternative

## Set Position

## set direction
bot a spesific rotation and a rotation rellative to mouse cursor
1. integrated innto the turn function

## print
Define print style in think or speak
define time duration for print
1. print has a time implementation 
2. the printed text is currentley printed at the sprites center.

## sprite
some premade custum paths to images in sprites
1. path is sent to main game handler where it is loaded as a sprite

ability to load custum sprites from sprite folder by name 
sprite should be a list and should be incrementable like the sprite.group class from pygame

the background can be implemented as a sprite.
1. possible but the user has to create a seperrate file

sprites should be able to be rectangles and circles

sprites should be transformable (resized)
1. implemented but not adjustable by player.

A true fals value for drawing the sprite

## entity layer list
layer objects to define draw order

## sound
???

## keyboard events
support for key press events

## event handler 
Support for custum events created by the playyer

## defined start condition
different start condition for running kode block. 
This could be implemented with a droppdown menue

## timer
start timer
1. timer start uppon prosess start

stopp timer
1. timer never stoppes because the timer itself is imported from windows

reset timer
1. By running timer(True) or timer(reset = True) the timer resets
2. the timer dose not return a value upon reset.

event on timer reaching time

time delay
1. A simple wait function implemented

## random
random number generator for float int and other
1. the random number gennerator is based uppon a float number from 0 to 1.
2. the standard opperation is to return this float as 0 or 1
3. spessifying a min and max value sets the span of the random number.
4. spessifying the float variable as true disables the typcasting to int.

## hitbox
some sort of hitbox and event on hit
on hit custumisable for user








