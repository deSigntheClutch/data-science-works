from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
import inspect, re
import json

def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)

# url_all = 'https://www.cars.com/for-sale/searchresults.action/?bsId=20203&mdId=36518738&mkId=20028&page=1&perPage=100&rd=99999&searchSource=PAGINATION&sort=price-highest&zc=90007'
# ul = 'https://www.cars.com/for-sale/searchresults.action/?mdId=36518738&mkId=20028&page=1&perPage=100&rd=50&searchSource=PAGINATION&sort=relevance&zc=90007'
# html = urlopen(url_all).read().decode('utf-8')
# file = open('./all_coupe/structure.html', 'a')
# file.write(html)
# file.close()

soup = BeautifulSoup(open('./all_coupe/structure.html'), features='html.parser')

def is_car_details(tag):
    if tag.has_attr('class') == False:
        return False
    return 'listing-row__details' in tag['class']

def has_id(tag):
    if tag.has_attr('data-listing-id') == False:
        return
    return tag['data-listing-id']

def get_valid_data(l):
    for element in l:
        if element == None:
            continue
        return element

res = []

for tag in soup.find_all(is_car_details):
    gen = {}
    data = tag.find_all('li')
    car_ext_color = None
    car_int_color = None
    car_drivetrain = None
    word_list = ['Ext. Color', 'Int. Color', 'Drivetrain']

    for x in data:
        useless = x.find('strong')
        x = str(x)
        for feature in word_list:
            if x.find(feature) != -1:
                tmp = x
                content = tmp.replace(str(useless), '').replace('<li>', '').replace('</li>', '').strip()
                if feature[0] == 'E': car_ext_color = content
                elif feature[0] == 'I': car_int_color = content
                else: car_drivetrain = content
                break

    recommend = tag.find_all(attrs={'class': 'listing-row__badges'})
    car_recommendation = 'None'
    if recommend == []:
        car_recommendation = 'None'
    elif 'data-auto-price-deal' in recommend[0].attrs:
            car_recommendation = recommend[0].attrs['data-auto-price-deal']

    car_certified = len(tag.find_all(attrs={'class':'listing-row__stocktype-cpo'})) > 0
    car_id = get_valid_data(list(map(has_id, tag.find_all('span'))))
    car_name = tag.find_all(attrs={'class':'listing-row__title'})[0].string.strip()
    car_price = tag.find_all(attrs={'class':'listing-row__price'})[0].string.strip()

    car_miles = '0'
    if tag.find_all(attrs={'class':'listing-row__mileage'}) != []:
        car_miles = tag.find_all(attrs={'class':'listing-row__mileage'})[0].string.strip()

    distance_str = tag.find_all(attrs={'class':'listing-row__distance'})[0].string.strip()
    distance_to_me = 100000
    matchObj = re.search('(.*)mi', distance_str, re.M|re.I)
    if matchObj != None:
        distance_to_me = int(matchObj.groups(1)[0].strip())

    print(car_certified, car_ext_color, car_int_color, car_drivetrain)
    print(distance_to_me, car_name, car_price, car_miles)

    detail_url = 'https://www.cars.com/vehicledetail/detail/' + str(car_id) + '/overview/'
    car_details_url = detail_url

    html = urlopen(detail_url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='html.parser')

    feat = []
    if soup.find_all(attrs={'class': 'vdp-details-basics__features-list'}) != []:
        feat = soup.find_all(attrs={'class': 'vdp-details-basics__features-list'})[0].find_all('li')

    features_list = [x.string.strip() for x in feat]

    gen[varname(features_list)] = features_list
    gen[varname(car_details_url)] = car_details_url
    gen[varname(car_recommendation)] = car_recommendation
    gen[varname(car_certified)] = car_certified
    gen[varname(car_ext_color)] = car_ext_color
    gen[varname(car_int_color)] = car_int_color
    gen[varname(car_drivetrain)] = car_drivetrain
    gen[varname(distance_to_me)] = distance_to_me
    gen[varname(car_name)] = car_name
    gen[varname(car_price)] = car_price
    gen[varname(car_miles)] = car_miles

    res.append(gen)


df = pd.DataFrame(res)
df.to_csv('all_amg_coupe.csv', index=False)