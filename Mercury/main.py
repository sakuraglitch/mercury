import pygame
import numpy as np


class CPU:

    def __init__(self, memory):
        self.registers = {'A': 0, 'F': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'H': 0, 'L': 0}
        self.PC = 0x0  # Program Counter
        self.SP = 0xFFFE  # Stack Pointer
        self.memory = memory
        self.cycles = 0

    def fetch(self):
        opcode = self.memory.read_byte(self.PC)
        self.PC += 1
        return opcode

    def decode_execute(self, opcode):
        if opcode == 0x00:  # NOP
            self.cycles += 4
        elif opcode == 0x3E:  # LD A, n
            value = self.memory.read_byte(self.PC)
            self.PC += 1
            self.registers['A'] = value
            self.cycles += 8
        elif opcode == 0x06:  # LD B, n
            value = self.memory.read_byte(self.PC)
            self.PC += 1
            self.registers['B'] = value
            self.cycles += 8
        elif opcode == 0x0E:  # LD C, n
            value = self.memory.read_byte(self.PC)
            self.PC += 1
            self.registers['C'] = value
            self.cycles += 8
            # Implement other opcodes...
        else:
            self.handle_cb_prefix(opcode)  # Handle CB-prefixed opcodes

    def step(self):
        opcode = self.fetch()
        self.decode_execute(opcode)
        raise NotImplementedError(f"Opcode {opcode:02X} not implemented.")


class Memory:
    class Memory:
        def __init__(self, size=2 ** 21):  # Assuming 2MB max size for ROM
            self.memory = bytearray(size)

        def load_rom(self, rom_path):
            with open(rom_path, 'rb') as rom_file:
                rom_data = rom_file.read()

                rom_size = min(len(rom_data), len(self.memory))
                self.memory[:rom_size] = rom_data[:rom_size]

        def read_byte(self, address):
            return self.memory[address]

        def write_byte(self, address, value):
            self.memory[address] = value

        def load_rom(self, rom_path):
            with open(rom_path, 'rb') as rom_file:
                rom_data = rom_file.read()
                self.memory[:len(rom_data)] = list(rom_data)

class Display:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((160, 144))
        self.clock = pygame.time.Clock()

    def draw(self, buffer):
        for y in range(144):
            for x in range(160):
                color = buffer[y][x]
                self.screen.set_at((x, y), (color, color, color))
        pygame.display.flip()


class InputHandler:
    def __init__(self):
        self.keys = {
            pygame.K_RIGHT: 'RIGHT',
            pygame.K_LEFT: 'LEFT',
            pygame.K_UP: 'UP',
            pygame.K_DOWN: 'DOWN',
            pygame.K_z: 'A',
            pygame.K_x: 'B',
            pygame.K_RETURN: 'START',
            pygame.K_BACKSPACE: 'SELECT'
        }

    def handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        return {action: pressed_keys[key] for key, action in self.keys.items()}


def main(rom_path):
    memory = Memory()
    memory.load_rom(rom_path)
    cpu = CPU(memory)


display = Display()
input_handler = InputHandler()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fetch-Decode-Execute cycle
        CPU.step()

        # Update display
        buffer = np.zeros((144, 160), dtype=np.uint8)  # Dummy display buffer
        display.draw(buffer)

        # Handle input
        inputs = input_handler.handle_input()
        print(inputs)

        display.clock.tick(60)

if __name__ == "__main__":
    main('C:\\Users\\ronia\\Documents\\rom.gb')
