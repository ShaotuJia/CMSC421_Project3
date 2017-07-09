#! /usr/bin/env python3

# Brief: This project is to estimate probability that each record in classify.data is a democrat representative
# Assumption: at first, assume that each field is independent to others
# Step 1: Load train data Set
# Step 2: Find the relation between party (democrat) and vote (Y, N, ?) in each field
# Step 3: Using obtained relation to estimate in classify.data
# Hints: using naive bayes (based on conditional independence) and using normalization to simplify the computation
# Example: P(R|a,b,c,d) = P(a,b,c,d|R)*P(R)/P(a,b,c,d) = alpha*P(a,b,c,d|R)*P(R)
# Example: P(D|a,b,c,d) = P(a,b,c,d|D)*P(D)/P(a,b,c,d) = alpha*P(a,b,c,d|D)*P(D)
# Example: P(a,b,c,d|R) = P(a|R)*P(b|R)*P(c|R)*P(d|R) # naive bayes, conditional independence
# !! In case Zero Frequency Problem !!!
from functools import reduce


filename = "house-votes-84.data"
file = open(filename, "r")

data = []
for line in file:
    data.append(line)

test = 'party,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n'
test = test.split(',')
likelihood = []
d_count = 0
r_count = 0


p_r = 0
p_d = 0


# This function is to get the Class Prior Probability of Democrat
# Probability of Republican is (1 - Democrat)
def democrat_pr(data):
    data_size = len(data)
    for i in range(0, data_size):
        ticket = data[i].split(',')

        if ticket[0] == 'republican':
            r_count = r_count + 1
        else:
            d_count = d_count + 1
    return d_count/data_size


def multiply(likelihood):
    result = 1
    amplifier = 5
    for i in range(0, len(likelihood)):
        result = result * likelihood[i]
    return result


# This function is to get posterior probability of 'democrat' without normalization
def posterior_democrat(test_ticket):
    likelihood = []
    for i in range(1,len(test_ticket)):
        counter = 1         # For Zero Frequency Problem !!
        d_counter = 3       # For Zero Frequency Problem !!
        for j in range(0, len(data)):
            train_ticket = data[j].split(',')
            if train_ticket[0] == 'democrat':
                d_counter = d_counter + 1
                if train_ticket[i] == test_ticket[i]:
                    counter = counter + 1
        likelihood.append(counter/d_counter)

    prior_pr = d_counter/len(data)
    total = multiply(likelihood)
    result = total*prior_pr
    return result




posterior = posterior_democrat(test)

print("{:.2e}".format(posterior))






