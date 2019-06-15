from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import matplotlib.pyplot as plt
import re
from bs4 import Tag
from selenium.common.exceptions import NoSuchElementException
# time.sleep(30)
# driver.get("https://www.linkedin.com/in/raghunitb/") #Enter any of your connection profile Link
# connectionName = driver.find_element_by_class_name('pv-top-card-section__name').get_attribute('innerHTML')
# print(connectionName)
from collections import Counter

def parseNumber(value, as_int=False):
    try:
        number = float(re.sub('[^.\-\d]', '', value))
        if as_int:
            return int(number + 0.5)
        else:
            return number
    except ValueError:
        return float('nan')

driver = webdriver.Firefox() #I actually used the chromedriver and did not test firefox, but it should work.
driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
driver.find_element(By.XPATH, "//input[@id='username']").send_keys("xxxxx@gmail.com")
driver.find_element(By.XPATH, "//input[@id='password']").send_keys("xxxxxx")
driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

topic_views_map = {}
post_count = 0
total_views_count = 0


driver.get("https://www.linkedin.com/in/raghunitb/detail/recent-activity/posts/")

SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(10)
driver.implicitly_wait(20)
html = driver.page_source
soup = BeautifulSoup(html)
soup.get_text()
soup.text()
for tag in soup.find_all('article'):
   arr = tag.text.split('\n')
   topic_views_map[arr[8]] = parseNumber(arr[36].split()[0])
   post_count = post_count + 1
   total_views_count = total_views_count + topic_views_map[arr[8]]


views = []
likes = []
shares = []
comments = []
posts = []
views_by_company = {}
views_by_jobttitle = {}
views_by_location = {}

linkedIn_url = 'https://www.linkedin.com'

for anchor in soup.findAll('a'):
  if anchor.parent.name == 'article':
    posts.append(anchor.text.split('\n')[5])
    url = linkedIn_url + anchor["href"]
    print('parent url '+url)
    driver.get(url)
    html1 = driver.page_source
    soup1 = BeautifulSoup(html1)
    for sub_anchor in soup1.findAll('a'):
        if sub_anchor.parent.name == 'li' and 'View stats' in sub_anchor.text:
            url = linkedIn_url + sub_anchor["href"]
            print('child url '+url)
            try:
                driver.get(url)
                driver.find_element(By.XPATH, "//button[text()='Show more']").click()
            except NoSuchElementException:
                print('No link found')
                break
            html2 = driver.page_source
            soup2 = BeautifulSoup(html2)
            comment  = 0
            reaction = 0
            view = 0
            share = 0
            for details in soup2.findAll('article'):
                if 'views from people' in details.text:
                    label = details.find('h3').text.replace("views from people at"," ").strip()
                    views_by_company[label.replace(label.split()[0],"").strip()] = views_by_company.get(label.replace(label.split()[0],"").strip(), 0) + parseNumber(label.split()[0])
                    for tag in details.find('section').find('ul'):
                        if isinstance(tag, Tag):
                            jobs = tag.text.split('\n')
                            views_by_company[jobs[2].replace("views from people at ","").strip()] = views_by_company.get(jobs[2].replace("views from people at ","").strip(), 0) + parseNumber(jobs[5])
                elif 'views from' in details.text:
                    label = details.find('h3').text.replace("views from ", " ").strip()
                    views_by_location[label.replace(label.split()[0], "").strip()] = views_by_location.get(label.replace(label.split()[0], "").strip(), 0) + parseNumber(label.split()[0])
                    for tag in details.find('section').find('ul'):
                        if isinstance(tag, Tag):
                            jobs = tag.text.split('\n')
                            views_by_location[jobs[2].replace("views from ","").strip()] = parseNumber(jobs[5])
                if 'have the job title' in details.text:
                    label = details.find('h3').text.replace("have the job title ", " ").strip()
                    views_by_jobttitle[label.replace(label.split()[0], "").strip()] = views_by_jobttitle.get(label.replace(label.split()[0], "").strip(), 0) + parseNumber(label.split()[0])
                    key = "empty"
                    value = "empty"
                    for tag in details.find('section').find('ul'):
                        if isinstance(tag, Tag):
                            jobs = tag.text.split('\n')
                            views_by_jobttitle[jobs[2].replace("have the job title ","").strip()] = views_by_jobttitle.get(jobs[2].replace("have the job title ","").strip(), 0) + parseNumber(jobs[5])
            for text in soup2.find_all("span"):
                if 'comments' in text.text:
                    comment = parseNumber(text.text.split()[0])
                if 'reactions' in text.text:
                    reaction = parseNumber(text.text.split()[0])
            for text in soup2.find_all("artdeco-tab"):
                if 'article views' in text.text:
                    view = parseNumber(text.text.split()[0])
                if 'reshare' in text.text:
                    share = parseNumber(text.text.split()[0])
            likes.append(reaction)
            views.append(view)
            shares.append(share)
            comments.append(comment)

print(comments)
print(shares)
print(views)
print(likes)
print(posts)
print(topic_views_map)
print(views_by_company)
print(views_by_jobttitle)
print(views_by_location)
#
#
# comments = [0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2.0, 6.0, 3.0, 0, 2.0, 2.0, 5.0, 4.0]
# shares = [1.0, 0, 0, 2.0, 1.0, 3.0, 0, 3.0, 0, 0, 2.0, 0, 1.0, 3.0, 2.0, 0, 0, 1.0, 0, 4.0]
# views = [233.0, 133.0, 589.0, 124.0, 2105.0, 7938.0, 61.0, 5718.0, 460.0, 0, 1291.0, 57.0, 395.0, 619.0, 333.0, 91.0, 82.0, 472.0, 132.0, 524.0]
# likes = [10.0, 12.0, 7.0, 15.0, 12.0, 31.0, 5.0, 25.0, 4.0, 0, 19.0, 10.0, 30.0, 23.0, 26.0, 0, 3.0, 14.0, 7.0, 22.0]
# posts = ['Handling Kafka downtime and saving data using RocksDB', 'Why you should opt for part time freelancing?', 'Unit Testing using H2 (in-memory DB)', 'Legacy Systems vs Legacy Minds : Which one is more Dangerous?', 'Unit Testing Using Embedded Cassandra', 'Spring Kafka Integration | Unit Testing using Embedded Kafka', 'Multi-Tenancy in Spring Security', 'Partitions Rebalance in Kafka ', 'Spring Security | Token Generation without OAuth', 'Multiple tenants in Rabbit MQ using virtual hosts (vhost)', 'Event driven design using Amazon SNS, SQS & KINESIS', 'How to integrate RabbitMQ (Event Messaging System)  with Spring Boot', 'Building Serverless Applications using AWS Lambda', 'Building microservices with Netflix OSS[In Spring Boot]', 'How we migrated from Cron oriented Facebook Feed to NRT Feed!!!', 'Advertisement in E-Commerce - A clever strategy to stay in the market if implemented in better way.', 'Designation : An incurable disease', 'Micro Services Architecture[Spring Cloud Netflix] - Scalable and Distributed', 'Application Design[Architecture] - Brick and mortar of a software company', 'Indian Startups : A success or Complete Failure']
# views_by_company = {'Chegg Inc.': 165.0, 'Nationwide': 6.0, 'DBS Bank': 57.0, 'Visa': 31.0, 'Walmart Labs India': 4.0, 'Limeroad.com': 4.0, 'TiVo': 24.0, 'Cognizant': 44.0, 'EnKash- Business Payments, Simplified': 5.0, 'Wipro Limited': 4.0, 'Infosys': 4.0, 'JPMorgan Chase & Co.': 51.0, 'Vuclip Inc.': 4.0, 'BlackBuck (Zinka Logistics Solutions Pvt. Ltd.)': 4.0, 'ADP': 28.0, 'Walmart eCommerce': 18.0, 'Paysafe Group': 6.0, 'IT Six Global Services': 6.0, 'Tata Consultancy Services': 5.0, 'Boeing': 4.0, 'Express Scripts': 5.0, 'Itaú Unibanco': 5.0, 'CommerceHub': 1.0, 'GlobalLogic': 1.0, 'Apple': 46.0, 'Systech Solutions, Inc.': 19.0, 'ING': 11.0, 'Adobe': 30.0, 'NVIDIA': 10.0, 'ThoughtWorks': 32.0, 'IBM': 10.0, 'Avaya': 70.0, 'Accenture': 31.0, 'EPAM Systems': 31.0, 'Nokia': 26.0, 'Oracle': 59.0, 'Walmart Labs': 23.0, 'NICE Ltd': 2.0, 'UST Global': 4.0, 'Triple Point Technology': 5.0, 'ALTEN Calsoft Labs': 1.0, 'Scotiabank': 1.0, 'Cloudera': 23.0, 'Cisco': 20.0, 'MS LLP': 6.0, 'Sportradar': 3.0, 'Bauman Moscow\xa0State Technical University': 3.0, 'Ingsoftware': 3.0}
# views_by_jobttitle = {'Telecommunications Specialist': 165.0, 'Software Developer': 4519.0, 'Technology Manager': 644.0, 'Software Tester': 66.0, 'Engineer': 254.0, 'Consultant': 176.0, 'Information Technology Support Specialist': 6.0, 'Business Analyst': 10.0, 'Student': 13.0, 'Information Technology Consultant': 243.0, 'Project Manager': 2.0, 'Executive Director': 16.0, 'Founder': 15.0, 'Architect': 48.0, 'Information Technology Engineer': 117.0, 'Information Technology System Administrator': 106.0, 'Product Development Engineer': 63.0}
# views_by_location = {'Noida Area, India': 13.0, 'San Francisco Bay Area': 648.0, 'Bengaluru Area, India': 3.0, 'Hyderabad Area, India': 14.0, 'Gurgaon, India': 58.0, 'Columbus, Ohio Area': 7.0, 'Pune Area, India': 2.0, 'Greater New York City Area': 94.0, 'Kalyan Area, India': 4.0, 'Mumbai Area, India': 1.0, 'Bhimavaram Area, India': 1.0, 'São Paulo Area, Brazil': 3.0, 'Greater Los Angeles Area': 7.0, 'Dolj County, Romania': 6.0, 'Greater St. Louis Area': 5.0, 'Zielona Gora, Lubusz District, Poland': 3.0, 'Belo Horizonte Area, Brazil': 1.0, 'Paris Area, France': 4.0, 'London, United Kingdom': 61.0, 'Amsterdam Area, Netherlands': 17.0, 'Greater Seattle Area': 51.0, 'Madrid Area, Spain': 13.0, 'Greater Chicago Area': 69.0, 'Berlin Area, Germany': 55.0, 'Toronto, Canada Area': 1.0, 'Jalandhar Area, India': 1.0, 'New Delhi Area, India': 58.0, 'Greater Jakarta Area, Indonesia': 6.0, 'Istanbul, Turkey': 4.0, 'Oslo Area, Norway': 3.0, 'Moscow, Russian Federation': 3.0}


posts = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15','P16','P17','P18','P19','P20']


# plt.rcParams.update({'font.size': 7})
# plt.bar(topic_views_map.keys(),topic_views_map.values())
#
# plt.xlabel('Blog Names')
# plt.ylabel('Views Count')
# plt.title('Blog-View Stats')
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(19680801)

n_bins = 5
x = np.random.randn(1000, 3)
np.arange(20)

# fig, axes = plt.subplots(4)
# ax0, ax1, ax2, ax3 = axes.flatten()
#
# ax0.hist(np.arange(20),n_bins, density=True, histtype='bar')
# ax0.legend(prop={'size': 10})
# ax0.set_title('LinkedIn Posts & Views')
# ax0.bar(posts,views)
#
# ax1.hist(np.arange(20), n_bins, density=True, histtype='bar')
# ax1.legend(prop={'size': 10})
# ax1.set_title('LinkedIn Posts & Comments')
# ax1.bar(posts,comments)
#
# ax2.hist(np.arange(20), n_bins, density=True, histtype='bar')
# ax2.legend(prop={'size': 10})
# ax2.set_title('LinkedIn Posts & Shares')
# ax2.bar(posts,shares)
#
# ax3.hist(np.arange(20), n_bins, density=True, histtype='bar')
# ax3.legend(prop={'size': 10})
# ax3.set_title('LinkedIn Posts & Likes')
# ax3.bar(posts,likes)


fig1, axes1 = plt.subplots(3)
ax4, ax5, ax6= axes1.flatten()

views_by_jobttitle = dict(Counter(views_by_jobttitle).most_common(5))
print(views_by_location)
ax4.hist(np.arange(len(views_by_jobttitle)), n_bins, density=True, histtype='bar')
ax4.legend(prop={'size': 10})
ax4.set_title('LinkedIn Top 5 Views from Job Title')
ax4.bar(views_by_jobttitle.keys(),views_by_jobttitle.values())


views_by_company = dict(Counter(views_by_company).most_common(5))
ax5.hist(np.arange(len(views_by_company)), n_bins, density=True, histtype='bar')
ax5.legend(prop={'size': 10})
ax5.set_title('LinkedIn Views from Top 5 Company')
ax5.bar(views_by_company.keys(),views_by_company.values())


views_by_location = dict(Counter(views_by_location).most_common(5))
ax6.hist(np.arange(len(views_by_location)), n_bins, density=True, histtype='bar')
ax6.legend(prop={'size': 10})
ax6.set_title('LinkedIn Views from Top 5 Location')
ax6.bar(views_by_location.keys(),views_by_location.values())

# fig.tight_layout()
fig1.tight_layout()
# plt.show()
