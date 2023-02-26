"""
Created on Tue Jan 31 19:30:58 2023

@author: Jake
"""

import CPU
import screen
import arcade
import time

cpu = CPU.CPU()

with open('./roms/test_opcode.ch8', 'rb') as f:
    content = f.read()
    cpu = CPU.CPU()
    cpu.LoadProgram(content)
    display = screen.Screen(20, 32, 64, cpu.ScreenBuffer)
    for i in range(5000):
        cpu.Cycle()
        if cpu.CycleCount % 100 == 0:
            display.updateScreen(cpu.ScreenBuffer)
            display.draw()
arcade.run()
# display.draw()
# time.sleep(5)
# cpu.ScreenBuffer[50] = 1
# cpu.ScreenBuffer[51] = 1
# cpu.ScreenBuffer[52] = 1
# cpu.ScreenBuffer[53] = 1
# cpu.ScreenBuffer[54] = 1
# cpu.ScreenBuffer[55] = 1
# display.updateScreen(cpu.ScreenBuffer)
# display.draw()
# arcade.run()