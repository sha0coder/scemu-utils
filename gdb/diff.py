
scemu = open('/tmp/scemu.log').read().strip().split('\n')
gdb = open('/tmp/gdb.log').read().strip().split('\n')

ins = 0

for i in range(len(scemu)):
    if 'rax' in scemu[i]:
        ins += 1

    if scemu[i] != gdb[i]:
        print(f'mismach on instruction {ins}')
        print('scemu:')
        print(scemu[i])
        print('gdb')
        print(gdb[i])
