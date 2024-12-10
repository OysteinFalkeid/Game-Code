set_sprite('apple.png')
scale(30,30)
score = 0
while True:
    if on_hit('code_file_1'):
        move_to(random(1, 5) * 100, random(1, 5) * 100)
        score += 1
        print(score, 1)