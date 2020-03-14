import re, sys
import math, random
import numpy as np
import collections

#### BEGIN----- functions to read movie files and create db ----- ####

def add_ratings(db, chunks, num):
    if chunks[0] not in db:
        db[chunks[0]] = {}
    db[chunks[0]][num] = int(chunks[2])

def read_files(db, num):
    movie_file = "movies/"+num
    ratings = []
    fo = open(movie_file, "r")
    r = 0
    for line in fo:
        chunks = re.split(",", line)
        chunks[len(chunks)-1] = chunks[len(chunks)-1].strip()
        add_ratings(db, chunks, num)

#### END----- functions to read movie files and create db ----- ####


def score(w, p, aux, r):
    '''
    Inputs: weights of movies, max rating per moive, auxiliary information, and a record, 
    Returns the corresponding score
    '''
    #### ----- your code here ----- ####

    supp_aux = len(aux)
    score = 0

    for movie in aux:
        if movie in r:
            score += w[movie] * ((1-( abs(aux[movie] - r[movie]) / p[movie] )) / supp_aux)

    return score



def compute_weights(db):
    '''
    Input: database of users
    Returns weights of all movies
    '''
    weights = {}
    movie_freq = calc_freq(db)
    #compute weights
    
    for movie in movie_freq:
        weights[movie] = 1/(np.log(movie_freq[movie]))

    return weights

#### BEGIN----- additional functions ----- ####

def calc_min_max(db, aux):

    min_max_rating = collections.defaultdict(list)

    for user in db:
        for movie in db[user]:
            db_rating = db[user][movie]

            if movie not in min_max_rating:
                min_max_rating[movie].append(float('inf'))
                min_max_rating[movie].append(float('-inf'))

            min_max_rating[movie][0] = min(min_max_rating[movie][0], db_rating)
            min_max_rating[movie][1] = max(min_max_rating[movie][1], db_rating)

            if movie in aux:
                min_max_rating[movie][0] = min(min_max_rating[movie][0], aux[movie])
                min_max_rating[movie][1] = max(min_max_rating[movie][1], aux[movie])

    return min_max_rating
            

def calc_range(rating):
    p = {}
    for movie in rating:
        p[movie] = abs(rating[movie][0]-rating[movie][1])

    return p

def all_scores(db, aux, w):
    
    
    min_max_rating = calc_min_max(db,aux)
    p = calc_range(min_max_rating)

    user_score = {}

    for user in db:
        user_score[user] = score(w, p, aux, db[user])

    print("Number of users in the database are {}".format(len(db)))
    print()
    sorted_ids = sorted(user_score, reverse = True, key = lambda k: user_score[k])

    return sorted_ids,user_score



def calc_freq(db):
    freq = {}

    #intially store the frequency for each movie
    for user in db:
        for movie in db[user]:
            if movie != 0:
                if movie not in freq:
                    freq[movie] = 1
                else:
                    freq[movie] += 1

    return freq

def print_highest_id(user_ids, db, aux):
    max_user_id = user_ids[0]

    print('The user-id of the user with highest score is {}\n'.format(max_user_id))
    print('Movie ratings of user from database:\n')

    max_user_ratings = db[max_user_id]

    for k,v in max_user_ratings.items():
    	print('{}: {}'.format(k,v))

    print()
    print('Note: The values of auxiliary db are rounded to verify similarity\n')

    for movie in max_user_ratings:
        if movie in aux:
            if max_user_ratings[movie] == round(aux[movie]):
                print('Rating for movie {} is similar to movie rating in auxiliary db '.format(movie))
            else:
                print('Rating for movie {} is not similar to movie rating in auxiliary db '.format(movie))
        else:
            print('Movie {} not found in auxiliary db'.format(movie))
    print()

def calc_ecc(aux, w):
    M = 0
    GAMMA = 0.1
    supp_aux = len(aux)
    for movie in aux:
        M += (w[movie] / supp_aux)

    return GAMMA*M

#### END----- additional functions ----- ####

if __name__ == "__main__":
    db = {}
    files = ["03124", "06315", "07242", "16944", "17113",
            "10935", "11977", "03276", "14199", "08191",
            "06004", "01292", "15267", "03768", "02137"]
    for file in files:
        read_files(db, file)

    aux = { '14199': 4.5, '17113': 4.2, '06315': 4.0, '01292': 3.3,
            '11977': 4.2, '15267': 4.2, '08191': 3.8, '16944': 4.2,
            '07242': 3.9, '06004': 3.9, '03768': 3.5, '03124': 3.5}

    
    w = compute_weights(db)
    print('Movie: Weight')
    print()

    for movie,rating in w.items():
        print('{}: {}'.format(movie, rating))
    print()

    sorted_ids,user_score = all_scores(db,aux, w)
    highest_score = user_score[sorted_ids[0]]
    second_highest = user_score[sorted_ids[1]]

    print('Highest score is {}'.format(highest_score))
    print('Second highest score is {}'.format(second_highest))
    print()

    print_highest_id(sorted_ids, db, aux)

    threshold = calc_ecc(aux, w)
    print('Value of  eccentricity threshold is {}'.format(threshold))
    print('Difference between highest and second highest score is {}'.format(highest_score - second_highest))

    print('Is the difference greater than eccentricity threshold: {}'.format((highest_score - second_highest)>threshold))

    ### ----- your code here ----- ####
