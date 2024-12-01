#move(200, direction = 'down')
print(move, 10)
for _ in range(360):
  turn(1)
#  wait(0.1)
  move(5, 0.02)

for _ in range(3):
  turn(random(5, 20))
  move(random(10, 200), 0.5)



