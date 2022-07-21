import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'https://www.cars.com/shopping/results/?list_price_max=&makes[]=&maximum_distance=all&models[]=&page=1&page_size=100&stock_type=all&zip=91385'
page = requests.get(url)
page

soup = BeautifulSoup(page.text, 'lxml')

columns = ['Year','Make','Model','Used/New','Price','ConsumerRating','ConsumerReviews','SellerType','SellerName','SellerRating','SellerReviews',
           'StreetName','State','Zipcode','DealType','ComfortRating','InteriorDesignRating','PerformanceRating','ValueForMoneyRating',
           'ExteriorStylingRating','ReliabilityRating','ExteriorColor','InteriorColor','Drivetrain','MinMPG','MaxMPG','FuelType',
           'Transmission','Engine','VIN','Stock#','Mileage']   

df= pd.DataFrame(columns=columns)


for i in range(98):
    
    postings = soup.find_all('a', class_ = 'vehicle-card-link js-gallery-click-link')
    current_page = soup
    for post in postings:
        try:
            link = 'http://cars.com' + post.get('href')
            info_page = requests.get(link)
            soup = BeautifulSoup(info_page.text, 'lxml')
            
            ###DELETE THIS WHEN YOURE DONE
            #test_link = 'https://www.cars.com/vehicledetail/1d26a033-1886-4e9c-80cb-fb4f15ff4d51/'
            #info_page = requests.get(test_link)
            #soup = BeautifulSoup(info_page.text, 'lxml')
            
            
            #Data we want
            title_info = soup.find('h1', class_ = 'listing-title').text.split()
            year = title_info[0]
            make = title_info[1]
            model = ' '.join(title_info[2:])
            used_or_new = soup.find('p', class_ = 'new-used').text
            price = soup.find('span', class_ = 'primary-price').text
            consumer_rating = float(soup.find('section', class_= 'sds-page-section vehicle-reviews').find('span', class_='sds-rating__count').text)
            consumer_reviews = int(soup.find('section',class_= 'sds-page-section vehicle-reviews').find('a',class_= 'sds-rating__link sds-button-link').text[1:].split()[0])
            
            #Seller Details
            #Dealer
            try:
                seller_name = soup.find('h3', class_ = 'sds-heading--5 heading seller-name').text
                seller_rating = float(soup.find('section',class_ = 'sds-page-section seller-info').find('span', class_ = 'sds-rating__count').text)
                seller_reviews = soup.find('a', class_ = 'sds-rating__link sds-button-link').text.split()[0][1:]
                seller_type = 'Dealer'
                if ',' in seller_reviews:
                    seller_reviews = int(''.join(seller_reviews.split(',')))
                else:
                    seller_reviews =  int(seller_reviews)
                address_pieces = soup.find('div', class_ = 'dealer-address').text.split(',')
                street_name = address_pieces[0]
                state = address_pieces[1].split()[0]
                zipcode = address_pieces[1].split()[1] 
                
            #Private seller    
            except:
                seller_type = 'Private'
                pieces = soup.find('div', class_ = 'seller-address').text.split('from')
                seller_name = pieces[0].strip()
                address_pieces = pieces[1].split(',')
                street_name = address_pieces[0].strip()
                state = address_pieces[1].split()[0]
                zipcode = address_pieces[1].split()[1] 
    
            
            #Deal type
            deal_type = 'NA'
            first_badge = soup.find('span', class_ = 'sds-badge__label').text
            if 'deal' in first_badge.casefold():
                deal_type = first_badge.split()[0]
            
            #Rating breakdown
            rb = soup.find_all('div', class_ = 'review-breakdown')[0].find_all('span', class_ = 'sds-definition-list__value')
            
            comfort = float(rb[0].text)
            interior_design = float(rb[1].text)
            performance = float(rb[2].text) 
            value_for_money = float(rb[3].text)
            exterior_styling = float(rb[4].text)
            reliability = float(rb[5].text)
            
            #Basic Description Table
            bd = soup.find_all('div', class_ = 'basics-content-wrapper')[0].find_all('dd')
            
            exterior_color = bd[0].text.strip()
            interior_color = bd[1].text.strip()
            drive_train = bd[2].text.strip()
            min_mpg = int(bd[3].text.split('\n')[2].split('–')[0])
            max_mpg = int(bd[3].text.split('\n')[2].split('–')[1])
            fuel_type = bd[4].text.strip()
            transmission = bd[5].text.strip()
            engine = bd[6].text.strip()
            vin = bd[7].text.strip()
            stock_number = bd[8].text.strip()
            mileage = int(''.join(bd[9].text.split()[0].split(',')))
            
            
    
            
            
            
            new_row = pd.DataFrame([[year,make,model,used_or_new,price,consumer_rating,consumer_reviews,seller_type,seller_name,seller_rating,seller_reviews,
                                   street_name,state,zipcode,deal_type,comfort,interior_design,performance,value_for_money,exterior_styling,reliability,
                                   exterior_color,interior_color,drive_train,min_mpg,max_mpg,fuel_type,transmission,engine,vin,stock_number,mileage]],
                                  columns=columns)
            
            #Generate row in dataframe based on scraped information
            df = pd.concat([df,new_row])
        except:
            pass
    
    current_page    
    current_page.find('a', {'aria-label':'Next page'}).get('href')
    next_page = 'http://cars.com' + current_page.find('a', {'aria-label':'Next page'}).get('href') #Get link to next page
        
    url = next_page
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    print(i)

file = 'C:/Users/leave/OneDrive/Documents/Scraped_Datasets/Cars_Data/cars_raw.csv'
df.to_csv(file, index= False)
