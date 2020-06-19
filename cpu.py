import sys

# Opcodes for branch table
ADD = 0b10100000
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001

# Sprint Challenge
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100

# Stretch
ADDI = 0b001000  # Seems to be two bits short of others

# Stack Pointer
SP = 7


class CPU:
    """Simulates LS8 Hardware"""

    def __init__(self):
        """Initiate LS8 Componets and Opcode Branch Table"""

        self.pc = 0
        self.reg = [0] * 8  # Register
        self.ram = [0] * 256  # Memory
        self.fl = 0

        # A dictionary to call methode opperations
        self.branch_table = {
            ADD: self.add,
            HLT: self.halt,
            LDI: self.ldi,
            PRN: self.prn,
            MUL: self.multiply,
            POP: self.pop,
            PUSH: self.push,
            CALL: self.call,
            RET: self.ret,
            CMP: self.cmp,
            JNE: self.jne,
            JEQ: self.jeq,
            JMP: self.jmp,
            ADDI: self.addi
            }

    # Load program specified during startup
    def load(self, program):
        """Adds Instructions to Memory."""

        instructions = []
        with open(program) as f:
            for line in f:
                line = line.strip().split("#")  # Removing Text
                try:
                    num = int(line[0], 2)  # Grab Binary
                except ValueError:
                    continue  # For this operation ValueErrors are expected

                instructions.append(num)

        address = 0

        for instruction in instructions:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU Operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << 2
        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> 2
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    # Write and read to ram
    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    # Adds to values
    def add(self, op_a, op_b):
        self.reg[op_a] += self.reg[op_b]
        self.pc += 3

    # Ends the program
    def halt(self, op_a, op_b):
        sys.exit(0)

    # Sets a register to given value
    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        self.pc += 3

    # Prints adding process
    def prn(self, op_a, op_b):
        print(self.reg[op_a])
        self.pc += 2

    def multiply(self, op_a, op_b):
        self.reg[op_a] *= self.reg[op_b]
        self.pc += 3

    # Push and Pop is a stack implementation
    def push(self, op_a, op_b):
        self.reg[SP] -= 1
        self.ram_write(self.reg[op_a], self.reg[SP])
        self.pc += 2

    def pop(self, op_a, op_b):
        value = self.ram_read(self.reg[SP])
        self.reg[op_a] = value
        self.reg[SP] += 1
        self.pc += 2

    # Call and ret
    def call(self, op_a, op_b):
        self.reg[SP] -= 1
        self.ram_write(self.pc + 2, self.reg[SP])
        self.pc = self.reg[op_a]

    def ret(self, op_a, op_b):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1   

    # Sprint Challenge Methodes

    # Conditional Comparision
    def cmp(self, op_a, op_b):
        if self.reg[op_a] == self.reg[op_b]:
            self.fl = "E"
        elif self.reg[op_a] < self.reg[op_b]:
            self.fl = "LT"
        elif self.reg[op_a] > self.reg[op_b]:
            self.fl = "GT"
        self.pc += 3

    def jeq(self, op_a, op_b):
        if self.fl == "E":
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    # Jump instruction
    def jmp(self, op_a, op_b):
        self.pc = self.reg[op_a]

    def jne(self, op_a, op_b):
        if self.fl != "E":
            self.pc = self.reg[op_a]
        else:
            self.pc += 2

    # ADDs imediate value to register
    def addi(self, op_a, op_b):
        self.reg[op_a] += self.reg[op_b]
        # Don't have any test programes so unsure of pc jump and IV
        self.pc += 2

    # Run methode to handle processing of programes
    def run(self):
        """Run the CPU."""
        while True:

            # Grabing current code
            op_code = self.ram[self.pc]
            operand_a, operand_b = self.ram[self.pc + 1], self.ram[self.pc + 2]  # Fething operations

            # Checking Opcode in branch table
            if op_code in self.branch_table:
                self.branch_table[op_code](operand_a, operand_b)
