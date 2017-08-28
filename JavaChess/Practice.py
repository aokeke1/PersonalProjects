# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 23:58:34 2017

@author: arinz
"""
import re
def showAsBoard1(bitboard):
    output = ""
    bitboard = bin(((1 << 64) - 1) & bitboard)[2:]
    while len(bitboard)<64:
        bitboard = "0" + bitboard
    for i in range(8):
        output += bitboard[i*8:i*8+8]+"\n"
    print (output)
    
def showAsBoardLittleEndian(bitboard):
    output = ""
    bitboard = bin(((1 << 64) - 1) & bitboard)[2:]
    while len(bitboard)<64:
        bitboard = "0" + bitboard
    for i in range(8):
        toAdd = bitboard[i*8:i*8+8]
        toAdd = toAdd[::-1]
        output += toAdd+"\n"
    print (output)
    
def reverse_board(bitboard):
    bitboard = bin(((1 << 64) - 1) & bitboard)[2:]
    while len(bitboard)<64:
        bitboard = "0" + bitboard
    bitboard = bitboard[::-1]
    return int("0b"+bitboard,2)
def get_sq_mask(r_board):
    x = bin(reverse_board(r_board))[2:]
    while len(x)<64:
        x = "0" + x
    inds = []
    for m in re.finditer('1', x):
        inds.append(m.start())
    output = 0
    ranks = 255
    files = 72340172838076673
    for i in inds:
        output |= (ranks<<(8*(i//8)))
        output |= (files<<(i%8))
    return output
def get_file_mask(r_board):
    x = bin(reverse_board(r_board))[2:]
    while len(x)<64:
        x = "0" + x
    inds = []
    for m in re.finditer('1', x):
        inds.append(m.start())
    output = 0
    files = 72340172838076673
    for i in inds:
        output |= (files<<(i%8))
    return output
def get_rank_mask(r_board):
    x = bin(reverse_board(r_board))[2:]
    while len(x)<64:
        x = "0" + x
    inds = []
    for m in re.finditer('1', x):
        inds.append(m.start())
    output = 0
    ranks = 255
    for i in inds:
        output |= (ranks<<(8*(i//8)))
    return output
    
r = int("0b\
00001000\
00000000",2)
o = int("0b\
10001000\
10000000\
10001000\
00000000",2)
o_prime = reverse_board(o)
r_prime = reverse_board(r)
print ("o")
showAsBoardLittleEndian(o)
print ("r")
showAsBoardLittleEndian(r)

horizontalattacks = (o-2*r)^reverse_board(reverse_board(o)-2*reverse_board(r))
verticalattacks = ((o&get_file_mask(r))-2*r)^reverse_board(reverse_board(o&get_file_mask(r))-2*reverse_board(r))
mask = get_sq_mask(r)
print ("horizontal attacks")
showAsBoardLittleEndian(horizontalattacks)
print ("vertical attacks")
showAsBoardLittleEndian(verticalattacks)
print ("mask")
showAsBoardLittleEndian(mask)
print ("final")
attacks = horizontalattacks|verticalattacks
showAsBoardLittleEndian(attacks&mask)

