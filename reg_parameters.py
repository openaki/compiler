# This file is used to edit the number of registers and there constraints
# Please use the variables (used in C code) as a key to the map.
# The value to the maps is a list of registers.
# The registers in the list follow a "and" condition


# Do not Delete
_optimization__never_go = {}
_optimization__always_go = {}
# Do not Delete

_optimization__REGS = 3  #Number of Registers

# The register number that a variable can not go into
#_optimization__never_go['a'] = [1, 2]
#_optimization__never_go['b'] = [0]

_optimization__always_go['a'] = [1]
 
