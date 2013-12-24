BNet-diagnosis
==============

Simple bayes net program that contains:
 - bayes net implementation (with variable elimination with min fill ordering)
 - 3 test programs to test the bayes net implementation
 - a program where bayes net is used to calculate probability of seizure given evidence on some symptom and cause variables 

Seizure diagnosis using bayes net
=================
Epileptic seizure has many symptoms/causes. In this program, a simple causal model has been created using some simple causes and symptoms. Check out the model diagram to see the network. Read the seizure.py file where this model has been implemented. The code has been heavily commented and fairly straightforward. The program performs 6 sample tests using the model and prints out the queried probability distribution. 

##The Network
This network represents a model that can be used to detect or predict Grand Mal seizure in patients. 
It has variables that represent measurable signals/symptoms, patient history elements and some hidden internal nodes.

##Variables

Variables will be addressed in abbreviations. For full name, see the graph.
Also, there are variables that can be queries as well as evidences. In real life, just because we can test something, does not mean we can test it easily. Doctors usually calculate an initial posterior from patient history. If that posterior is high, then we do further tests (to get more evidences) and get a better posterior. So depending on the situation, some variables can be queries as well as evidences.

**GB:**

Patient’s genetic/hereditary biases towards having tumors and cell malformations.

Domain: {Present, Absent}

Type: Evidence (can get it from patient’s hereditary information/history or tests)

**AN:**

Is the patient anorexic? This variables has an effect on blood nutrient quality of patient. 

Domain: {True, False}

Type: Evidence (can get it from patient’s history or tests)

**MD:**

Presence of medicine in patient’s blood that causes chemical imbalance. 

Domain: {Present, Absent}

Type: Evidence (can get it from tests or looking into previous prescription)

**BV:**

Presence of blood vessel malformation in patient’s brain. This is one of the general causes of tumors.

Domain: {Present, Absent}

Type: Evidence (can detect from test), Query (since the test is expensive, we can also query on it given evidence about GB, which is a cause)

**BQ:**

Blood quality, which is a measure of how well balanced nutrients and electrolytes are in patient blood. Imbalance increases hyper activity of brain, making it more susceptible to seizure. 

Domain: {Optimal, Imbalanced}

Type: Evidence (can detect from test), Query.

**TM:**

Does patient have a brain tumor? 

Domain: {True, False}

Type: Evidence

**TR:**

Did patient suffer from head trauma in the past? 

Domain: {True, False}

Type: Evidence

**ER:**

Error in EMG signal measurement due to noise and other factors.

Domain: { 10%, 25%+}
Although there can be many other possible values (since the domain is continuous), only 2 were chose. ‘25%+’ means 25% or more error in the measured EMG signal.

Type: Evidence (can derive priors for these errors by doing tests on the machine)

**NS:**

Error in EEG signal measurement due to noise and other factors.

Domain: { 10%, 25%+}

Type: Evidence (can derive priors for these errors by doing tests on the machine)

**SE:**

Is the patient having seizure (at the moment) or is he susceptible to having seizure? 

Domain: {True, False}

Type: Query

**EEG_AMP:**

Peak EEG signal (recording of electrical activity along the scalp) amplitude measured in microvolts. This is naturally a continuous value, but has been made binary by choosing the two frequently seen values.

Domain: {~150, 1000+}. ~150 is seen in healthy brain, while 1000 or more is seen in pathologic conditions.

Type: Evidence

**EEG_SIG:**

Periodicity of EEG signal.

Domain: {Periodic, Aperiodic}. In general brainwave is asynchronous, but shows periodicity during seizure.

Type: Evidence

**EMG:**

This variable specifies EMG signal characteristics. EMG signal is the recording of electrical activities in skeletal muscles.

Domain: {'Periodic_convulsion', 'Normal', 'Sustained_contraction'}. These are the three noticeable features for our case. The first and last one are usually indicators of seizure. Normal means usual electrical activity.




##Seizure tests explained

*Note: Run seizure.py to see the test results presented here. Some of the evidence values in the result has been renamed (i.e. from True|False) to be make things more intuitive (i.e. Anorexic|Not anorexic)*

**(1) Does knowing BQ (blood quality) makes SE (seizure) independent of AN?)**

Test with BQ set to a certain evidence and changing evidence of AN. SE gives equal distribution in both cases:

> Distribution(SE|Optimal, Anorexic): [0.4240, 0.5760]

> Distribution(SE|Optimal, Not anorexic): [0.4240, 0.5760]

But if we don’t give any evidence about BQ, the distribution changes with AN evidence change:

> Distribution(SE|Anorexic): [0.6375, 0.3624]

> Distribution(SE|Not anorexic): [0.5106, 0.4894]

This is an example of a case where knowing knowing a fact can make another fact irrelevant.



**(2) Does knowing GM makes EEG_AMP independent of TM and TR?)**

Same as before, we can try with some combinations of evidences to see the effect:

> Distribution(EEG_AMP|tumor, trauma, seizure): [0.02, 0.98]

> Distribution(EEG_AMP|-tumor, trauma, seizure): [0.02, 0.98]

> Distribution(EEG_AMP|tumor, -trauma, seizure): [0.02, 0.98]

With same value for seizure (SE), different combinations of other evidences don’t matter. But without any SE evidence, we see changes in probabilities:

> Distribution(EEG_AMP|tumor, trauma): [0.2485, 0.7515]

> Distribution(EEG_AMP|!tumor, trauma): [0.3851, 0.6149]

> Distribution(EEG_AMP|tumor, !trauma): [0.4167, 0.5833]

(Similar phenomenon as seen in test #1)


**(3) Given SE, does BQ explain away TM?)**

If seizure (SE) happens and we know the blood quality (BQ) was optimal, there is higher (0.6377) chance that trauma was the reason.

> Distribution(Trauma|seizure, optimal): [0.6377, 0.3622]

But if we know blood quality was a imbalanced, trauma’s probability as the cause goes down (0.5217).

> Distribution(Trauma|seizure, imbalanced): [0.5217, 0.4782]

Here, knowing presence of one cause explains away another.



**(4) Given BQ (blood quality), does MD (medicine in blood) explain away AN (anorexia)?)**

> Distribution(Anorexia | blood nutrient imbalance, MD present): [0.125, 0.875

> Distribution(Anorexia | blood nutrient imbalance, MD absent): [0.280, 0.720]

If MD is present it explains away Anorexia (less probability of being anorexic (0.125)). But if MD is absent, probability of being anorexic goes up (0.280). As in test #3, we do not see dramatic changes since probability of anorexia itself is quite low. This has been made low based on statistics.

> Distribution(Anorexia): [0.1, 0.9]


**(5) A patient is not anorexic but has medicine that causes chemical imbalance in blood. He also has brain trauma, but no one in his family had seizure (GB, the genetic bias towards seizure, is absent). Given this patient history what is the probability of him having seizure?)**

The patient has higher chance of having seizure given his history.

> Distribution(Seizure | patient history): [0.7575, 0.2425]

This is a realistic example, where we only know the past history as the input.



**(6) We observe periodicity in EEG signal (EEG_SIG = periodic) and periodic muscle convulsion (EMG = periodic_convulsion). But both EEG and EMG measurements can be off by 25% or more. What is the probability that the patient is having seizure?)**

There should be higher probability that patient is having seizure at the time of measurement. 

> Distribution(Seizure | measurable evidence, errors in measurement): [0.8458, 0.1541]

This high value makes sense since we are observing signs from two independent sources, even though the measurement can be off. This is another realistic case, where medical equipment needs detect seizure from symptoms and call for help.
