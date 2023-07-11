'''
    gdb plugin that show info like  scemu -f ./elf64 -r 
    todo diffing with the scemu -r and detect bugs
'''

import ctypes
import gdb

class StepAndPrintRegisters(gdb.Command):
    def __init__(self):
        super().__init__("scemu", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        while True:
            self.print_registers()
            gdb.execute("stepi", to_string=True)

    def get_reg(self, regname):
        frame = gdb.selected_frame()
        reg = frame.read_register(regname)
        reg = reg.cast(gdb.lookup_type('long long'))
        if reg == -64:
            return hex(0xffffffffffffffc0)

        reg = ctypes.c_int64(reg).value

        if reg < 0:
            reg2 = (reg + (2 ** 64)) & 0xffffffffffffffff
        else:
            reg2 = reg

        return hex(reg2)


    def print_registers(self):
        frame = gdb.selected_frame()
        arch = frame.architecture()
        regs = arch.registers()

        rax = self.get_reg('rax')
        rbx = self.get_reg('rbx')
        rcx = self.get_reg('rcx')
        rdx = self.get_reg('rdx')
        rsi = self.get_reg('rsi')
        rdi = self.get_reg('rdi')
        rbp = self.get_reg('rbp')
        rsp = self.get_reg('rsp')

        r8 = self.get_reg('r8')
        r9 = self.get_reg('r9')
        r10 = self.get_reg('r10')
        r11 = self.get_reg('r11')
        r12 = self.get_reg('r12')
        r13 = self.get_reg('r13')
        r14 = self.get_reg('r14')
        r15 = self.get_reg('r15')


        fd = open('/tmp/gdb.log','a')
        fd.write(f"\trax: {rax} rbx: {rbx} rcx: {rcx} rdx: {rdx} rsi: {rsi} rdi: {rdi} rbp: {rbp} rsp: {rsp}\n")
        print(f"\trax: {rax} rbx: {rbx} rcx: {rcx} rdx: {rdx} rsi: {rsi} rdi: {rdi} rbp: {rbp} rsp: {rsp}")
        fd.write(f"\tr8: {r8} r9: {r9} r10: {r10} r11: {r11} r12: {r12} r13: {r13} r14: {r14} r15: {r15}\n")
        print(f"\tr8: {r8} r9: {r9} r10: {r10} r11: {r11} r12: {r12} r13: {r13} r14: {r14} r15: {r15}")
        #print(f"\tr8u: {r8u} r9u: {r9u} r10u: {r10u} r11u: {r11u} r12u: {r12u} r13u: {r13u} r14u: {r14u} r15u: {r15u}")
        #print(f"\tr8d: {r8d} r9d: {r9d} r10d: {r10d} r11d: {r11d} r12d: {r12d} r13d: {r13d} r14d: {r14d} r15d: {r15d}")
        #print(f"\tr8w: {r8w} r9w: {r9w} r10w: {r10w} r11w: {r11w} r12w: {r12w} r13w: {r13w} r14w: {r14w} r15w: {r15w}")
        #print(f"\tr8l: {r8l} r9l: {r9l} r10l: {r10l} r11l: {r11l} r12l: {r12l} r13l: {r13l} r14l: {r14l} r15l: {r15l}")

        cf_mask = 1 << 0
        pf_mask = 1 << 2
        af_mask = 1 << 4
        zf_mask = 1 << 6
        sf_mask = 1 << 7
        tf_mask = 1 << 8
        if_mask = 1 << 9
        df_mask = 1 << 10
        of_mask = 1 << 11
        nt_mask = 1 << 14
        eflags = frame.read_register('eflags')
        cf = str(bool(eflags & cf_mask)).lower()
        pf = str(bool(eflags & pf_mask)).lower()
        af = str(bool(eflags & af_mask)).lower()
        zf = str(bool(eflags & zf_mask)).lower()
        sf = str(bool(eflags & sf_mask)).lower()
        tf = str(bool(eflags & tf_mask)).lower()
        if_flag = str(bool(eflags & if_mask)).lower()
        df = str(bool(eflags & df_mask)).lower()
        of = str(bool(eflags & of_mask)).lower()
        nt = str(bool(eflags & nt_mask)).lower()

        fd.write(f"\tzf: {zf} pf: {pf} af: {af} of: {of} sf: {sf} df: {df} cf: {cf} tf: {tf} if: {if_flag} nt: {nt}\n")
        print(f"\tzf: {zf} pf: {pf} af: {af} of: {of} sf: {sf} df: {df} cf: {cf} tf: {tf} if: {if_flag} nt: {nt}")
        fd.close()
        #instruction = gdb.execute("x/i $pc", to_string=True)
        #print(instruction)






class GoToCommand(gdb.Command):
    "GDB command for executing n steps."

    def __init__(self):
        super(GoToCommand, self).__init__("goto", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        steps = int(arg.strip())
        for _ in range(steps):
            gdb.execute('stepi')

class Stepper(gdb.Command):
    def __init__(self):
        super().__init__("stepper", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        while True:
            gdb.execute("x/i $pc")
            gdb.execute("si", to_string=True)






#gdb.execute("set logging file /tmp/gdb.log")
#gdb.execute("set logging on")
gdb.execute("set pagination off")

GoToCommand()
StepAndPrintRegisters()
Stepper()



