from bnetbase import *

## Test Net # 1
# Variables
A = Variable('A', ['a', '-a'])
B = Variable('B', ['b', '-b'])
C = Variable('C', ['c', '-c'])
D = Variable('D', ['d', '-d'])
E = Variable('E', ['e', '-e'])
F = Variable('F', ['f', '-f'])
G = Variable('G', ['g', '-g'])
H = Variable('H', ['h', '-h'])
I = Variable('I', ['i', '-i'])

# Factors
FA = Factor('P(A)', [A])
FH = Factor('P(H)', [H])
FG = Factor('P(G)', [G])
FF = Factor('P(F)', [F])

FB = Factor('P(B|A,H)', [B, A, H])
FC = Factor('P(C|B,G)', [C, B, G])
FD = Factor('P(D|C,F)', [D, C, F])
FE = Factor('P(E|C)', [E, C])
FI = Factor('P(I|B)', [I, B])

# Add values to factors
FA.add_values([['a',0.9], ['-a', 0.1]])
FF.add_values([['f',0.1], ['-f', 0.9]])
FG.add_values([['g',1], ['-g', 0]])
FH.add_values([['h',0.5], ['-h', 0.5]])

FB.add_values([['b', 'a', 'h', 1], ['b', 'a', '-h', 0], ['b', '-a', 'h', 0.5],['b', '-a', '-h', 0.6],
               ['-b', 'a', 'h', 0], ['-b', 'a', '-h', 1], ['-b', '-a', 'h', 0.5],['-b', '-a', '-h', 0.4]])
FC.add_values([['c', 'b', 'g', .9], ['c', 'b', '-g', .9], ['c', '-b', 'g', .1],['c', '-b', '-g', 1],
               ['-c', 'b', 'g', .1], ['-c', 'b', '-g', .1], ['-c', '-b', 'g', 0.9],['-c', '-b', '-g', 0]])
FD.add_values([['d', 'c', 'f', 0], ['d', 'c', '-f', 1], ['d', '-c', 'f', 0.7],['d', '-c', '-f', 0.2],
               ['-d', 'c', 'f', 1], ['-d', 'c', '-f', 0], ['-d', '-c', 'f', 0.3],['-d', '-c', '-f', 0.8]])

FE.add_values([['e', 'c', 0.2], ['e', '-c', 0.4], ['-e', 'c', 0.8], ['-e', '-c', .6]])
FI.add_values([['i', 'b', 0.3], ['i', '-b', 0.9], ['-i', 'b', 0.7], ['-i', '-b', .1]])

# Create BN
testQ1 = BN('SampleQ1', [A,B,C,D,E,F,G,H,I], [FA,FB,FC,FD,FE,FF,FG,FH,FI])

# Tests
# print generate_assignments(FB.get_scope(), None)
# 
# A.set_assignment('a')
# A.set_evidence('-a')
# print generate_assignments(FB.get_scope(), [A], 'assignment')
# print generate_assignments(FB.get_scope(), [A], 'evidence')
# print generate_assignments(FB.get_scope(), [A])
# 
# product = create_product_factor([FC, FI], None)
# print product.get_scope()

print '-----------------------------------------------------------------------'
A.set_evidence('a')
distribution = VE(testQ1, B, [A], min_fill_ordering)
print 'Distribution(B): ', distribution

print '-----------------------------------------------------------------------'
A.set_evidence('a')
distribution = VE(testQ1, C, [A], min_fill_ordering)
print 'Distribution(C): ', distribution

print '-----------------------------------------------------------------------'
A.set_evidence('a')
E.set_evidence('-e')
distribution = VE(testQ1, C, [A, E], min_fill_ordering)
print 'Distribution(C): ', distribution

print '-----------------------------------------------------------------------'
A.set_evidence('a')
F.set_evidence('-f')
distribution = VE(testQ1, C, [A, F], min_fill_ordering)
print 'Distribution(C): ', distribution

print 'done'

###############################################################################

