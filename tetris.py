#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, unicode_literals, print_function
import os
width = 10
height = 20
regex = r"[\-|]"
regex1 = r"[ABCDEFG\-|]"
regex2 = r"[ABCDEFG]"
regex4 = r"[ABCDEFG|]"
score = 0
speed = 5000
acceleration = 6

#import tty, termios, 
import copy
import sys
import time,re
import random, eel, socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 8080))
s.listen()



class Tetrimino(object):

    content: list

    def __init__(self):
        self.posx = round(width/2)
        self.posy = 0

    def advance(self):
        self.posy += 1

    def rotate(self):

        new_tm = copy.copy(self)
        new_tm = wipe(new_tm)
        posy = 0
        if self.shape == 'A':
            if  self.content == [
               [" ","A"," "],
               [" ","A"," "],
               [" ","A"," "],
               [" ", "A", " "]
            ]:
                new_tm.content :list  = [
                    [" "," "," "," "],
                    ["A","A","A","A"],
                    [" ", " ", " ", " "]
                ]

            elif self.content == [
                    [" "," "," "," "],
                    ["A","A","A","A"],
                    [" ", " ", " ", " "]
                ]:
                new_tm.content = [
                    [" ", "A", " "],
                    [" ", "A", " "],
                    [" ", "A", " "],
                    [" ", "A", " "]
                ]
            self.content = new_tm.content
            return

        for y in self.content:
            posx = 0
            for x in y:
                new_tm.content[posx][round(len(self.content) / 2) - posy] = x
                posx += 1
            posy += 1
        self.content = new_tm.content


    def shift_l(self):
        self.posx -= 1


    def shift_r(self):
        self.posx += 1


    def create(self, shape):
        self.shape = shape
        if shape == "A":
           self.content = [
               [" ","A"," "],
               [" ","A"," "],
               [" ","A"," "],
               [" ", "A", " "]
           ]
        elif shape == "B":
            self.content = [
                [" ","B", " "],
                [" ","B", " "],
                ["B","B"," "]
            ]
        elif shape == "C":
            self.content = [
                ["C","C","C"],
                [" ","C"," "],
                [" "," "," "]
            ]
            pass
        elif shape == "D":
            self.content = [
                ["D", "D", " "],
                [" ", "D", "D"],
                [" ", " ", " "]
            ]
            pass
        elif shape == "E":
            self.content = [
                ["E", "E", " "],
                [" ", "E", " "],
                [" ", "E", " "]
            ]
            pass
        elif shape == "F":
            self.content = [
                ["F", "F"],
                ["F", "F"]
             ]
            pass
        elif shape == "G":
            self.content = [
                [" ", "G", "G"],
                ["G", "G", " "],
                [" ", " ", " "]
            ]
            pass
        else:
            return KeyError

class Board:

    def __init__(self,height, width):
        self.charmap = [[' ' for x in range(width + 2)] for y in range(height)]

        for y in range(height):
            for x in range(width):
                self.charmap[y][x + 1]= " "
            self.charmap[y][0] = "|"
            self.charmap[y][width + 1]= "|"

        lastline = "+"
        for x in range(width):
             lastline=lastline+"-"
        lastline=lastline+"+"
        self.charmap.append(lastline)

    def __iadd__(self, tm):
        self:Board
        posy = 0
        for y in tm.content:
            posx = 0
            for x in y:
                if not re.match(regex1, self.charmap[tm.posy + posy][tm.posx + posx]):
                    self.charmap[tm.posy + posy][tm.posx + posx] = x
                posx += 1
            posy += 1
        return self

    def __isub__(self, tm):
        self:Board
        blank = wipe(tm)
        if not collision(self, blank):
            posy = 0
            for y in blank.content:
                posx = 0
                for x in y:
                    if not re.match(regex, self.charmap[tm.posy + posy][tm.posx + posx]) and tm.content[posy][posx] is not ' ':
                        self.charmap[tm.posy + posy][tm.posx + posx] = x
                    posx += 1
                posy += 1
        return self

def wipe(tm):
    blank = copy.deepcopy(tm)
    posy = 0
    for y in tm.content:
        posx = 0
        for x in y:
            blank.content[posy][posx] = " "
            posx += 1
        posy += 1
    return blank

def collision(cur_board,tm):
    testboard = copy.copy(cur_board)
    posy = 0

    for y in tm.content:
        posx = 0
        for x in y:
            try:
                if re.match(regex1, testboard.charmap[tm.posy+posy][tm.posx+posx]) and x is not ' ':
                    return True
            except:
                return True
            finally:
                posx += 1
        posy += 1
    return False

def row_finished(cur_board):
    rows = []
    row = 0
    for y in cur_board.charmap:
        full = True
        for x in y:
            if not re.match(regex4,x):
                full = False
                break
        if full:
            rows.append(row)
        row +=1
    return rows

def slide_down(cur_board,rows):
    total_rows = 0
    blink_time = .25
    global score
    full_board = copy.deepcopy(cur_board)
    for row in rows:
        posx =0
        for x in cur_board.charmap[row]:
            if not re.match(regex,x):
                cur_board.charmap[row][posx] = ' '
            posx +=1
        total_rows +=1
    render(cur_board.charmap)
    for x in range(3):
        time.sleep(blink_time)
        render(full_board.charmap)
        time.sleep(blink_time)
        render(cur_board.charmap)



    score = score + (500 * 2**total_rows)

    for i in range(total_rows):
        for row in range(rows[i],0,-1):
            posx = 0
            for x in cur_board.charmap[row-1]:
                if not re.match(regex, x) and row <= height-1:
                    cur_board.charmap[row][posx] = x
                posx += 1



def render(board):
    y = 0
    eel.clear_canvas_js()
    eel.print_js(board)
    for _ in board:
        y += 1
    eel.draw_text_js(('SCORE\r'),10, (40*y)+80)
    eel.draw_text_js(score, 10, (40*y)+40)

    # os.system('clear')
    # eel.clear_canvas_js()
    # yy = 50
    # for y in board:
    #     eel.draw_text_js((''.join(y)+'\r'),10, yy)
    #     yy += 40
    # eel.draw_text_js(('SCORE\r'),10, yy)
    # eel.draw_text_js(score, 10, yy+40)


def main(char_list):
    global speed
    myboard = Board(height, width)
    cur_piece = Tetrimino()
    cur_piece.create("A")
    pos_change = True
    gameover = False
    gotobottom = False
    eel.print_js(myboard.charmap)


    while not gameover:
        bottom = True
        while not collision(myboard,cur_piece):
            if row_finished(myboard):
                rows = row_finished(myboard)
                slide_down(myboard, rows)
                pos_change = True
            prev_piece = copy.deepcopy(cur_piece)
            if pos_change:
                myboard += cur_piece
                render(myboard.charmap)
                myboard -= cur_piece
            if gotobottom:
                char_list[0] = 32
            if char_list[0] is not None:
                print(f'char={char_list[0]}')
                if char_list[0] in ('s','S','5',38):
                    cur_piece.rotate()
                    bottom = False
                if char_list[0] in ('a','A',"4",52,37):
                    cur_piece.shift_l()
                    bottom = False
                if char_list[0] in ('d','D','6',54,39):
                    cur_piece.shift_r()
                    bottom = False
                if char_list[0] in ('z','Z','2',50,40):
                    cur_piece.advance()
                    bottom = True
                if char_list[0] == 32 and cur_piece.posy is not 0:
                    cur_piece.advance()
                    bottom = True
                    gotobottom =True
                if char_list[0] in ('81','27'):  # x1b is ESC
                    exit()
                char_list[0] = None
                pos_change = True
            else:
                pos_change = False




            if round(time.process_time()*1000)%speed == 0:
                cur_piece.advance()
                bottom = True
                pos_change = True
            if round(time.process_time() * 1000) % 5000 == 0:
                speed = speed - acceleration
                if speed <= 0:
                    speed = 1

        if cur_piece.posy == 0 and bottom is True:
            gameover = True

        cur_piece = prev_piece
        if bottom:
            shape = random.choice('ABCDEFG')
            myboard += cur_piece
            next_piece = Tetrimino()
            next_piece.create(shape)
            cur_piece = next_piece
            gotobottom = False

    eel.draw_text_js("GAME OVER",40,40)

if __name__ == "__main__":
    main()









