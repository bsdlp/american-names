import requests
import sys
import csv
from bs4 import BeautifulSoup


def atoi(c: str) -> int:
	return int(c.replace(',', ''))

def quicksort(items: list) -> list:
	if len(items) <= 1:
		return items
	pivot = items[0][1]
	left = [x for x in items[1:] if x[1] >= pivot]
	right = [x for x in items[1:] if x[1] < pivot]
	return quicksort(left) + [items[0]] + quicksort(right)

response = requests.get("https://www.ssa.gov/oact/babynames/decades/century.html")
soup = BeautifulSoup(response.content, 'html.parser')
table_body = soup.table.tbody
rows = table_body.find_all('tr')

# [[name, count]]
data = []

for row in rows:
	# ranking, male_name, male_count, female_name, female_count
	cols = row.find_all('td')
	if len(cols) != 5:
		continue
	cols = [ele.text.strip() for ele in cols]
	data.append([cols[1], atoi(cols[2])]) # male_name, male_count
	data.append([cols[3], atoi(cols[4])]) # female_name, female_count

data = quicksort(data)
csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(['name','count'])
for row in data:
	csv_writer.writerow(row)

