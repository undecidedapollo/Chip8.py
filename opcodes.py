# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 19:30:58 2023

@author: Jake
"""

CLS = 0x0  # Clear Screen 0x00E0
RET = 0xE  # Return       0x00EE

_1nnn = 0x1  # Jump addr nnn
_2nnn = 0x2  # CALL addr nnn
_3xkk = 0x3  # SE Vx, byte: Skip next inst. if Vx = kk
_4xkk = 0x4  # SNE Vx, byte: '' if Vx != kk
_5xy0 = 0x5  # SE Vx, Vy: '' if Vx = Vy
_6xkk = 0x6  # LD Vx, byte: Vx = byte
_7xkk = 0x7  # ADD Vx, byte: Vx = Vx + byte

_8xy0 = 0x0  # LD Vx, Vy: Vx = Vy
_8xy1 = 0x1  # OR Vx, Vy: Vx = Vx OR Vy
_8xy2 = 0x2  # AND Vx, Vy
_8xy3 = 0x3  # XOR Vx, Vy
_8xy4 = 0x4  # ADD Vx, Vy, VF = carry
_8xy5 = 0x5  # SUB Vx, Vy, Vx = Vx - Vy, VF = NOT borrow (Vx > Vy)
_8xy6 = 0x6  # SHR Vx, Vy, VF = 1 if LSB of Vx = 1 (so VF = LSB(Vx))
# 1.) Vx = Vy = Vy >> 1
# 2.) Vx = Vx >> 1
_8xy7 = 0x7  # SUBN Vx, Vy, Vx = Vy - Vx, Vf = NOT borrow (Vy > Vx)
_8xyE = 0xE  # SHL Vx, Vy, VF = MSB(Vx) Vx = Vx << 1 or Vx = Vy = Vy << 1

_9xy0 = 0x9  # SNE Vx, Vy
Annn = 0xA   # LD I, addr: I = nnn
Bnnn = 0xb   # JP V0, addr: jump to V0 + nnn
Cxnn = 0xC   # RND Vx, byte: Vx = randByte AND nn
# DRW Vx, Vy, nibble: display n-byte sprite starting at mem. location I at (Vx, Vy), VF = collision
Dxyn = 0xD

Ex9E = 0x9E  # SKP Vx: Skip next instruction if key @ Vx is pressed
ExA1 = 0xA1  # SKNP Vx: '' not pressed

Fx07 = 0x07  # LD Vx, DT: Set Vx to delay-timer value
Fx0A = 0x0A  # LD Vx, K: wait for key press, store key value in Vx
Fx15 = 0x15  # LD DT, Vx: Set delay-timer = Vx
Fx18 = 0x18  # LD ST, Vx: Set sound-timer = Vx
Fx1E = 0x1E  # ADD I, Vx: I = I + Vx
Fx29 = 0x29  # LD F, Vx: I = location of sprite for digit Vx
# LD B, Vx: Store BCD representation at I, I+1, I+2: (i.e 123 => I = 1, I+1 = 2, I+2 = 3)
Fx33 = 0x33
Fx55 = 0x55  # LD [I], Vx: Store V0-Vx in memory starting at I
Fx65 = 0x65  # LD Vx, [I]: Read V0-Vx from memory stariting at I
