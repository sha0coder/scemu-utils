
skip_to = 21659
ignore_undefined_behaviours = [530,531]

def diffstr(s1, s2):
    diff = []
    ss1 = s1.split(' ')
    ss2 = s2.split(' ')
    prev = ''
    for i in range(len(ss1)):
        if ss1[i] != ss2[i]:
            diff.append(prev.strip()+' '+ss1[i].strip())
        prev = ss1[i]
    return diff


scemu = open('/tmp/scemu.log').read().strip().split('\n')
gdb = open('/tmp/gdb.log').read().strip().split('\n')

i = 0
j = 0
k = 0

while True:
    k += 1
    scemu_regs = scemu[i]
    scemu_regs2 = scemu[i+1]
    scemu_flags = scemu[i+2]
    #scemu_nemonic = scemu[i+3]
    i += 3 

    gdb_regs = gdb[j]
    gdb_regs2 = gdb[j+1]
    gdb_flags = gdb[j+2]
    gdb_nemonic = gdb[j+3]
    j += 5

    if k < skip_to:
        continue

    if k in ignore_undefined_behaviours:
        continue
    
    diff = diffstr(scemu_regs, gdb_regs)
    if diff:
        if diff[0] == 'rbx: 0x5100800':
            print('skip1')
            continue
        if diff[0] == 'rax: 0xf':
            print('skip2')
            continue
        if diff[0] == 'rax: 0x400':
            print('skip3')
            continue
        print(f'diff regs: {diff}')
    

    if scemu_regs != gdb_regs:
        print(f'ins {k} {gdb_nemonic}')
        print('scemu:')
        print(scemu_regs)
        print('gdb')
        print(gdb_regs)
        break


    diff = diffstr(scemu_regs2, gdb_regs2)
    if diff:
        print(f'diff regs2: {diff}')

    if scemu_regs2 != gdb_regs2:
        print(f'ins {k} {gdb_nemonic}')
        print('scemu:')
        print(scemu_regs2)
        print('gdb')
        print(gdb_regs2)
        break

    '''
    diff = diffstr(scemu_flags, gdb_flags)
    if diff:
        if diff[0] == 'af: true':
            continue
        if diff[0] == 'pf: true':
            continue
        print(f'diff flags: {diff}')


    if scemu_flags != gdb_flags: 
        print(f'ins {k} {gdb_nemonic}')
        print('scemu:')
        print(scemu_flags)
        print('gdb')
        print(gdb_flags)
        break
    '''




    
