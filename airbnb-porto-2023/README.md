# Airbnb Data Analysis - Porto 2023 

Table of Contents:
1. Requirements
2. File Descriptions
3. Data
4. Project Motivation
5. Summary of the Analysis
6. Acknowledgements
7. Author

---
## 1. Requirements
To run the code you need the following software:
- Python v.3+
- Jupyter Notebook
- Suggestion: Anaconda v.4+ since it has both in one suite.

Additionally, you need to unpack the zip file _../model/calendar.csv.gz_ in the same directory. 
  
## 2. File Descriptions
- _airbnb-porto-2023-eda.ipynb_: Jupyter Notebook, which contains the full code.
- _202206-listings.csv_: Snapshot of Airbnb listing's data from Q2 2022
- _202209-listings.csv_: Snapshot of Airbnb listing's data from Q3 2022
- _202212-listings.csv_: Snapshot of Airbnb listing's data from Q4 2022
- _202303-listings.csv_: Snapshot of Airbnb listing's data from Q1 2023
- _202303-calendar.csv_: Snapshot of Airbnb activity's data from Q1 2022 (obtained from the zip file: _calendar.csv.gz_)

## 3. Data
The data was obtained from the website <a href=http://insideairbnb.com/get-the-data/>Inside Airbnb</a> and it is made of four CSV files - which contains listing information - and one CSV file with activity information. The listing files are the focus of the project while the calendar.csv was only used once for a quality check.

The listing's data contains, among others, these columns:
- id
- name
- description
- host_is_superhost
- neighbourhood
- property_type
- bedrooms
- beds
- bathrooms
- amenities
- price
- availabity_90
- number_of_reviews
- review_scores_rating
- etc.

The data dictionary of the columns can be found [here](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit#gid=1322284596).

### Limitations of the data
Although there is relevant information available about the listings, there are still some features missing which may influence the analysis, especially when trying to predict the price, the occupancy or explaining causality for something interesting we may see in the data. This list is not exhaustive but gives an overview of these limitations:
- This data is composed of quarterly snapshots, which means that numbers like availability rates may have changed over the time.
- Information about state of the listing (brand new/used) is not available.
- Size of the listing is not available.
- Other subjective factors cannot be measured like decoration, natural light, overall attractiveness, etc.
- Only the last 12 months of data were available.


## 4. Project Motivation
This project was done as part of the curriculum of the [Udacity's Data Scientist Nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025). I decided to choose this analyis due to various reasons:
- I am natural from Porto, Portugal and I am interested in Airbnb market of that region.
- Since around 2015, the country has seen a dramatic increase in tourists and real estate prices. Then, in 2019 the COVID pandemic hit the region hard and since 2022 things seem to be recovering.

The __main goals__ of this project were to investigate:
1. How the numbers of listings, prices and overnights were evolving after the pandemic.
2. How the occupancy rate was generally distributed - for example whether superhosts in general had higher occupancy rates.
3. Whether it was possible to create a predictive model for the price per night based on the available data. 


## 5. Summary of the Analysis
Like many data analysis projects start, the first thing I wanted to see is how the data looks like: which portion of the data is missing, which columns hold important information or to look at the distribution of the continuous variables. In this case, I was interested to see how the __price distribution__ looked like, since I was using it later as my target variable for the model.
![Price density map](images/price_density_map.png)

As one can see the distribution is so skewed to the right that the curve of the distribution is almost a straight line in the graphic. This is due to the fact that there are few, but very extreme values in this dataset - the so-called outliers. The highest price per night one could pay in Porto based on Q1 2023's data was $80100. I knew directly I needed to address this later and I also decided to use the median instead of the mean for the further analyses, as it is less sensitive to outliers.

You may find more analyses like this in the [Jupyter notebook](https://github.com/bruno-f7s/portfolio/blob/main/airbnb-porto-2023/airbnb-porto-2023-eda.ipynb). Below, you can find a summary of the relevant findings related to the initial business questions.

### Evolution of the number of listings, prices and occupancy rates
The data I gathered reaches from Q2 2022 until Q1 2023. This means 12 months of historical data that coincide with the "end" of the pandemic, when people could start to travel again with less restrictions. Looking at the number of Airbnb listings available for this time period, we can see that the hosts were also probably expecting an increase in tourists:

![Number of listings by period](images/bar_listings_period.png)

Of course, we do not know the causes for this or if the trend was already there before, but looking at the data at hand we can see some optimism in the market. This is however not valid for all cities of the Porto metropolitan area: some cities had a decrease in the number of offerings (more info in the Jupyter notebook).

Regarding the __occupancy rates__ the picture is a bit different:

![Occupancy rates by period](images/bar_occupancy.png)

Looking at the graphic above, we see a decrease of the occupancy rates in the colder months, which is somewhat expected since most of the listings are likely dependent on tourism and the number of tourists tends to decrease in the northern hemisphere during this time period. To evaluate if these numbers are high or not, more historical data would have been needed. Nevertheless, we can have an estimate based on statistic reports. The official  Portuguese tourism agency reports that the average occupancy rate for this region in 2018 was around 73% (for hotels), so this could be used as a rough estimate ([source](https://travelbi.turismodeportugal.pt/alojamento/taxas-de-ocupacao-quartocama/)). In the data I gathered, the mean value was 51%, which means that occupancy rates are still far behind the pre-pandemic numbers. 

This distribution of the occupancy rates by period looks very similar across the different cities of the region:

![Occupancy rates by period by city](https://github.com/bruno-f7s/portfolio/assets/68636948/2e9e1173-244d-45c6-9fb5-b6f2f2b4c118)

As for the median __prices per night__, we also see a different picture:

![Price per night by period](https://github.com/bruno-f7s/portfolio/assets/68636948/a059757f-1577-4785-a5ba-d667d60f1017)

In this case the median price per night decreased in the second half of the period. It is difficult to explain this just by looking at this graphic and I decided not to focus too much on this explanation as it would have involved combining features with each other, which was too complex for this scope. Instead, I investigated how the price was distributed by some single features and below one can see the median price per number of rooms of an Airbnb listing:

![Price per night by number of bedrooms](https://github.com/bruno-f7s/portfolio/assets/68636948/41324cb3-f492-4156-a648-0265afca26d5)

Here we can clearly see that as the number of bedrooms per listing increases, so does the median price. The drops at 10 and 14 bedrooms caught my eye and I decided to analyze it further. It turned out that these two categories had a small amount of listings and referred to hostels or other shared accommodations, not an entire housing unit.

Another aspect I investigated was the number of reviews vs the median price per unit (until $500), in this case just for the last quarter: 

![Price vs number of reviews](https://github.com/bruno-f7s/portfolio/assets/68636948/57d8a029-6b3e-4728-81c4-add17e8134d8)

The scatterplot above shows that there is not any strong correlation between the two features.

### Distributions of the occupancy rate
I decided to put some focus on the occupancy rate because it is what any host strives to achieve, so I wanted to investigate which interesting findings this data could show. Intuitively humans tend to follow what others do/like or are interested in others' opinions, and when we are buying something from the internet we usually search for reviews from prior customers. I wanted to see if with increased number of reviews the occupancy rates also increased:

![Occupancy rate by number of reviews](https://github.com/bruno-f7s/portfolio/assets/68636948/caa2d361-f8ba-4b93-af3d-c99b9921dc6c)

The graphic clearly shows a positive trend. Of course, one thing can lead to another, but this can still be a good assumption because (1) not every guest leaves a review and (2) the listings with higher reviews have been visited before and therefore new occupancies are not changing that numbers. This occupancy rate we are looking at is actually referring to the next number of days an unit is sold within the next 90 days.

Another thing I thought it might be worth looking at, was if superhosts (which typically are a good reference for a guest) actually had higher occupancy rates than the normal hosts.

![occupancy rate by host by period](https://github.com/bruno-f7s/portfolio/assets/68636948/1a242dea-fd3c-4677-b759-9577899b5c7c)

The table above shows some interesting information: In the colder months, when the occupancy rate is generally lower, the regular hosts had a higher average occupancy rate and in the higher season the superhosts actually had a higher average occupancy rate. It seems that as the occupancy rate increases, so the difference of the average occupancy rates between the two types of hosts increases. This trend of course cannot be validated using only this amount of data, but it was an interesting fact nonetheless.

Finally, I looked at the whole distribution of the listings by the occupancy rate for these two categories of hosts:

![listing distribution by occupancy rate by host](https://github.com/bruno-f7s/portfolio/assets/68636948/6315650a-c399-43f8-b7d2-5254ed0d5b4d)

Looking at the superhosts (in orange) we see that the number of listings they have is almost uniformly distributed accross all levels of occupancy rates. As an example, we can assume that a similar amount of listings from superhosts had a 20% and 80% occupancy rate. The picture changes for the non-superhosts (in blue): we can see that the majority of the non-superhosts' listings have lower occupancy rates, but we also see a big amount of them concentrated at around 100%. This is particularly interesting because there are some non-superhosts which are practically sold-out all the time.

### Predicting the price per night of an Airbnb Unit
To train the model, I needed to make some feature selection and transformation. In summary, I used all relevant information about a listing like number of bedrooms, beds, bathrooms, how many guests it could accommodate, its location and some types of amenities it offered. I left out some features like the number of reviews or occupancy rates for various reasons. For example, the 90-day occupancy rate or number of reviews do not have any strong correlation with the price and if the listing is new these values will always be 0.

I only used the last period of data (Q1 2023) because I was not interested in the evolution of the prices between of the last 12 months but rather focus on the current situation. As we saw with the pandemic, external events can have a lot of influence so prices may be affected by sudden changes.

Finally, I also decided to only include listings that had a maximum price per night of $500 and to remove the outliers (0.7% of the total). Although this may be an important information, we might have not been able to explain these extreme prices with the data at hand. For example, an important factor missing here was the size of the listing. Also, my goal was to predict a listing that is somehow realistic in a normal context. I personally think that after a certain threshold of luxury you are free to dictate the price.

Based on these assumptions I trained the model that achieved a root mean squared error (RMSE) of about $41, which is not great in this context (the standard deviation of this price distribution was around $60). This means that our prediction could have a deviation of $41 and still be considered "normal" when comparing to the rest. If we are looking at a $400 unit then this might not be a problem, but for cheaper listings this could make a big difference. However, looking at the median price distribution and the limitations in our dataset this is actually not completely wrong.

I then used a listing for prediction with some features based on an actual listing I know, and the prediction was $63. By knowing well some of the details of this listing using some information not captured in this dataset, I would use the error to inflate the price a little - probably not to the maximum but maybe halfway and put the appartment for rental at around $85 per night.

## 6. Acknowledgements
- I would like mention to the website <a href=http://insideairbnb.com/get-the-data/>Inside Airbnb</a> from where I retrieved this project's data, because the team there did an amazing job in keeping data up-to-date for numerous cities worldwide. Feel free to check the website in case you want to do a similar analysis for your hometown.
- I would like to mention that I got some writing inspirations from [Robert Chang](https://medium.com/@rchang) for this project.

## 7. Author
Bruno Fernandes - Data Analyst & Enthusiast - [LinkedIn](https://www.linkedin.com/in/b-fernandes/) - [Xing](xing.to/brunofernandes)
