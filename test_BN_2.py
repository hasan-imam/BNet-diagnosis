from bnetbase import *

## Test Net # 2
# Source: http://cs.nyu.edu/faculty/davise/ai/bayesnet.html 

# Variables
A = Variable('A', ['a', '-a'])
B = Variable('B', ['b', '-b'])
C = Variable('C', ['c', '-c'])
D = Variable('D', ['d', '-d'])
E = Variable('E', ['e', '-e'])

# Factors
FA = Factor('P(A)', [A])
FB = Factor('P(B)', [B])

FC = Factor('P(C|A)', [C, A])
FD = Factor('P(D|A,B)', [D, A, B])
FE = Factor('P(E|C)', [E, C])

# Add values
FA.add_values([['a',0.3], ['-a', 0.7]])
FB.add_values([['b',0.6], ['-b', 0.4]])

FC.add_values([['c', 'a', 0.8], ['c', '-a', 0.4], ['-c', 'a', 0.2], ['-c', '-a', .6]])
FE.add_values([['e', 'c', 0.7], ['e', '-c', 0.2], ['-e', 'c', 0.3], ['-e', '-c', .8]])
FD.add_values([['d', 'a', 'b', 0.7], ['d', 'a', '-b', 0.8], ['d', '-a', 'b', 0.1],['d', '-a', '-b', 0.2],
               ['-d', 'a', 'b', 0.3], ['-d', 'a', '-b', 0.2], ['-d', '-a', 'b', 0.9],['-d', '-a', '-b', 0.8]])

# Create BN
testQ2 = BN('SampleQ2', [A,B,C,D,E], [FA,FB,FC,FD,FE])

# Tests
print '-----------------------------------------------------------------------'
distribution = VE(testQ2, D, [], min_fill_ordering)
print 'Distribution(D): ', distribution
print '-----------------------------------------------------------------------'
distribution = VE(testQ2, C, [], min_fill_ordering)
print 'Distribution(C): ', distribution
print '-----------------------------------------------------------------------'
C.set_evidence('c')
distribution = VE(testQ2, A, [C], min_fill_ordering)
print 'Distribution(A): ', distribution
print '-----------------------------------------------------------------------'
D.set_evidence('-d')
distribution = VE(testQ2, A, [D], min_fill_ordering)
print 'Distribution(A): ', distribution
print '-----------------------------------------------------------------------'
A.set_evidence('-a')
E.set_evidence('e')
distribution = VE(testQ2, C, [A, E], min_fill_ordering)
print 'Distribution(C): ', distribution
