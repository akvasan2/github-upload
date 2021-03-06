import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib
import grid_construction as Grid_Construct
import select_trajectories as Select
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
cmap="RdBu_r"

##############################################
######## Definition of parameters####### 
#############################################

data_file='../Input_Files/input.dat' #### File containing raw data obtained from Conf_Search protocol

data=np.loadtxt(data_file)

## Index for each slow coordinate
z_index = 0
inc_index = 1
az_index = 2
en_index = 3

### en_std and en_mean used to standardize energy.
en_std = np.std(data[:,en_index])
en_mean = np.mean(data[:,en_index])

##### Load in transition data
transition_file = '../Output_Files/transition_search.dat' #### File containing transitions from MCPS
num_transitions = 2000 ### number of transitions to load.  Use a number at which the density converges

t_file=open(transition_file)
transitions_tot=[]
with t_file as my_file:
    for line in my_file:
        myarray=np.fromstring(line, dtype=float, sep=' ')
        transitions_tot.append(myarray)
transitions=transitions_tot[0:num_transitions]

###### Grid construction parameters

z_step = 1 ## grid size in z
inc_step = 18 ## grid size in inc
az_step = 18 ## grid size in az
top_z=6 ## topmost z to create grid
bott_z=-2 ## bottomost z

##### Trajectory selection parameters
bins_z=[]

z_num=int((top_z-bott_z)/float(z_step))

#### Create bins for z, inc, az

## Do not change parameters here
for i in range(z_num):
    z_i=top_z-z_step*i
    bins_z=np.append(bins_z,z_i)

bins_inc_ang=np.arange(0,180,inc_step) #### create bins by defining the lower range of the bin 
bins_az_ang=np.arange(0,360,az_step)

##### Assign each step of every trajectory to a grid

paths_file = 'pathway_grids.dat' #### Grid at each point of each traj
paths_density_file = 'pathway_density.dat' #### Density at each point along traj
    
###### Group trajectories ########

cluster_cutoff = 0 #### Define how to cutoff the clusters.  In this code, this is defined as the aziuthal angle to cutoff the clusters.  If you do not want to cluster, then just set this cutoff to 0
density_cutoff = 0.2 ## we are using grids denser than this to group trajectories.

count_cutoff = len(bins_z)-1 ## keep this set as is.

paths_file = f'Traj_Group_Data/screened_trajectories.dat' ## where to store all filtered trajectories
paths_file_c1 = f'Traj_Group_Data/cluster1_paths.dat' ## where to store filtered trajectories for group 1
paths_file_c2 = f'Traj_Group_Data/cluster2_paths.dat' ## where to store filtered trajectories for group 2

############## The points on each trajectory need to be represented as grids. SWITCH controls whether you need to assign these grids or you have already done so.
SWITCH = 1  ## if you have already assigned grids to paths: SWITCH = 0, otherwise: SWITCH = 1

##############################################
######## Running calculation####### 
#############################################

####### Grid construction ########

Grid_z,Grid_inc,Grid_az,Grid_density = Grid_Construct.grid_construction (data, transitions, z_index, inc_index, az_index, en_index, en_mean, en_std, top_z, bott_z, z_step, inc_step,az_step)

np.savetxt('Grid_Data/grid_density.dat',Grid_density)
np.savetxt('Grid_Data/grid_z.dat',Grid_z)
np.savetxt('Grid_Data/grid_inc.dat',Grid_inc)
np.savetxt('Grid_Data/grid_az.dat',Grid_az)

print('Created grids')

##### Assign each step of every trajectory to a grid ######

if SWITCH == 1:
    pathway_grids, pathway_density = Select.assign_paths(transitions, data, z_index, inc_index, az_index, top_z,bott_z,bins_z,bins_inc_ang,bins_az_ang,paths_file,paths_density_file,z_step, inc_step,az_step,Grid_z,Grid_density)
elif SWITCH==0:
    pathway_grids, pathway_density = Select.open_paths(paths_file,paths_density_file)

print('Assigned points along paths to grids')
##### Filter trajectories #######

Select.cluster_trajectories(transitions, bins_z, pathway_grids, pathway_density, count_cutoff, density_cutoff, cluster_cutoff,paths_file,paths_file_c1,paths_file_c2,Grid_z,Grid_az,Grid_density)

print('Grouped trajectories')

