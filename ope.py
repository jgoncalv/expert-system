# Opérations And, OR, XOR..
# 0 = false, 1 = true, 2 = indeterminé

def m_and(match):
    x = match.groups()[0]
    y = match.groups()[1]
    if x == '0' or y == '0':
	    return '0'
    if x == '2' or y == '2':
	    return '2'
    if x == '1' and y == '1':
	    return '1'

def m_or(match):
    x = match.groups()[0]
    y = match.groups()[1]
    if x == '1' or y == '1':
	    return '1'
    if x == '2' or y == '2':
	    return '2'
    if x == '0' and y == '0':
	    return '0'

def m_xor(match):
    x = match.groups()[0]
    y = match.groups()[1]
    if (x == '1' and y == '1') or (x == '0' and y == '0'):
	    return '0'
    if x == '2' or y == '2':
	    return '2'
    if x == '1' or y == '1':
	    return '1'

def AND(x, y):
    if x == 0 or y == 0:
	    return 0
    if x == 2 or y == 2:
	    return 2
    if x == 1 and y == 1:
	    return 1

def OR(x, y):
    if x == 1 or y == 1:
        return 1
    if x == 2 or y == 2:
        return 2
    if x == 0 and y == 0:
        return 0

def XOR(x, y):
    if (x == 1 and y == 1) or (x == 0 and y == 0):
        return 0
    if x == 2 or y == 2:
        return 2
    if x == 1 or y == 1:
        return 1
