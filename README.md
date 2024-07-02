# Rain-drain-programming-exercise
<p align="justify">
An artist is setting up a collection of rain drains on a wall. From the top of the wall there is water
flowing down equally distributed along the complete edge. On the wall, there are several rain drains,
which capture water and release it on the right end.
Your task is to write a program, which calculates the amount of water flowing out on the right side of
a rain drain.

The program has the following inputs:

N... number of rain drains
<br><br>

For each rain drain, three values have to be provided:

H... height of the rain drain (integer)

L... left endpoint of the rain drain (integer)

R... right endpoint of the rain drain (integer)
<br><br>

One additional global parameter is requested as input:

amount... amount of water / length which is flowing down from the top edge. (double)
(For example a rain drain fully exposed to water from the top will release (R-L)*amount of water on
its right end)
<br><br>

The below picture is an illustrative example of how such a setup could look like. The numbers in the
picture indicate outflows on the right end of the rain drains.
</p>

<p align="center">
  <img  style="text-align:center" src="https://github.com/albifnt/Rain-drain-programming-exercise/blob/main/img/Wall.PNG">
</p>

## Task
<p align="justify">
Write a program in Python or C#, which outputs the amount of water flowing out of each rain drain.
Describe your approach in a few sentences.
Choose appropriate data structures and determine its runtime complexity with respect to the
number of rain drains N.
</p>

## Solution
### ASSUMPTIONS
<p align="justify">
  
- We assume the system is at steady state, so we neglect any transient.
  
- We assume that when the right x of the rain drain correspond to the left x of the below rain drain (as
show in the below picture), the water of the higher rain drain is captured on the lower one.

<p align="center">
  <img  style="text-align:center" src="https://github.com/albifnt/Rain-drain-programming-exercise/blob/main/img/Figure_1.PNG">
</p>

- We assume that when the right x of the rain drain correspond to the left x of another rain drain at the
same height (as show in the below picture), the water from the left drain moves to the right one (so they
behave as one longer rain drain).

<p align="center">
  <img  style="text-align:center" src="https://github.com/albifnt/Rain-drain-programming-exercise/blob/main/img/Figure_2.PNG">
</p>

- We assume that the rain drains are not overlapping, otherwise the inputs are not validated.
</p>

### INFORMAL EXPLANATION
<p align="justify">
To solve the problem, I imagine to start at the upper edge of the wall with a list named "wall_rain_fall".
This list is as long as the width of the wall, which is determined by the difference between the maximum
right x-coordinate and the minimum left x-coordinate of the rain drains.
"wall_rain_fall" is initialized with the input value representing the amount of water per unit length.
Progressing downward from the wall's top edge, I come across the initial rain drain – the one positioned at
the highest and left most height. Since I know the x-coordinates for its right and left sides, I can sum the
corresponding values in the "wall_rain_fall" list. This sum is the amount of water streaming from the right
end of this drain. Now, I update the "wall_rain_fall" list as follows: first I set the components corresponding
to the currently examined rain drain to zero; then, I set the component immediately after the right end of
the drain to previously computed sum.
Transitioning to the subsequent rain drain, which might rest at a lower height, I repeat the same process.
This procedure works because if this new drain happens to be partially or completely covered by a
previously processed drain, the summation of zero-valued components doesn't contribute to its water
amount.
</p>

### FORMAL EXPLANATION
<p align="justify">
Initially, the rain drains are sorted in descending order based on their height. Following that, for rain drains
with the same height, a secondary sorting is done in ascending order according to their left horizontal
coordinate. This prioritizes the rain drain with the smaller left x when they share the same height. 

<p align="center">
  <img  style="text-align:center" src="https://github.com/albifnt/Rain-drain-programming-exercise/blob/main/img/Figure_3.PNG">
</p>

This sorting allows for a systematic examination of each rain drain one by one. Before starting the analysis,
one list, with length equal to the width of the wall, is prepared:

- "wall_rain_fall": this list indicates the water quantity that can accumulate on the examined rain drain per
unit of length. When an entry is non-zero, it means that water, originating from either the wall's upper
edge or the right end of an overlying rain drain, can reach the specific position corresponding to the rain
drain. Conversely, a zero entry indicates obstruction by one or more other rain drains between that
position and the wall's top edge. Initially, all list entries are set to the water amount per unit of length,
which is an input of the problem. However, as we progress from one rain drain to the next, entries
spanning the horizontal width of the current rain drain are updated to 0, representing blocked water flow.
Simultaneously, the entry just beyond the rain drain's right edge is increased by the amount of the
examined drain.

By sequentially moving from one rain drain to the next and updating these two lists, it becomes feasible to
determine the water amount falling from the right end of each rain drain.
The code produces a list, with each entry representing the water amount for the corresponding rain drain,
maintaining the same order as the inputs.
</p>

### STRUCTURE OF THE CODE
<p align="justify">
The code features the following functions:

- <b>generate_random_drains()</b>: this function generates the input height, left_x and right_x lists containing
the coordinates of the rain drains. It is used only test.py.

- <b>validate_input()</b>: this function checks that the inputs of the problem satisfy the assumptions below.
  
- <b>calculate_drain_amount()</b>: this function contains the resolution algorithm.
  
- <b>generate_raindrops()</b>: this function generates the raindrops to be displayed in the plot.
  
- <b>process_to_height_and_raindrops()</b>: this function evaluates the heights of the locations where the water
amounts of the different rain drains fall and process the raindrops based on the DataFrame information.

- <b>plot_graph()</b>: this function plots the graph.
  
</p>

<p align="justify">
The code is structured in 3 files:
  
  - main.py: it contains the code to run. Before running the code the user should replace the inputs: N, water_amount_per_unit_of_length, height, left_x and right_x.
  
  - test.py: it contains a simulation of the problem. The inputs N and amount of water/length are specified and the height, left_x and right_x input lists are generated with the generate_random_drains() function.
  
  - functions.py: it contains the functions.
    

The requirements.txt file contains the packages that are necessary to run the code. To install the packages run:

    pip install -r requirements.txt

</p>

### RUNTIME COMPLEXITY
<p align="justify">
To analyze the time complexity of the given algorithm, we do not investigate the functions
<b>generate_random_drains()</b> (since this is only executed when the user does not insert the inputs),
<b>generate_raindrops()</b>, <b>process_to_height_and_raindrops()</b>, <b>plot_graph()</b> (since these functions are used
only to implement and display the graphical representation of the solution which is not necessarily needed)
and we focus on the <b>validate_input()</b>, <b>calculate_drain_amount()</b> functions. Let’s consider the
<b>calculate_drain_amount()</b> function first which has a time complexity of O(N M). Let’s break it down step by
step:
  
- Sorting: the initial part of the algorithm involves sorting the df dataframe based on the height and left_x
column. Sorting typically has a time complexity of O(N logN), where N is the number of elements in the list.

- Loop: the algorithm then iterates over the N rows of the df dataframe. Inside the loop, there are some
operations involving assigning values to variables, slicing lists and summing elements of lists. These
operations are performed on subarrays with a maximum fixed size equal to wall_width = M. The wall_width
depends on the inputs, since it is given by the difference between the maximum right x-coordinate and the
minimum left x-coordinate among all the input rain drains. Therefore the time complexity of these internal
operations can be considered O(M).

The loop iteration itself contributes O(N) since each row in the df dataframe is processed once. Inside each
loop we are performing the counting and summing operations that contributes O(M). Therefore, the overall
time complexity of the algorithm is O(N M). For the same reasons, even validate_input() has a time
complexity of O(N M).
</p>
<br><br>

<p align="justify">
To calculate the space complexity of the given algorithm, we focus again only on the
<b>calculate_drain_amount()</b> function for the aforementioned reasons. We need to consider the additional
memory used by the algorithm in terms of data structures and variables.
Data structures and variables:
  
- <b>df</b>: this dataframe is generated at the beginning of the algorithm with the input height, left_x and right_x
lists which have length N, and therefore the space complexity of the dataframe is O(N). The dataframe is
augmented with the drain_amount column, but this does not affect the space complexity.

- <b>wall_rain_fall</b>: this list is created to keep track of the presence of the water amounts above the rain
drains. It has length equal to the wall_width = M. Therefore the space complexity of this list is O(M).

- <b>min_x_left</b>, <b>wall_width</b>: these variables are used to store numeric values and occupy constant space.
  
- <b>left_index</b>, <b>right_index</b>, <b>length</b>, <b>drain_amount</b>: these variables store temporary values and occupy
constant space during each iteration of the loop.

- <b>outstanding_wall_rain_fall</b>: this list stores temporary values. It stores at most wall_width values,
therefore it is at most O(M) during each iteration of the loop.

Considering the space complexities of the data structures and variables, and identifying O(M) and O(N) as
the two dominant terms, the space complexity O(N + M) is linear because it grows linearly with the size of
the input data.
  
