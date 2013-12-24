###############################################################################
# Classes
###############################################################################

'''Classes for variable elimination Routines 
   A) class Variable
      This class allows one to define Bayes Net variables.

      On initialization the variable object can be given a name and a
      domain of values. This list of domain values can be added to or
      deleted from to support incremental specification of the
      variable domain.

      The variable can be assigned a value. These assigned values are used
      by the factor class objects. It can also be given an evidence
      value. This is used when doing Variable Elimination. 


    B) class Factor

      This class allows one to define a factor specified by a table
      of values. 

      On initialization the variables the factor is over is
      specified. This must be a list of variables. This list of
      variables cannot be changed once the Factor object is
      created.

      Once created the factor can be incrementally initialized with a
      list of values which specify the factor's numeric value on 
      various assignments to the variables in its scope.
      
      There are two ways to set the factor's values:
      (a) a list of lists. Each list in this list specifies the
      value of each variable in the factor's scope followed by
      the numeric value for the factor on this sequence of variable
      values.
      (b) one can set the assigned value for every variable in the 
      factor's scope then add the number associated with that setting
      of its variables. 

      Getting the factor's values has two similar interfaces. 

      Initially, one creates a factor object for every conditional
      probability table (CPT) in the bayes-net. Then one initializes the
      factor with the specified values of these CPTs.


    C) class BN This class allows one to put factors and variables
       together to form a Bayes net.  It serves as a convenient place
       to store all of the factors and variables associated with a
       Bayes Net in one place.

    '''

class Variable:
    '''Class for defining Bayes Net variables. '''
    
    def __init__(self, name, domain=[]):
        '''Create a variable object, specifying its name (a
        string). Optionally specify the initial domain.
        '''
        self.name = name                #text name for variable
        self.dom = list(domain)         #Make a copy of passed domain
        self.evidence_index = 0         #evidence value (stored as index into self.dom)
        self.assignment_index = 0       #For use by factors. We can assign variables values
                                        #and these assigned values can be used by factors
                                        #to index into their tables.

    def add_domain_values(self, values):
        '''Add domain values to the domain. values should be a list.'''
        for val in values: self.dom.append(val)

    def value_index(self, value):
        '''Domain values need not be numbers, so return the index
           in the domain list of a variable value'''
        return self.dom.index(value)

    def domain_size(self):
        '''Return the size of the domain'''
        return(len(self.dom))

    def domain(self):
        '''return the variable domain'''
        return(list(self.dom))

    def set_evidence(self,val):
        '''set this variable's value when it operates as evidence'''
        self.evidence_index = self.value_index(val)

    def get_evidence(self):
        '''gets this variable's evidence vaalue'''
        return(self.dom[self.evidence_index])

    def set_assignment(self, val):
        '''Set this variable's assignment value for factor lookups'''
        self.assignment_index = self.value_index(val)

    def get_assignment(self):
        '''Get this variable's assignment value for factor lookups'''
        return(self.dom[self.assignment_index])

    ##These routines special low-level routines used directly by the
    ##factor objects
    def set_assignment_index(self, index):
        '''This routine is used by the factor objects'''
        self.assignment_index = index

    def get_assignment_index(self):
        '''This routine is used by the factor objects'''
        return(self.assignment_index)

    def __repr__(self):
        '''string to return when evaluating the object'''
        return("{}".format(self.name))
    
    def __str__(self):
        '''more elaborate string for printing'''
        return("{}, Dom = {}".format(self.name, self.dom))


class Factor: 
    '''Class for defining factors. A factor is a function that is over
    an ORDERED sequence of variables called its scope. It maps every
    assignment of values to these variables to a number. In a Bayes
    Net initially every CPT is represented as a factor. Pr(A|B,C) for
    example will be represented by a factor over the variables
    (A,B,C). If we assign A = a, B = b, and C = c, then the factor
    will map this assignment, A=a, B=b, C=c, to a number that is equal
    to Pr(A=a| B=b, C=c). During variable elimination, however, the
    factors we compute (when variables are eliminated) are no longer
    conditional probabilities. However, the factors still map
    assignments of values to the variables in their scope to numbers.

    Note that if the factor's scope is empty it is a constant factor
    that stores only one value. add_values would be passed something
    like [[0.25]] to set the factor's single value. The get_value
    functions will still work.  E.g., get_value([]) will return the
    factor's single value. Constant factors can be generated during
    variable elimination when a factor is restricted.'''

    def __init__(self, name, scope):
        '''create a Factor object, specify the Factor name (a string)
        and its scope (an ORDERED list of variable objects).'''
        self.scope = list(scope)
        self.name = name
        size = 1
        for v in scope:
            size = size * v.domain_size()
        self.values = [0]*size  #initialize values to be long list of zeros.

    def get_scope(self):
        return list(self.scope)

    def add_values(self, values):
        '''This routine can be used to initialize the factor. We pass
        it a list of lists. Each sublist is a ORDERED sequence of
        values, one for each variable in self.scope followed by a
        number that is the factor's value when its variables are
        assigned these values. For example, if self.scope = [A, B, C],
        and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], then we could pass add_values the
        following list of lists
        [[1, 'a', 'heavy', 0.25], [1, 'a', 'light', 1.90],
         [1, 'b', 'heavy', 0.50], [1, 'b', 'light', 0.80],
         [2, 'a', 'heavy', 0.75], [2, 'a', 'light', 0.45],
         [2, 'b', 'heavy', 0.99], [2, 'b', 'light', 2.25],
         [3, 'a', 'heavy', 0.90], [3, 'a', 'light', 0.111],
         [3, 'b', 'heavy', 0.01], [3, 'b', 'light', 0.1]]
         Note that these numbers need not be probabilities.

         This list initializes the factor so that, e.g., its value on
         (A=2,B=b,C='light) is 2.25'''

        for t in values:
            index = 0
            for v in self.scope:
                index = index * v.domain_size() + v.value_index(t[0])
                t = t[1:]
            self.values[index] = t[0]
         
    def add_value_at_current_assignment(self, number):
        '''This is a special purpose function for initializing a
        factor. We pass it only a single number. It then looks at the
        assigned values of the variables in its scope and initializes
        the factor to have that value on the current assignment of its
        variables. Hence, to use this function one first must set the
        assigned values of the variables in its scope.

        For example, if self.scope = [A, B, C], and A.domain() =
        [1,2,3], B.domain() = ['a', 'b'], and C.domain() = ['heavy',
        'light'], and we invoke A.set_assignment(1),
        B.set_assignment('a') and C.set_assignment('heavy'), then call
        this function with the value 0.33, we would have initialized
        this factor to have the value 0.33 on the assigments (A=1,
        B='1', C='heavy')'''

        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        self.values[index] = number

    def get_value(self, variable_values):
        '''This function is used to retrieve a value from the
        factor. We pass it an ordered list of values, one for every
        variable in self.scope. It then returns the factor's value on
        that set of assignments.  For example, if self.scope = [A, B,
        C], and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], and we invoke this function
        on the list [1, 'b', 'heavy'] we would get a return value
        equal to the value of this factor on the assignment (A=1,
        B='b', C='light')'''
        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.value_index(variable_values[0])
            variable_values = variable_values[1:]
        return self.values[index]

    def get_value_at_current_assignments(self):
        '''This function is used to retrieve a value from the
        factor. The value retrieved is the value of the factor when
        evaluated at the current assignment to the variables in its
        scope.

        For example, if self.scope = [A, B, C], and A.domain() =
        [1,2,3], B.domain() = ['a', 'b'], and C.domain() = ['heavy',
        'light'], and we had previously invoked A.set_assignment(1),
        B.set_assignment('a') and C.set_assignment('heavy'), then this
        function would return the value of the factor on the
        assigments (A=1, B='1', C='heavy')'''
        
        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        return self.values[index]

    def print_table(self):
        '''print the factor's table'''
        saved_values = []  #save and then restore the variable assigned values.
        for v in self.scope:
            saved_values.append(v.get_assignment_index())

        self.recursive_print_values(self.scope)

        for v in self.scope:
            v.set_assignment_index(saved_values[0])
            saved_values = saved_values[1:]
        
    def recursive_print_values(self, vars):
        if len(vars) == 0:
            print "[",
            for v in self.scope:
                print "{} = {},".format(v.name, v.get_assignment()),
            print "] = {}".format(self.get_value_at_current_assignments())
        else:
            for val in vars[0].domain():
                vars[0].set_assignment(val)
                self.recursive_print_values(vars[1:])

    def __repr__(self):
        return("{}({})".format(self.name, map(lambda x: x.name, self.scope)))
    
    def get_restricted_factor(self, restrictions):
        '''Apply restrictions (list of variables with evidence) to this factor 
        and return a copy of the restricted factor. The returned factor has 
        the same name, but reduced scope and values. The restriction variables  
        must have evidence values assigned.'''
        # Create new restricted factor
        new_scope = [var for var in self.get_scope() if var not in restrictions] 
        if new_scope:
            new_factor = Factor(generate_factor_name(new_scope), new_scope) 
        else:
            # Since scope is empty, add last restrictions to the factor's name
            new_factor = Factor('f'+str([x.name for x in restrictions]), new_scope) 
            
        # Generate list of possible assignments
        # where restricted variables only take the evidence values
        # and others take all values in their domains
        assignments = generate_assignments(self.get_scope(), restrictions, 'evidence')
            
        # Initialize values (apply restriction)
        # Use generated list of assignments to lookup values from this factor
        # and store them to the new factor
        restricted_indices = [self.scope.index(var) for var in restrictions]
        # Create the argument 'values' for add_values() call
        values = list()
        for assignment in assignments:
            # Keep the part of the assignment that is not in the restrictions
            value = [assignment[i] for i in range(0, len(assignment)) 
                     if i not in restricted_indices]
            value.append(self.get_value(assignment)) 
            values.append(value)
        # Add values to the new factor
        new_factor.add_values(values)
        return new_factor
        

class BN:
    '''Class for defining a Bayes Net.'''
    def __init__(self, name, Vars, Factors):
        self.name = name
        self.Variables = list(Vars)
        self.Factors = list(Factors)
        for f in self.Factors:
            for v in f.get_scope():     
                if not v in self.Variables:
                    print "Bayes net initialization error"
                    print "Factor scope {} has variable {} that",
                    print " does not appear in list of variables {}.".format(map(lambda x: x.name, f.get_scope()), v.name, map(lambda x: x.name, Vars))

    def factors(self):
        '''Return a new list of the factors. So we don't modify BN'''
        return list(self.Factors)

    def variables(self):
        return list(self.Variables)


###############################################################################
# Bayes Net functions
###############################################################################

def min_fill_ordering(Factors, QueryVar):
    '''Compute a min fill ordering given a list of factors. Return
    ordered list of variables from the scopes of the factors in
    Factors. The QueryVar will NOT be part of the returned ordering.
    The ordering is the min-fill ordering.'''
    scopes = []
    for f in Factors:
        scopes.append(list(f.get_scope()))
    Vars = []
    for s in scopes:
        for v in s:
            if not v in Vars and v != QueryVar:
                Vars.append(v)
    
    ordering = []
    while Vars:
        (var,new_scope) = min_fill_var(scopes,Vars)
        ordering.append(var)
        if var in Vars:
            Vars.remove(var)
        scopes = remove_var(var, new_scope, scopes)
    return ordering

def min_fill_var(scopes, Vars):
    '''Given a set of scopes (lists of lists of variables) compute and
    return the variable with minimum fill in. This is the variable that
    generates a factor of smallest scope when eliminated from the set
    of scopes. Also return the new scope generated from eliminating
    that variable.'''

    minv = Vars[0]
    (minfill,min_new_scope) = compute_fill(scopes,Vars[0])
    for v in Vars[1:]:
        (fill, new_scope) = compute_fill(scopes, v)
        if fill < minfill:
            minv = v
            minfill = fill
            min_new_scope = new_scope
    return (minv, min_new_scope)

def compute_fill(scopes, var):
    '''Return the fill in scope generated by eliminating var from
    scopes along with the size of this new scope'''
    union = []
    for s in scopes:
        if var in s:
            for v in s:
                if not v in union:
                    union.append(v)
    if var in union: union.remove(var)
    return (len(union), union)

def remove_var(var, new_scope, scopes):
    '''Return the new set of scopes that arise from eliminating var
    from scopes'''

    new_scopes = []
    for s in scopes:
        if not var in s:
            new_scopes.append(s)
    new_scopes.append(new_scope)
    return new_scopes
            

def VE(Net, QueryVar, EvidenceVars, orderingFn):
    '''
    Input: Net---a BN object (a Bayes Net)
           QueryVar---a Variable object (the variable whose distribution
                      we want to compute)
           EvidenceVars---a LIST of Variable objects. Each of these
                          variables has had its evidence set to a particular
                          value from its domain using set_evidence. 
           orderingFn---a FUNCTION that whose prototype is identical to
                        min_fill_ordering, i.e.:
                        order = orderingFn(Factors, QueryVar)
                        where Factors is a list of factor objects, and
                        QueryVar is a variable.
                        This function returns an ordered list 
                        of variables from the scopes of Factors (not
                        including QueryVar). VE will follow this
                        ordering when eliminating its variables. That is
                        VE will eliminate order[0] first then order[1] ...

                        NOTE you should first restrict the Net's factors
                        by the Evidence Variables (thus removing these
                        variables) before you compute an elimination 
                        ordering of the remaining variables.


    VE returns a distribution over the values of QueryVar, i.e., a list
    of numbers one for every value in QueryVar's domain. These numbers
    sum to one, and the i'th number is the probability that QueryVar is
    equal to its i'th value given the setting of the evidence
    variables. For example if QueryVar = A with Dom[A] = ['a', 'b',
    'c'], EvidenceVars = [B, C], and we have previously called
    B.set_evidence(1) and C.set_evidence('c'), then VE would return a
    list of three numbers. E.g. [0.5, 0.24, 0.26]. These numbers would
    mean that Pr(A='a'|B=1, C='c') = 0.5 Pr(A='a'|B=1, C='c') = 0.24
    Pr(A='a'|B=1, C='c') = 0.26
 
    '''

    ## Replace each factor f in F that mentions a variable(s) in EvidenceVars
    # with its restriction factor (this might yield a 'constant' factor)
    factors = list() # list to contain the factors after restriction step
    for factor in Net.factors():
        scope = factor.get_scope()
        if not scope:
            # Constrant factor. Nothing to restrict
            continue
        
        # Apply restriction, if needed
        restrictions = [var for var in scope if var in EvidenceVars]
        if restrictions:
            # Add restricted factor 
            factors.append(factor.get_restricted_factor(restrictions))
        else:
            # Add the original factor
            factors.append(factor)
    
    ## Get an ordering of variables for elimination
    order = orderingFn(factors, QueryVar)
    
    ## Eliminate variables in order
    for var in order:
        # Create list of factors that have 'var' in their scope
        prod_list = [f for f in factors if var in f.get_scope()]
        # Create product of factors, if needed
        product = None
        if len(prod_list) == 1:
            product = prod_list[0]
        elif len(prod_list) > 1:
            # Create a product factor
            product = create_product_factor(prod_list, var)
        else:
            continue
        # Eliminate var by summing
        summed = eliminate_var(product, var)
        # Eliminate factors containing var and add the summed factor
        factors = [x for x in factors if x not in prod_list] + [summed]
    
    ## Factor the factors containing QueryVar
    prod_list = [f for f in factors if QueryVar in f.get_scope()]
    f = create_product_factor(prod_list, QueryVar)
    factors = [x for x in factors if x not in prod_list] + [f]
    
    ## Normalize
    # Get normalization const
    n_const = 0
    assignments = generate_assignments(f.get_scope(), None)
    for a in assignments:
        n_const += f.get_value(a)
    # Set normalized values
    if (n_const != 1):
        for a in assignments:
            a.append(f.get_value(a)/n_const)
            f.add_values([a])
    
    if len(f.get_scope()) != 1:
        print 'Error in final factor. Scope: ', f.get_scope()
        exit(-1)
    else:
        distribution = [f.get_value(a) for a in generate_assignments(f.scope, None)]
        return distribution
    
def eliminate_var(factor, var):
    '''Eliminates the given var from the factor by summing.
    Returns a newe factor with var removed from its scope. 
    This operation might result in constant factor, where len(scope) is 0'''
    # Create new factor to contain the values after elimination
    new_scope = [x for x in factor.get_scope() if x is not var]
    new_factor = Factor(generate_factor_name(new_scope), new_scope)
    assignments = generate_assignments(new_scope, None)
    # Index of 'var' in factor's scope
    var_index = factor.get_scope().index(var)
    # Add values to new factor using the generated assignemnts
    for i in range(0, len(assignments)):
        # Get new assignment value by summing over all possible values
        # in var's domain 
        t = 0 
        for val in var.domain(): 
            a = assignments[i][0:var_index] + [val] + assignments[i][var_index:len(assignments)]
            t += factor.get_value(a) 
        # Concatenate the sum to the assignment so that it can be 
        # used to call new_factor.add_values()
        assignments[i].append(t)
    # Store the values in new_factor
    new_factor.add_values(assignments)
    return new_factor

def create_product_factor(factors, cvar):
    '''Returns a factor that is the product of the 'factors' given the 
    common variable 'cvar'
    ''' 
    # Create product using two factors at a time
    factor1 = factors[0]
    for factor2 in factors[1:]:
        factor1 = product_helper(factor1, factor2)
    return factor1
    
def product_helper(factor1, factor2): 
    '''Creates product of factor1 and factor2. 
    These factors can have one or many variables in common.'''
    # Create the product factor
    # Notice the ordering of the new_scope variables
    # This is crucial in the step where we set the values in the table
    new_scope = [var for var in factor1.get_scope()]
    new_scope = new_scope + [var for var in factor2.get_scope() if var not in factor1.get_scope()]
    product = Factor(factor1.name + '_x_' + factor2.name, new_scope)
    
    # List of variables that are common in both factors
    cvars = [var for var in factor1.get_scope() if var in factor2.get_scope()]
    # Create list of possible assignment combinations for the common variables
    restricted_assignments = generate_assignments(cvars, None) 
    
    # Add values to the new factor
    for ra in restricted_assignments:
        # Assign values from this restriction to the common vars
        for i in range(0,len(cvars)):
            cvars[i].set_assignment(ra[i])
        # Generate assignments for the given factors. 
        # These will be used to lookup values.
        assignments1 = generate_assignments(factor1.get_scope(), cvars, 'assignment')
        assignments2 = generate_assignments(factor2.get_scope(), cvars, 'assignment')
        # Calculate and add new values
        for a1 in assignments1:
            for a2 in assignments2:
                # Find indices of the common vars in factor 2
                common_indices2 = [factor2.scope.index(var) for var in cvars]
                value = None # Argument for product.add_values(*) call
                value = a1 + [a2[i] for i in range(0, len(a2)) if i not in common_indices2] 
                #value += [var for (i,var) in a2 if i not in common_indices2] 
                value += [factor1.get_value(a1) * factor2.get_value(a2)]
                product.add_values([value])
    return product  
    
def generate_assignments(scope, restrictions, source = 'evidence'): 
    '''Generate possible assignments of values given a scope (list of vars) and 
    restriction (list of vars) for some of the vars in the scope.
    source = {evidence, assignment}. This defines where to look for the value 
    in a restriction variable. By default, looks into evidence to find the 
    restricted value.
    If no restriction given then just generates all possible value combinations
    Returns list of lists containing assigned vales for each variable in the 
    scope (in order)
    '''
    # Generate list of possible assignments
    # where restricted variables only take the evidence values
    # while others take all values in their domains
    assignments = list()
    assignments.append([])
    for var in scope:
        new_assignments = list()
        while len(assignments) > 0:
            old_tuple = assignments.pop(0)
            if restrictions and var in restrictions:
                # If a restricted variable, 
                # generate just one assignment for it (the restriction)
                tmp = old_tuple[:]
                if source == 'evidence':
                    tmp.append(restrictions[restrictions.index(var)]
                           .get_evidence())
                else: 
                    tmp.append(restrictions[restrictions.index(var)]
                           .get_assignment())
                new_assignments.append(tmp)
            else:
                # Otherwise generate all possible assignments 
                # of this variable
                for val in var.domain():
                    tmp = old_tuple[:]
                    tmp.append(val)
                    new_assignments.append(tmp)
        assignments = new_assignments
    return assignments

def generate_factor_name(scope):
    '''Generates factor name from the list of scope variables'''
    return 'f' + str([x.name for x in scope])

