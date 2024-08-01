# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 19:43:19 2023

@author: Jake
"""

import random
import opcodes
import binascii

class CPU:
    def __init__(self):
        self.V = [0 for i in range(0x10)]  # registers V0-VF
        # 4096 bytes of memory
        # 0x000 - 0x1FF: CHIP-8 interpretor
        # 0x050 - 0x0A0: 0-F characters
        # 0x200 - 0xFFF: ROM/program instructions
        self.memory = [0 for i in range(0x1000)]
        self.I = 0x0000  # 16-bit index register
        self.PC = 0x0200  # 16-bit program counter
        self.STACK = [0 for i in range(0x10)]  # Stack to hold PC values
        self.SP = 0x00  # Stack pointer
        self.OPCODE = 0x00
        self.DT = 0x00  # Delay timer
        self.ST = 0x00  # Sound timer
        self.ScreenBuffer = [0 for i in range(64 * 32)]
        self.CycleCount = 0
        self.LoadFonts()
    
    def LoadProgram(self, program):
        for i, byte in enumerate(program):
            self.memory[i + 0x0200] = byte
            # print(hex(byte))
    
    def LoadFonts(self):
        fontset = [
                0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
                0x20, 0x60, 0x20, 0x20, 0x70, # 1
                0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
                0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
                0x90, 0x90, 0xF0, 0x10, 0x10, # 4
                0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
                0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
                0xF0, 0x10, 0x20, 0x40, 0x40, # 7
                0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
                0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
                0xF0, 0x90, 0xF0, 0x90, 0x90, # A
                0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
                0xF0, 0x80, 0x80, 0x80, 0xF0, # C
                0xE0, 0x90, 0x90, 0x90, 0xE0, # D
                0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
                0xF0, 0x80, 0xF0, 0x80, 0x80  # F
            ]
        for i, byte in enumerate(fontset):
            self.memory[i + 0x50] = byte

    def Cycle(self):
        self.CycleCount += 1
        opcode = (self.memory[self.PC] << 0x8) | self.memory[self.PC + 1]  # Fetch
        self.OPCODE = opcode
        # print(hex(self.memory[self.PC]))
        # print(hex(self.memory[self.PC + 1]))
        self.PC += 2
        # print(self.PC)
        # print(hex(opcode))
        print(hex(opcode))
        match opcode >> 0xC: # Shift 3 nibbles = 3 * 4 = 12 = 0xC
            case 0:
                match opcode & 0xF:
                    case opcodes.CLS:
                        print("CLS")
                    case opcodes.RET:
                        print("RET")
                        self.SP -= 1
                        self.PC = self.STACK[self.SP]
                    case _: raise ValueError(f"Invalid opcode {opcode}")
            case opcodes._1nnn:
                print("1nnn, JMP")
                self.PC = opcode & 0x0FFF
            case opcodes._2nnn:
                print("2nnn, CALL")
                self.STACK[self.SP] = self.PC
                self.SP += 1
                self.PC = opcode & 0xFFF
            case opcodes._3xkk:
                print("3xkk, SE")
                x = (opcode & 0x0F00) >> 0x8 #shift one byte
                if self.V[x] == opcode & 0xFF:
                    self.PC += 2
            case opcodes._4xkk:
                print("4xkk, SNE")
                x = (opcode & 0x0F00) >> 0x8 #shift one byte
                if self.V[x] != opcode & 0xFF:
                    self.PC += 2
            case opcodes._5xy0:
                print("5xy0, SE")
                x = (opcode & 0x0F00) >> 0x8
                y = (opcode & 0x00F0) >> 0x4
                if self.V[x] == self.V[y]:
                    self.PC += 2
            case opcodes._6xkk:
                print("6xkk, LD")
                x = (opcode & 0x0F00) >> 0x8
                byte = opcode & 0xFF
                self.V[x] = byte
            case opcodes._7xkk:
                print("7xkk, ADD")
                x = (opcode & 0x0F00) >> 0x8
                byte = opcode & 0xFF
                sum = self.V[x] + byte
                self.V[0xF] = 1 if sum > 0xFF else 0
                self.V[x] = sum & 0xFF
            case 8:
                x = (opcode & 0x0F00) >> 0x8
                y = (opcode & 0x00F0) >> 0x4
                match opcode & 0xF:
                    case 0x0:
                        print("8xy0, LD")
                        self.V[x] = self.V[y]
                    case 0x1:
                        print("8xy1, OR")
                        self.V[x] = self.V[x] | self.V[y]
                    case 0x2: 
                        print("8xy2, AND")
                        self.V[x] = self.V[x] & self.V[y]
                    case 0x3: 
                        print("8xy3, XOR")
                        self.V[x] = self.V[x] ^ self.V[y]
                    case 0x4:
                        print("8xy4, ADD")
                        sum = self.V[x] + self.V[y]
                        self.V[0xF] = 1 if sum > 0xFF else 0
                        self.V[x] = sum & 0xFF
                    case 0x5:
                        print("8xy5, SUB")
                        self.V[0xF] = 1 if self.V[x] < self.V[y] else 0
                        self.V[x] = (self.V[x] - self.V[y]) & 0xFF
                    case 0x6:
                        print("8xy6, SHR")
                        self.V[0xF] = self.V[y] & 0x1
                        self.V[x] = (self.V[y] >> 1) & 0xFF
                    case 0x7:
                        print("8xy7, SUBN")
                        self.V[0xF] = 1 if self.V[x] > self.V[y] else 0
                        self.V[x] = (self.V[y] - self.V[x]) & 0xFF
                    case 0xE:
                        print("SHL")
                        self.V[0xF] = self.V[y] >> 0xF  # Get MSB
                        self.V[x] = (self.V[y] << 1) & 0xFF
                    case _: raise ValueError(f"Invalid opcode {opcode}")
            case opcodes._9xy0:
                print("9xy0, SNE")
                x = (opcode & 0x0F00) >> 0x8
                y = (opcode & 0x00F0) >> 0x4
                if self.V[x] != self.V[y]:
                    self.PC += 2
            case opcodes.Annn:
                print("Annn, LD I")
                self.I = opcode & 0x0FFF
            case opcodes.Bnnn:
                print("Bnnn, JP")
                self.PC = (opcode & 0xFFF) + self.V[0]
            case opcodes.Cxnn:
                print("Cxnn, RND")
                x = (opcode & 0x0F00) >> 8
                byte = opcode & 0xFF
                self.V[x] = random.randint(0, 0xFF) & byte
            case opcodes.Dxyn:
                print("Dxyn, DRW")
                x = (opcode & 0x0F00) >> 0x8
                y = (opcode & 0x00F0) >> 0x4
                n = opcode & 0x000F
                did_pix_turn_off = False
                for i in range(n):
                    for j in range(8):
                        spritePix = (self.memory[self.I + i] >> (7 - j)) & 0x1 #(self.memory[self.I + n] & 0x1 << j) >> j
                        screenIdx = self.V[x] + j + (self.V[y] + i) * 64
                        before = self.ScreenBuffer[screenIdx]
                        self.ScreenBuffer[screenIdx] ^= spritePix
                        after = self.ScreenBuffer[screenIdx]
                        if before == 1 and after == 0:
                            did_pix_turn_off = True
                if did_pix_turn_off:
                    self.V[0xF] = 1
            case 0xE:
                match opcode & 0xFF:
                    case opcodes.Ex9E:
                        print("Ex9E, SKP key")
                    case opcodes.ExA1:
                        print("ExA1, SKNP")
                    case _: raise ValueError(f"Invalid opcode {opcode}")
            case 0xF:
                x = (opcode & 0x0F00) >> 0x8
                match opcode & 0xFF:
                    case opcodes.Fx07:
                        print("Fx07, LD Vx <- DT")
                        self.V[x] = self.DT
                    case opcodes.Fx0A:
                        print("Fx0A, LD Vx <- K")
                    case opcodes.Fx15:
                        print("Fx15, LD DT <- Vx")
                        self.DT = self.V[x]
                    case opcodes.Fx18:
                        print("Fx18, LD ST <- Vx")
                        self.ST = self.V[x]
                    case opcodes.Fx1E:
                        print("Fx1E, ADD I, Vx")
                        self.I += self.V[x]
                    case opcodes.Fx29:
                        print("Fx29, LD F, Vx")
                    case opcodes.Fx33:
                        print("Fx33, store BCD")
                        num = self.V[x]
                        self.memory[self.I + 2] = num % 10
                        num = num // 10
                        self.memory[self.I + 1] = num % 10
                        self.memory[self.I] = num = num // 10
                    case opcodes.Fx55:
                        print("Fx55, LD [I], Vx")
                        for i in range(x + 1):
                            self.memory[self.I + i] = self.V[i]
                        self.I += x + 1
                    case opcodes.Fx65:
                        print("Fx65, LD Vx, [I]")
                        for i in range(x + 1):
                            self.V[i] = self.memory[self.I + i]
                        self.I += x + 1
                    case _: raise ValueError(f"Invalid opcode {opcode}")
