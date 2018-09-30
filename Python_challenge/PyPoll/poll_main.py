# importing packages and data csv
import os
import csv
poll_csv = os.path.join("./election_data.csv")

# defining initial lists and variables
voters = 0
voterID = []
candidates = []

# opening and defining csvreader to manipulate further
with open(poll_csv,newline="") as pollcsvfile:
    csvreader = csv.reader(pollcsvfile,delimiter=",")
    # prints header to remove it from subsequent for loop
    csv_header = next(csvreader)
    # print(csv_header)
    # for loop
    for row in csvreader:
        voters = voters + 1
        voterID.append(row[0])
        candidates.append(row[2])

# generating totals for each of the candidates with a new dictionary
# of candidate vote totals
    cand_count_calc = {}.fromkeys(candidates,0)
    for candidate in candidates:
        cand_count_calc[candidate] += 1

# generating another dictionary to calculate each candidate's percentage
# share of the total votes 
    cand_percentage_calc = {candidate: round(float((cand_count_calc[candidate]/voters)*100),6) for candidate in candidates}

# determining the election winner, flipped value/key order for easier calling below
    election_winner = [(value, key) for key, value in cand_count_calc.items()]

# breaking down dictionaries to make new lists
    cand_name = cand_count_calc.keys()
    cand_votes = cand_count_calc.values()
    cand_percentage = cand_percentage_calc.values()

# making a new list and defining a function to generate election totals strings
    organizing_cand_data = [[name, percentage, votesTotal] for name, percentage, votesTotal in zip(cand_name,cand_percentage,cand_votes)]
    for row in organizing_cand_data:
        organized_cand_data = list()
        organized_cand_data.append(f'{row[0]}: {row[1]}% ({row[2]})')
    print(len(organizing_cand_data))
    print(organizing_cand_data)

# trying to put these print statements into a variable that I can put in the summary variable below


# printing data summary
    dataSummary = f"""

    Election Results
    -------------------------
    Total Votes: {voters}
    -------------------------
    {organized_cand_data}
    -------------------------
    Winner: {max(election_winner)[1]}
    """
    print(dataSummary)

# putting data summary as a .txt file output
f = open('poll_data.txt','w')
f.write(dataSummary)
f.close()