print(move, 10) # prints the dokkumentation of move
wait(1)
for _ in range(360):
    turn(1)
    move(5, 0.02)

for _ in range(3):
    turn(random(5, 20))
    move(random(10, 200), 0.5)
my_variable = 0