while True:
    key = keypress()
    if key == 'w':
        move(100, 0.2, 'up')
    elif key == 's':
        move(100, 0.2, 'down')
    elif key == 'a':
        move(100, 0.2, 'left')
    elif key == 'd':
        move(100, 0.2, 'right')