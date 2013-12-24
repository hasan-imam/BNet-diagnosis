from bnetbase import *

###############################################################################
# Problem domain: Grand mal seizure detection
###############################################################################

## Variables
# Genetic/hereditary biases towards disease
GB = Variable('Genetic_Bias', ['Present', 'Absent'])
# Anorexic patient
AN = Variable('Anorexic', [True, False])
# Presence of medicine that causes chemical imbalance in blood
MD = Variable('Medicine', ['Present', 'Absent'])
# Blood vessel malformation
BV = Variable('BV_Malformation', ['Present', 'Absent'])
# Blood quality (based on electrolyte and glucose balance)
BQ = Variable('Blood', ['Optimal', 'Imbalanced'])
# Tumor found
TM = Variable('Tumors', [True, False])
# Previous brain trauma
TR = Variable('Trauma', [True, False])
# Error in EMG
ER = Variable('Error_EMG', ['10%', '25%+'])
# Error in EEG
NS = Variable('Error_EEG', ['10%', '25%+'])
# Grand mal seizure taking place
SE = Variable('Sezure', [True, False])
# Amplitude of EEG signal
EEG_AMP = Variable('EEG_Amp', ['~150', '1000+'])
# Periodicity in EEG signal
EEG_SIG = Variable('EEG_Period', ['Periodic', 'Aperiodic'])
# EMG signal (muscle activation) features
EMG = Variable('EMG', ['Periodic_convulsion', 'Normal', 'Sustained_contraction'])

## Factors
# Probability tables
FGB = Factor('P(GB)', [GB])
FAN = Factor('P(AN)', [AN])
FMD = Factor('P(MD)', [MD])
FTR = Factor('P(TR)', [TR])
FER = Factor('P(ER)', [ER])
FNS = Factor('P(NS)', [NS])
# Conditional probability tables
FBV = Factor('P(BV|GB)', [BV, GB])
FTM = Factor('P(TM|GB,BV)', [TM, BV, GB])
FBQ = Factor('P(BQ|AN,MD)', [BQ, AN, MD])
FAMP = Factor('P(EEG_AMP|SE,NS)', [EEG_AMP, SE, NS])
FSIG = Factor('P(EEG_SIG|SE,NS)', [EEG_SIG, SE, NS])
FEMG = Factor('P(EMG|SE,ER)', [EMG, SE, ER])
FSE = Factor('P(SE|TM,TR,BQ)', [SE, TM, TR, BQ])

## Initialize factors 
# Probability tables
FGB.add_values([['Present',0.1], ['Absent', 0.9]])
FAN.add_values([[True,0.1], [False, 0.9]])
FMD.add_values([['Present',0.2], ['Absent', 0.8]])
FTR.add_values([[True,0.1], [False, 0.9]])
FER.add_values([['10%',0.8], ['25%+', 0.2]])
FNS.add_values([['10%',0.8], ['25%+', 0.2]])
# Conditional probability tables
FBV.add_values([['Present', 'Present', 0.6], ['Present', 'Absent', 0.5], 
                ['Absent', 'Present', 0.4], ['Absent', 'Absent', 0.5]])
FTM.add_values([[True, 'Present', 'Present', 0.7], [True, 'Present', 'Absent', 0.6], 
                [True, 'Absent', 'Present', 0.7],[True, 'Absent', 'Absent', 0.4],
               [False, 'Present', 'Present', 0.3], [False, 'Present', 'Absent', 0.4], 
                [False, 'Absent', 'Present', 0.3],[False, 'Absent', 'Absent', 0.6]])
FBQ.add_values([['Optimal', True, 'Present', 0.1], ['Optimal', True, 'Absent', 0.3], 
                ['Optimal', False, 'Present', 0.3],['Optimal', False, 'Absent', 0.8],
               ['Imbalanced', True, 'Present', 0.9], ['Imbalanced', True, 'Absent', 0.7], 
                ['Imbalanced', False, 'Present', 0.7],['Imbalanced', False, 'Absent', 0.2]])
FAMP.add_values([['~150', True, '10%', 0], ['~150', True, '25%+', 0.1], 
                ['~150', False, '10%', 1],['~150', False, '25%+', 0.7],
               ['1000+', True, '10%', 1], ['1000+', True, '25%+', 0.9], 
                ['1000+', False, '10%', 0],['1000+', False, '25%+', 0.3]])
FSIG.add_values([['Periodic', True, '10%', 0], ['Periodic', True, '25%+', 0.3], 
                ['Periodic', False, '10%', 0.9],['Periodic', False, '25%+', 0.1],
               ['Aperiodic', True, '10%', 1], ['Aperiodic', True, '25%+', 0.7], 
                ['Aperiodic', False, '10%', 0.1],['Aperiodic', False, '25%+', 0.9]])
FEMG.add_values([['Periodic_convulsion', True, '10%', 0.6], ['Periodic_convulsion', True, '25%+', 0.5], 
                ['Periodic_convulsion', False, '10%', 0.2], ['Periodic_convulsion', False, '25%+', 0.3],
               ['Normal', True, '10%', 0],                  ['Normal', True, '25%+', 0.1], 
                ['Normal', False, '10%', 0.6],              ['Normal', False, '25%+', 0.5],
               ['Sustained_contraction', True, '10%', 0.4], ['Sustained_contraction', True, '25%+', 0.4], 
                ['Sustained_contraction', False, '10%', 0.2],['Sustained_contraction', False, '25%+', 0.2]])
FSE.add_values([[True, True, True, 'Optimal', 0.7],      [True, True, False, 'Optimal', 0.5], 
                [True, False, True, 'Optimal', 0.5],     [True, False, False, 'Optimal', 0.3],
                [True, True, True, 'Imbalanced', 0.85],   [True, True, False, 'Imbalanced', 0.7], 
                [True, False, True, 'Imbalanced', 0.8],  [True, False, False, 'Imbalanced', 0.7],
               [False, True, True, 'Optimal', 0.3],      [False, True, False, 'Optimal', 0.5], 
                [False, False, True, 'Optimal', 0.5],    [False, False, False, 'Optimal', 0.7],
                [False, True, True, 'Imbalanced', 0.15],  [False, True, False, 'Imbalanced', 0.3], 
                [False, False, True, 'Imbalanced', 0.2], [False, False, False, 'Imbalanced', 0.3]])

## Create Bayes Net representation
bn = BN('SampleQ2', [GB,AN,MD,TR,ER,NS,BV,TM,BQ,EEG_AMP,EEG_SIG,EMG,SE], [FGB,FAN,FMD,FTR,FER,FNS,FBV,FTM,FBQ,FAMP,FSIG,FEMG,FSE])

## Tests
print '.:: RUNNING SMAPLE DIAGNOSIS ::.\n'

# Test: 1
print '1. Does knowing blood quality makes seizure independent of presence of aneroxia?'
print '-----------------------------------------------------------------------'
BQ.set_evidence('Optimal')
AN.set_evidence(True)
distribution = VE(bn, SE, [BQ,AN], min_fill_ordering)
print 'Distribution(SE|Optimal, Anorexic): ', distribution
AN.set_evidence(False)
distribution = VE(bn, SE, [BQ,AN], min_fill_ordering)
print 'Distribution(SE|Optimal, Not anorexic): ', distribution
AN.set_evidence(True)
distribution = VE(bn, SE, [AN], min_fill_ordering)
print 'Distribution(SE|Anorexic): ', distribution
AN.set_evidence(False)
distribution = VE(bn, SE, [AN], min_fill_ordering)
print 'Distribution(SE|Not anorexic): ', distribution
print '-----------------------------------------------------------------------\n'

# Test: 2
print '2. Does knowing GM makes EEG_AMP independent of TM and TR?'
print '-----------------------------------------------------------------------'
TM.set_evidence(True)
TR.set_evidence(True)
SE.set_evidence(True)
distribution = VE(bn, EEG_AMP, [TM,TR,SE], min_fill_ordering)
print 'Distribution(EEG_AMP|tumor, trauma, seizure): ', distribution
TM.set_evidence(False)
TR.set_evidence(True)
SE.set_evidence(True)
distribution = VE(bn, EEG_AMP, [TM,TR,SE], min_fill_ordering)
print 'Distribution(EEG_AMP|-tumor, trauma, seizure): ', distribution
TM.set_evidence(True)
TR.set_evidence(False)
SE.set_evidence(True)
distribution = VE(bn, EEG_AMP, [TM,TR,SE], min_fill_ordering)
print 'Distribution(EEG_AMP|tumor, -trauma, seizure): ', distribution
TM.set_evidence(True)
TR.set_evidence(True)
distribution = VE(bn, EEG_AMP, [TM,TR], min_fill_ordering)
print 'Distribution(EEG_AMP|tumor, trauma): ', distribution
TM.set_evidence(False)
TR.set_evidence(True)
distribution = VE(bn, EEG_AMP, [TM,TR], min_fill_ordering)
print 'Distribution(EEG_AMP|-tumor, trauma): ', distribution
TM.set_evidence(True)
TR.set_evidence(False)
SE.set_evidence(True)
distribution = VE(bn, EEG_AMP, [TM,TR], min_fill_ordering)
print 'Distribution(EEG_AMP|tumor, -trauma): ', distribution
print '-----------------------------------------------------------------------\n'

# Test: 3
print '3. Given SE, does BQ explain away TM?'
print '-----------------------------------------------------------------------'
SE.set_evidence(True)
BQ.set_evidence('Optimal')
distribution = VE(bn, TM, [SE, BQ], min_fill_ordering)
print 'Distribution(Trauma|seizure, optimal): ', distribution
SE.set_evidence(True)
BQ.set_evidence('Imbalanced')
distribution = VE(bn, TM, [SE, BQ], min_fill_ordering)
print 'Distribution(Trauma|seizure, imbalanced): ', distribution
print '-----------------------------------------------------------------------\n'

# Test: 4
print '4. Given BQ, does MD explain away AN?'
print '-----------------------------------------------------------------------'
MD.set_evidence('Present')
BQ.set_evidence('Imbalanced')
distribution = VE(bn, AN, [MD, BQ], min_fill_ordering)
print 'Distribution(Anorexia | blood neutrient imbalance, MD present): ', distribution
MD.set_evidence('Absent')
BQ.set_evidence('Imbalanced')
distribution = VE(bn, AN, [MD, BQ], min_fill_ordering)
print 'Distribution(Anorexia | blood neutrient imbalance, MD absent): ', distribution
distribution = VE(bn, AN, [], min_fill_ordering)
print 'Distribution(Anorexia): ', distribution
print '-----------------------------------------------------------------------\n'

# Test: 5
print """5. A patient is not anorexic but has medicine that causes 
chemical imbalance in blood. He also has brain trauma, but no one in his 
family had seizure (GB, the genetic bias towards seizure, is absent). Given 
this patient history what is the probability of him having seizure?"""
print '-----------------------------------------------------------------------'
AN.set_evidence(False)
MD.set_evidence('Present')
TR.set_evidence(True)
GB.set_evidence('Absent')
distribution = VE(bn, SE, [AN, MD, TR, GB], min_fill_ordering)
print 'Distribution(Seizure | patient history): ', distribution
print '-----------------------------------------------------------------------\n'

# Test: 6
print """6. We observe periodicity in EEG signal (EEG_SIG = periodic) and periodic 
muscle convulsion (EMG = periodic_convulsion). But both EEG and EMG measurements 
can be off by 25% or more. What is the probability that the patient is having 
seizure?"""
print '-----------------------------------------------------------------------'
EEG_SIG.set_evidence('Periodic')
EMG.set_evidence('Periodic_convulsion')
NS.set_evidence('25%+')
ER.set_evidence('25%+')
distribution = VE(bn, SE, [EEG_SIG, NS, EMG, ER], min_fill_ordering)
print 'Distribution(Seizure | measurable evidence, errors in measurement): ', distribution
print '-----------------------------------------------------------------------\n'
