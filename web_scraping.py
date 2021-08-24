# we need to install and import few modules
# 1- pip install lxml
# 2- pip install requests
# 3- pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_titles = []
company_names = []
location_names = []
links = []
job_requirements = []
date = []

page_num = 0

while True:
    # we need to fetch the url by requests
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=data%20analyst&start={page_num}")

        # we need to save request in var
        src = result.content

        # we need to create soup object to parse content
        soup = BeautifulSoup(src, "lxml")

        # we need to find the elements which we are searching for like:
        # -- job title, job skills, location, company name, Apply now, date

        job_title = soup.find_all("h2", attrs={"class": "css-m604qf"})
        company_name = soup.find_all("a", attrs={"class": "css-17s97q8"})
        location_name = soup.find_all("span", attrs={"class": "css-5wys0k"})
        posted_old = soup.find_all("div", attrs={"class": "css-4c4ojb"})
        posted_new = soup.find_all("div", attrs={"class": "css-do6t5g"})
        posted = [*posted_old, *posted_new]
        page_limit = int(soup.find("strong").text) // 15

        if (page_num > page_limit):
            print("Page ended")
            break

        # now we will make a loop to fetch the text from the list
        for i in range(len(job_title)):
            job_titles.append(job_title[i].text)
            company_names.append(company_name[i].text)
            location_names.append(location_name[i].text)
            links.append(job_title[i].find("a").attrs['href'])
            # return_value = posted[i].text.replace("-", "").strip()
            date.append(posted[i].text)

        page_num += 1
        print("Page Switched")
    except:
        print("error occurred")
        break

# here we will open another link to get more information
for link in links:
    result = requests.get(link)
    soup = BeautifulSoup(result.content, "lxml")
    job_requirement = soup.find("div", attrs={"class": "css-1t5f0fr"}).ul
    respon_text = ""
    for li in job_requirement.find_all("li"):
        respon_text += li.text+"| "
    respon_text = respon_text[:-2]  # slice to cut last sign >>> | <<<
    job_requirements.append(respon_text)

# create csv file
file_list = [job_titles, company_names, location_names, links, job_requirements, date]
exported = zip_longest(*file_list)
with open(r"D:\15 Development\25 Data Analyst\02 Python\01 Arabic\01 Python 3 (Codezilla)\37 Projects\jobsets.csv", "w",
          newline='') as myfile:
    myfile_wr = csv.writer(myfile)
    myfile_wr.writerow(["Job Title", "Company Name", "Location", "Links", "Job Requirements", "Posted Date"])
    myfile_wr.writerows(exported)
