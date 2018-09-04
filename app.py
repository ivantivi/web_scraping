from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


my_url = "https://www.nytimes.com/interactive/2017/06/23/opinion/trumps-lies.html"
#grabbing the html
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html,"html.parser")

#grabs all lies
blocks = page_soup.findAll("span", {"class", "short-desc"})

file_name = "all_lies.csv"
header = "Date, Lie, Truth"

with open(file_name, "w") as file:
    file.write(header)
    for i, block in enumerate(blocks):
        lie = block.strong.next_sibling
        date = block.strong.text
        truth = block.a.text
        file.write(f"\n{date},{lie.replace(',', '|')},{truth.replace(',', '|')}")
