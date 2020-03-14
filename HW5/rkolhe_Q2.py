#!/usr/bin/env python
# coding: utf-8

# In[1]:


from nltk.corpus import wordnet
import collections


# In[2]:


#A list of checkpoints from question2 a)
checkpoints = [
    ['Does the operator obtain parental consent by directly notifying the parent with regard to the collection, use or disclosure of personal information from the children?'],
    ["Does the operator collect the parent's online information from the child in order to provide notice"],
    ["Does the notice contain the name, address, telephone number, email address of all operators that collect and maintain personal information from children?"],
    ["Does the operator take additional measures to verify that the person providing the consent is actually the parent of the child?"],
    ["Does the operator provide the requested information to the parent whose child has given the concerned information?"],
    ["Is the operator fair in terms of the child’s participation in the game and offering of a price? The operator should not be unfair to the child in exchange for collecting additional information from the child"],
    ["Does the operator take required measures to encrypt and protect the personal information collected from children?"],
    ["Does the operator delete all the personal information of the child and the parent after the purpose for which it is collected is served?"]
]
# list of keywords from each checkpoint
checkpoint_keyword = [
    ['parental','consent' ,'notifying' ,'collection','information' ],
    ['parent', 'online' ,'information' ,'comply' ,'refuse' 'permit' ,'contact' ,'delete' ],
    ['clearly' ,'labeled' ,'link' ,'notice','name','address','telephone','email'],
    ['measures','verify' ,'delete' ,'failed' ,'attempts' ,'not' ,'shared' ],
    ['provide', 'requested', 'information'],
    ['fair' ,'participation' ,'offering' ,'prize'],
    ['measures' ,'encrypt' ,'protect' 'personal' ,'information'],
    ['delete' ,'information','child','parent']
]

#create a bag of words for each checkpoint
#store the synonyms of each keyword in a list
#checkpoint_syns stores a list of checkpoint keywords
checkpoint_syns = []
for point in checkpoint_keyword:
    tmp = set()
    for word in point:
        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                tmp.add(l.name())
    checkpoint_syns.append(tmp)


# In[3]:


#load the policies of all five applications in a list
policies = []
for num in range(1,6):
    path = 'policy'+str(num)+'.txt'
    with open(path,'r+',encoding="utf8") as f:
        policies.append(f.read().splitlines())


# In[4]:


#split each policy into words
new_policy = []
for policy in policies:
    new_policy.append([[word for word in sentence.split(' ')] for sentence in policy])


# In[5]:


#this function annontates the sentences that are closest to each checkpoint

def annotate_sentences(policy_index, threshold):
    print('######################################')
    print(f'Policy {policy_index+1} matches are as follows:')
    print()
    checkpoints_sentences = collections.defaultdict(list)
    for sentence in new_policy[policy_index]:
        matches = []
        for idx, checkpoint in enumerate(checkpoint_syns):
            if len(checkpoint.intersection(set(sentence))) > threshold:
                print('***********')
                print('Sentences that match the given checkpoint->')
                print()
                print(' '.join(sentence))
                print()
                print('Checkpoint->')
                print(checkpoints[idx][0])
                print()
                break


# In[6]:


annotate_sentences(0,1)
annotate_sentences(1,2)
annotate_sentences(2,2)
annotate_sentences(3,2)
annotate_sentences(4,2)

