import time

def linesWith(lines, c, i):
    ret = []
    for line in lines:
        if line[i] == c:
            ret.append(line)
    return ret

def ogrPareDown(lines, i):
    if len(lines) == 1 and i <= len(lines[0]):
        return ogrPareDown(lines, i+1)
    if i >= len(lines[0]):
        return lines
    bitlist = [l[i] for l in lines]        
    if bitlist.count('0') > bitlist.count('1'):
        sublines = linesWith(lines, '0', i)
    else:
        sublines = linesWith(lines, '1', i)
    return ogrPareDown(sublines, i+1)
 
def co2PareDown(lines, i):
    if len(lines) == 1 and i <= len(lines[0]):
        return co2PareDown(lines, i+1)
    if i >= len(lines[0]):
        return lines
    bitlist = [l[i] for l in lines]        
    if bitlist.count('1') >= bitlist.count('0'):
        sublines = linesWith(lines, '0', i)
    else:
        sublines = linesWith(lines, '1', i)
    return co2PareDown(sublines, i+1)
    
   
for fname in ['input.txt', 'input2.txt']:
    with open(fname, 'r') as f:
        start = time.time()
        lines = [l.strip() for l in f.readlines()]
        ogr = ogrPareDown(lines, 0)
        co2 = co2PareDown(lines, 0)
        print(ogr)
        print(co2)
        ogr = int(''.join(ogr), base=2)
        co2 = int(''.join(co2), base=2)
        end = time.time()
        print('{} solution: {} took {} seconds'.format(fname, ogr*co2, end-start))

