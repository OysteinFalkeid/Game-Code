while True:
    key = keypress()
    if key == 'w':
        move(100, None, 'up')
    elif key == 's':
        move(100, None, 'down')
    elif key == 'a':
        move(100, None, 'left')
    elif key == 'd':
        move(100, None, 'right')