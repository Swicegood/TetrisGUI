import eel, threading
import tetris
char = [None]


eel.init('web')


eel.start('main.html', char_list=(char, ),block=False, size=(240,400), zoom=200)

threading.Thread(target=tetris.main, args=(char, )).start()


# if __name__ == "__main__":
#    _thread.start_new_thread(tetris.main, (char, ))


while True:
    eel.sleep(10)