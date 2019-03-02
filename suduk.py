# -*- coding: cp936 -*-
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
#得到的是各个方块的位置表示的集合；
#类比于是Excel表格的排布，9行，9列，9个小九宫格的集合
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
#得到一个大数组，结果是：[[],[],[]...],一共是9+9+9，共27个小数组，每个数组代表一个单元，即一列或一行或一个小九宫格。
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)
#遍历一个方阵，得到每一个元素与其所对应的单元组成的键值对；
#得到一个字典，键是81个方块的位置表示，值是所对应的3个单元的所有方块，
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)
#sum 函数将字典的一个key所对应的value（即一个数组，里面是三个数组）中的所有项进行加
#利用set函数，去掉重复值，并再减去key本身


#这个函数是将初始数独带入，基本上能对很多方格进行赋值或者说排除数字
#从这里开始执行解数独的过程
def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)#value 代表一个字典
    for s,d in grid_values(grid).items():#这里讲初始数独表示成字典，并遍历items
        if d in digits and not assign(values, s, d):#对方格执行进行赋值，赋值前先判断该方格数字是否确定
            return False ## (Fail if we can't assign d to square s.)
    return values

 
#grid 是一个字符串，是一个数独的原始表达，这个字符串中可能有换行符
#将grid表示为一个字典，这个字典是初始的数独，某些方格是数字是确定的，其他是不确定的
def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))#分配，一个方格对应一个grid中的数字

 #该函数是用来赋值，就是已经确定方格s中的数字是d了，将d外的所有数字从方格中删除
 #等于是间接赋值，并且利用eliminate函数进行删除数字
def assign(values,s,d):
#这里value代表一个方阵字典，s是一个方格，d是一个数字，也就是说确定这个方格就是这个数字
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values,except return False if a contradiction is detected."""
    other_values = values[s].replace(d,'')#将key对应数字d外要从该方格s排除的其余数字赋给这个变量
    if all(eliminate(values,s,d2) for d2 in other_values):#依次删除要赋值给方格s的数字d外的所有数字
        return values
    else:
        return False

 #直接执行删除数字的功能，主要是靠replace方法来执行
 #并且对删除一个数字后的结果分情况讨论
 #可能方格内只剩下一个数字，需要将该数字从peers中删除，即调用自身
 #在方格内删除数字d，有可能在一个单元中剩余的方格中只有一个方格可以放这个数字d，则放入
def eliminate(values,s,d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values,except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')#对某个key 删除一个数字d
    ## (1) If a square s is reduced to one value d2,then eliminate d2 from the peers.
    if len(values[s]) ==0 :
        return False ##Contradiction:removed last value
    elif len(values[s]) == 1 :
        d2 = values[s]
        if not all(eliminate(values,s2,d2) for s2 in peers[s]):#将某个位置只剩下的那个数字来排除peers中的方格
            return False
    ##(2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:#没看懂
    #这里units是一个字典，一个方格对应其单元，
    #依次遍历该方格的单元u
    #此时方格s内已经将数字d删除
        dplaces = [s for s in u if d in values[s]]
        #这里的s跟上面传进来的参数s不是一个，是一个临时变量
        #得到一个单元中所有含有数字d的方格
        if len(dplaces) == 0:
            return False##Contradiction :no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values,dplaces[0],d):
                return False
        return values


#这个函数先不管，重要性不打
def display(values):
    "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols)
        if r in 'CF':
            print line

#该程序执行的开始            
def solve(grid):
    return search(parse_grid(grid))

#执行parse_grid函数后，可能会有部分方格的数字不能确定
#再用search函数进行排除
#会递归调用自己
def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):#利用函数all来判断是否所有的方格内的数字已唯一确定
        return values ##Solved!
        
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]),s) for s in squares if len(values[s]) > 1)#min函数内的形式应该是((),(),...)
    return some(search(assign(values.copy(),s,d)) for d in values[s])#依次带入方格内剩余的元素进行尝试排除
    #直到某依次尝试排除得到结果或者出错，不然递归调用自己。
    #注意这里是用副本进行尝试，这个现在还不知道具体怎么执行，再想想

    #利用some函数返回正确的那次尝试排除
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


#下面是main函数
display(grid_values(grid))
print '\n'
display(solve(grid))
    
