import csv

with open('output.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    data = [col for col in csv_reader]
print(data)