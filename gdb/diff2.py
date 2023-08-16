scemu = open('/tmp/scemu.log').read().strip().split('\n')
gdb = open('/tmp/gdb.log').read().strip().split('\n')

for i in range(len(scemu)):
    emu = scemu[i].split(' ')[2]

    print(f'{i+1}  {emu} {gdb[i]}')
    if emu != gdb[i]:
        break
