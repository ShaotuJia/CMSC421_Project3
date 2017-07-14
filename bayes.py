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

import sys

# Obtain train data from file
train_file_name = sys.argv[1]
train_file = open(train_file_name, "r")

data = []
for line in train_file:
    data.append(line)

# Obtain classify data from file
classify_file_name = sys.argv[2]
classify_file = open(classify_file_name, "r")
classify_data = []
for line in classify_file:
    classify_data.append(line)


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
def posterior_democrat(data:list,test_ticket:list):
    likelihood = []
    for i in range(1,len(test_ticket)):
        counter = 1         # For Zero Frequency Problem; add ONE for one of choices(y, n, ?) !!
        d_counter = 3       # For Zero Frequency Problem; add ONE for all three choices(y,n,?) !!
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


def posterior_republican(data:list, test_ticket:list):
    r_likelihood = []
    for i in range(1,len(test_ticket)):
        counter = 1         # For Zero Frequency Problem; add ONE for one of choices(y, n, ?) !!
        r_counter = 3       # For Zero Frequency Problem; add ONE for all three choices(y,n,?) !!
        for j in range(0, len(data)):
            train_ticket = data[j].split(',')
            if train_ticket[0] == 'republican':
                r_counter = r_counter + 1
                if train_ticket[i] == test_ticket[i]:
                    counter = counter + 1
        r_likelihood.append(counter/r_counter)

    prior_pr = r_counter/len(data)
    total = multiply(r_likelihood)
    result = total*prior_pr
    return result


# This function is to normalize the probability
# Return the posterior probability of democrat
def d_normalize(posterior_R:float, posterior_D: float):
    return posterior_D/(posterior_R + posterior_D)


# Bayes Function
def bayes(data:list, test_ticket:list):
    posterior_R = posterior_republican(data, test_ticket)
    posterior_D = posterior_democrat(data, test_ticket)
    return d_normalize(posterior_R, posterior_D)


# Print the result for a series of classify data
def output(data: list, classify_data: list):
    for ticket in classify_data:     # Tickets are stored as 'str' in data set
        ticket = ticket.split(',')   # convert str to list for bayes function
        pr = bayes(data, ticket)
        print("The Probability of being a democrat: ", pr)

# Print results
output(data, classify_data)





