import neverbounce_sdk as nb
import pandas as pd
import numpy as np

# SETTING UP API KEY FOR NEVERBOUNCE
api_key = 'private_ab043d7c068809af0652039366a9129c'
client = nb.client(api_key=api_key, timeout=30)
acc = client.account_info()

# READING CSV FILE

doc = pd.read_csv("VAR.csv")

# EXTRACTING CONTACT NAMES & INITIALS

# SETTING UP THE LISTS TO BE APPENDED INTO
temp_name = []
contact_name = []
first_name_tab = []
last_name_tab = []
first_init_tab = []
last_init_tab = []

domain = []

# FOR LOOP EXTRACTING THE DATA
# TO DO: AUTOMATE FINDING THE LENGTH OF THE EXCEL CSV FILE
#        AUTOMATE FINDING THE COLUMN WITH THE FULL NAME
for i in range(0, 54):
    temp_name.append(doc.iloc[i][0])
    contact_name.append(temp_name[i].split(" ", 1))
    first_name_tab.append(contact_name[i][0])
    last_name_tab.append(contact_name[i][1])
    first_init_tab.append(contact_name[i][0][0])
    last_init_tab.append(contact_name[i][1][0])
    domain.append(doc.iloc[i][1])

# EMAIL FORMATS IN ORDER OF POPULARITY

# 1 [First_Name].[Last_Name]
# 2 [First_Inital][Last_Name]
# 3 [First_Name]
# 4 [First_Name][Last_Initial]
# 5 [First_Name][Last_Name]
# 6 [First_Initial].[Last_Name]
# 7 [First_Name]_[Last_Name]
# 8 [First_Initial][Last_Initial]


# SETTING UP EMAIL FORMAT FUNCTION

def email_format(k, i):
    if k == 1:
        return "{0}.{1}@{2}".format(first_name_tab[i], last_name_tab[i], domain[i])
    elif k == 2:
        return "{0}{1}@{2}".format(first_init_tab[i],last_name_tab[i], domain[i])
    elif k == 3:
        return "{0}@{1}".format(first_name_tab[i], domain[i])
    elif k == 4:
        return "{0}{1}@{2}".format(first_name_tab[i],last_init_tab[i], domain[i])
    elif k == 5:
        return "{0}{1}@{2}".format(first_name_tab[i],last_name_tab[i], domain[i])
    elif k == 6:
        return "{0}.{1}@{2}".format(first_init_tab[i], last_name_tab[i], domain[i])
    elif k == 7:
        return "{0}_{1}@{2}".format(first_name_tab[i], last_name_tab[i], domain[i])
    elif k == 8:
        return "{0}{1}@{2}".format(first_init_tab[i], last_init_tab[i], domain[i])



# SETTING UP EMAIL CHECK FUNCTION

def email_check(i):
    for l in range(1,9):
        resp = client.single_check(email_format(l,i))
        print(resp)
        if (resp['result'] == 'catchall'):
            print(acc['credits_info'])
            exit()
        if (resp['result'] == 'valid'):
            print(acc['credits_info'])
            print(email_format(l,i))
            exit()

# TO DO:
#      -ADD A CONTINGENCY FOR TIMEOUT REQUESTS
#      -ADD CORRECT EMAILS TO A CSV
#      -CREATE DATABASE FOR CORRECT EMAILS FORMATS WITH COMPANY SIZE & INDUSTRY
#       TO ALLOW TRACKING OF MOST COMMON FORMATS ACROSS MANY METRICS

n = 53

print(email_format(1,n))
email_check(n)


#resp = client.single_check(email0(2))
#print(resp)
#print('Done')
#if (resp['result'] == 'invalid'):
 #   print('Invalid')
#if (resp['result'] == 'catchall'):
#    print('Catchall')

print(acc['credits_info'])
