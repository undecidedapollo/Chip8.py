import CPU
import binascii

def load_program():
    cpu = CPU.CPU()
    program = [0x00, 0xE0, 0x00, 0xEE]
    cpu.LoadProgram(program)
    assert(cpu.PC == 0)
    cpu.Cycle()
    assert(cpu.OPCODE == 0x00E0)
    assert(cpu.PC == 2)
    cpu.Cycle()
    assert(cpu.OPCODE == 0x00EE)
    assert(cpu.PC == 0)
    print("load_program: pass")

# load_program()s

# print(hex(0x1234 >> 0xC))
# print(hex(0x8000 >> 0xD))

with open('test_opcode.ch8', 'rb') as f:
    content = f.read()
    print(binascii.hexlify(content))
    cpu = CPU.CPU()
    cpu.LoadProgram(content)
    for i in range(100):
        cpu.Cycle()
