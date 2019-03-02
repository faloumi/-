# -*- coding: cp936 -*-
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
#�õ����Ǹ��������λ�ñ�ʾ�ļ��ϣ�
#�������Excel�����Ų���9�У�9�У�9��С�Ź���ļ���
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
#�õ�һ�������飬����ǣ�[[],[],[]...],һ����9+9+9����27��С���飬ÿ���������һ����Ԫ����һ�л�һ�л�һ��С�Ź���
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
#����һ�����󣬵õ�ÿһ��Ԫ����������Ӧ�ĵ�Ԫ��ɵļ�ֵ�ԣ�
#�õ�һ���ֵ䣬����81�������λ�ñ�ʾ��ֵ������Ӧ��3����Ԫ�����з��飬
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)
#sum �������ֵ��һ��key����Ӧ��value����һ�����飬�������������飩�е���������м�
#����set������ȥ���ظ�ֵ�����ټ�ȥkey����


#��������ǽ���ʼ�������룬�������ܶԺܶ෽����и�ֵ����˵�ų�����
#�����￪ʼִ�н������Ĺ���
def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)#value ����һ���ֵ�
    for s,d in grid_values(grid).items():#���ｲ��ʼ������ʾ���ֵ䣬������items
        if d in digits and not assign(values, s, d):#�Է���ִ�н��и�ֵ����ֵǰ���жϸ÷��������Ƿ�ȷ��
            return False ## (Fail if we can't assign d to square s.)
    return values

 
#grid ��һ���ַ�������һ��������ԭʼ������ַ����п����л��з�
#��grid��ʾΪһ���ֵ䣬����ֵ��ǳ�ʼ��������ĳЩ������������ȷ���ģ������ǲ�ȷ����
def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))#���䣬һ�������Ӧһ��grid�е�����

 #�ú�����������ֵ�������Ѿ�ȷ������s�е�������d�ˣ���d����������ִӷ�����ɾ��
 #�����Ǽ�Ӹ�ֵ����������eliminate��������ɾ������
def assign(values,s,d):
#����value����һ�������ֵ䣬s��һ������d��һ�����֣�Ҳ����˵ȷ�������������������
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values,except return False if a contradiction is detected."""
    other_values = values[s].replace(d,'')#��key��Ӧ����d��Ҫ�Ӹ÷���s�ų����������ָ����������
    if all(eliminate(values,s,d2) for d2 in other_values):#����ɾ��Ҫ��ֵ������s������d�����������
        return values
    else:
        return False

 #ֱ��ִ��ɾ�����ֵĹ��ܣ���Ҫ�ǿ�replace������ִ��
 #���Ҷ�ɾ��һ�����ֺ�Ľ�����������
 #���ܷ�����ֻʣ��һ�����֣���Ҫ�������ִ�peers��ɾ��������������
 #�ڷ�����ɾ������d���п�����һ����Ԫ��ʣ��ķ�����ֻ��һ��������Է��������d�������
def eliminate(values,s,d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values,except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')#��ĳ��key ɾ��һ������d
    ## (1) If a square s is reduced to one value d2,then eliminate d2 from the peers.
    if len(values[s]) ==0 :
        return False ##Contradiction:removed last value
    elif len(values[s]) == 1 :
        d2 = values[s]
        if not all(eliminate(values,s2,d2) for s2 in peers[s]):#��ĳ��λ��ֻʣ�µ��Ǹ��������ų�peers�еķ���
            return False
    ##(2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:#û����
    #����units��һ���ֵ䣬һ�������Ӧ�䵥Ԫ��
    #���α����÷���ĵ�Ԫu
    #��ʱ����s���Ѿ�������dɾ��
        dplaces = [s for s in u if d in values[s]]
        #�����s�����洫�����Ĳ���s����һ������һ����ʱ����
        #�õ�һ����Ԫ�����к�������d�ķ���
        if len(dplaces) == 0:
            return False##Contradiction :no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values,dplaces[0],d):
                return False
        return values


#��������Ȳ��ܣ���Ҫ�Բ���
def display(values):
    "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols)
        if r in 'CF':
            print line

#�ó���ִ�еĿ�ʼ            
def solve(grid):
    return search(parse_grid(grid))

#ִ��parse_grid�����󣬿��ܻ��в��ַ�������ֲ���ȷ��
#����search���������ų�
#��ݹ�����Լ�
def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):#���ú���all���ж��Ƿ����еķ����ڵ�������Ψһȷ��
        return values ##Solved!
        
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]),s) for s in squares if len(values[s]) > 1)#min�����ڵ���ʽӦ����((),(),...)
    return some(search(assign(values.copy(),s,d)) for d in values[s])#���δ��뷽����ʣ���Ԫ�ؽ��г����ų�
    #ֱ��ĳ���γ����ų��õ�������߳�����Ȼ�ݹ�����Լ���
    #ע���������ø������г��ԣ�������ڻ���֪��������ôִ�У�������

    #����some����������ȷ���Ǵγ����ų�
def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e:
            return e
    return False
                
grid = """
400000805
030000000
000700000
020000060
000080400
000010000
000603070
500200000
104000000"""                    


#������main����
display(grid_values(grid))
print '\n'
display(solve(grid))
    
