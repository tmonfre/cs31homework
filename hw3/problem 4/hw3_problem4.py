# Thomas Monfre
# Dartmouth College CS 31, 19W
# Homework 3 Problem 4

import numpy as np
from math import inf

# open file and store each word in array words
file = open("paragraph.txt", "r")
words = [None] # insert null so we index from 1 (following project description)

for line in file:
    words.append(line[:-1])

file.close()

# define helper variables and constants
M = 70  # maximum line length (measured in characters)
n = len(words)  # number of words in file

# create helper matrices (size nxn) and fill with zeros
num_extra_spaces = np.zeros((n,n))
cost_of_line = np.zeros((n,n))

# fill in num_extra_spaces (holds the number of extra spaces for a given choice of words i through j)
for i in range(1,n):
    for j in range(1,n):
        # determine the number of extra spaces on this choice of line
        extra_spaces = M - j + i  # number of characters per line minus the number of spaces

        # subtract off lengths of words
        for word in range(i,j+1):
            extra_spaces -= len(words[word])

        # add to matrix
        num_extra_spaces[i,j] = extra_spaces

# fill in cost_of_line (holds the cost of a line of words from word i to word j)
for i in range(1,n):
    for j in range(1,n):
        # if this choice of words does not fit on a line, set cost to infinity to ensure we avoid making it a line
        if num_extra_spaces[i,j] < 0:
            cost_of_line[i,j] = inf

        # if we've found the last line, ignore by setting cost to 0 (since we are focused on minimizing above lines)
        elif j == (n-1):
            cost_of_line[i,j] = 0

        # otherwise, define cost as cube of number of extra spaces at the end of the line (from problem description)
        else:
            cost_of_line[i,j] = num_extra_spaces[i,j] ** 3

# the sub-problem is the choice of the first word in the last line
# let's assume we have words 1...j and we are told the word i that is the first word in the last line. Then the cost of
# choosing word i is the cost of the optimal solution to the sub-problem for the lines above it plus the cost of that line.

# instantiate optimal_costs (array from 1..n) that will hold the lowest cost found for a line from 1..j
optimal_costs = [0]
indices_of_first_word_in_line = [1]  # holds the index of the first word in the last line for each choice of words 1..j

# perform a bottom-up solution to this above problem by computing the best cost we found for each choice of j from 1...n
for j in range(1,n):
    # initially set the optimal cost for this j to the cost where i is 1 (in this case we only need the cost of the line)
    optimal_costs.append(cost_of_line[1,j])
    indices_of_first_word_in_line.append(1)

    # try all other options for i
    for i in range(2,j+1):
        cost = optimal_costs[i-1] + cost_of_line[i,j]

        # update if found better
        if cost < optimal_costs[j]:
            optimal_costs[j] = cost
            indices_of_first_word_in_line[j] = i

# determine the index of the first word in each line from the optimal cost substructure above
output_indices = []
current_index = n-1

# keep looping until we've found the first line
while current_index > 1:
    # get the index of the first word in the last line, insert it into output_indices, then follow the stored indices
    # up until we hit the first line
    output_indices.insert(0,indices_of_first_word_in_line[current_index])
    current_index = indices_of_first_word_in_line[current_index] - 1

# print the computed solution to the output file
output_file = open("output.txt", "w")

# define the indices we are currently visiting
start_index = None
end_index = None

# loop through all indices but the last
for i in range(len(output_indices) - 1):
    # indices in words we will write out
    start_index = output_indices[i]
    end_index = output_indices[i+1]

    # construct string that holds desired words with spaces in between
    s = ""
    for word in range(start_index, end_index):
        s += words[word] + " "
    s = s[:-1] # remove last space

    # write to output and advance
    output_file.write(s + "\n")

# write out the last line
start_index = end_index
end_index = n

# construct string that holds desired words with spaces in between
s = ""
for word in range(start_index, end_index):
    s += words[word] + " "
s = s[:-1] # remove last space

# do not include new-line character
output_file.write(s)