# Cars.com-Data-Project
Data scraped and analyzed from Cars.com

The goal of this project was to build a web scraping script in Python using the BeautifulSoup package. I was able to scrape data from over 9,000 car posts on Cars.com.

The code starts by importing the required libraries, such as requests, BeautifulSoup, re and pandas, and defining the URL of the page that needs to be scraped.

Then, the script uses the requests library to retrieve the content of the webpage and the BeautifulSoup library to parse the HTML content of the webpage. The script then creates an empty Pandas DataFrame with column headers defined.

Next, a loop is set up to navigate through the listings on the page, with each iteration of the loop collecting information from a single car listing on the webpage. The information gathered includes details such as year, make, model, used/new, price, consumer rating, consumer reviews, seller type, seller name, seller rating, seller reviews, street name, state, zipcode, deal type, comfort rating, interior design rating, performance rating, value for money rating, exterior styling rating, reliability rating, exterior color, interior color, drivetrain, min/max mpg, fuel type, transmission, engine, VIN, stock #, and mileage.

The script then stores this information in the empty Pandas DataFrame and continues to iterate through the listings on the page. Finally, the DataFrame is exported to a CSV file.

I posted the scraped data on https://www.kaggle.com/datasets/chancev/carsforsale and created a challenge for data science student to practice their data skills. The challenge includes several objectives, such as removing symbols from the price variable and converting it into an integer, changing all the different types of certified values into one certified category, removing rows from the data where the drivetrain value is '-', creating dummy variables for appropriate categorical variables, creating a regression model to predict a car's price, or a classification model to predict a car's drivetrain, and exploring the data further to find other insights. The challenge requires data cleaning, data manipulation, and modeling skills, making it an excellent opportunity for data science students to enhance their skills and gain practical experience.

The dataset posted on kaggle as over 10,000 views and over 1500 downloads. I interacted with kaggle community members who posted code notebooks to attemp the challenge and gave them feedback on their data handling skills!
