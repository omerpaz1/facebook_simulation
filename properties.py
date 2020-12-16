

'''
helpful information, no need to to touch.

Users availables:
UserID            UserName
-------------------------

 2                 UserA
 3                 UserB
 4                 UserC
 5                 UserD
 6                 UserE

'''

'''
Parameters:
'''
#SNIR TEST
# total rounds for the simulation. can be in range [1,infinty]
total_rounds = 5
# number of LC Rounds.
LC = 5
# number of users that will be in the simulationץ can be in range [2,5]
Users_num = 2
# the agent user id can be in    ragne [2,6]
agent_id = 2 # if change the agent id -> run this in the init_simulator: init_users_free() 

adminUser = 1 # "omerpaz"

temp = 1

SL_Burden = -0.2
SL_PS = -0.1
UL_Burden = -0.7 
UL_PS = -1

# for score:
AF_COST = -0.3
OF_COST = -0.6 
SL_COST = SL_Burden + SL_PS
UL_COST = UL_Burden + UL_PS
NONE_COST = 0

site_path = "http://34.107.23.0/"