# European Travel Recommendation
[Overview Presentation](presentation.pdf)

## Business Understanding
I often find that I have the time, means, and desire to go on vacation, but unless I have family obligations, I have no clue where I should visit. Additionally, I have found that most travel websites can give you specific information about a city of interest, but only if you know where you want to go and that is the problem.

I have created a web application that first measures user interest in five settings that often appear in European cities/regions. I then ask the user for information about previous travel experience in Europe by asking them to rate 10 random European locations. This second step does two things:

* removes that location from potential recommendations
* updates the user's initial setting ratings to be more or less similar to visited cities (based on good or bad experience)

The application then gives the user five recommended cities. Each city's picture also links to the appropriate [Rick Steves](ricksteves.com) entry on the destination.

The recommender system is evaluated by how many of the recommendations the user is interested in.

## Data Understanding
Selenium was used to scrape text summaries from [ricksteves.com](ricksteves.com) as well as [Wikipedia](wikipedia.com). These text summaries along with `City`, `Country` names and URLs are stored in a MongoDB Atlas database.

I additionally scraped photos from Rick Steves for use on the website. 

Note: the XPath I used for images has changed since I completed scraping for the project. 
[Scraping Notebook](collect_data.ipynb)

## Data Preparation
I used NLTK and gensim to tokenize, lemmatize, and stem all city text summaries. I used these text summaries to perform LDA topic modeling and my initial topics were accurate topics, but they were topics such as "French", "European", or "King Henry" which are not helpful for the business problem. I added to the gensim's default list of stopword all names (country, city, or person) I saw in the topic modeling.

From LDA modeling I discovered 5 clear topics:
* Forest/Mountain
* Palaces/Castles
* Coastal/Water
* Historical
* Urban

Once I had the LDA model, I scored each summary by the probability it belonged to a topic. I then used the average of the Rick Steve and Wikipedia summary scores to give each city an aggregate score for each topic.

I also had to ensure that `St. Petersburg` and `St. Andrews` did not have a period as the period breaks the model.

[Data Preparation and Topic Modeling Notebook](data_preparation.ipynb)

## Modeling
I created a cold start recommendation system that uses nearest neighbors with Euclidean distance to make recommendations. The model takes in user scores on the same five topics and gives back the 50 closest neighbors in order of closest to farthest. Ten of these 50 are then randomly selected to collect information on the user's previous experience. If one of these ten cities has been visited by the user, the initial topic ratings are adjusted by becoming more similar to visited cities they liked, and less similar to visited cities that they disliked. These previous experience ratings are also saved in MongoDB for future implementation of an ALS model. The updated ratings go back into the nearest neighbors model, a new 50 closest are generated (removing any visited cities), but only the top 5 are shown to the user. 

[Modeling Notebook](recommend_by_nearest_topic_score.ipynb)

## Evaluation
As this was an unsupervised learning model, I am unable to evaluate objectively using metrics such as accuracy, recall, roc, etc.
Therefore, I implemented a subjective evaluation tool for the application. The user has the opportunity to give a thumbs up and thumbs down to the destinations they have been recommended. I then collected this information in a MongoDB Atlas database.

Preliminary results show that users are interested in about 67% of their recommendations. However, this number is not reflective of the population as a whole with only 32 samples, which were also subject to sample bias most (if not all) of these samples are from people in my network. Additionally, a few of these samples may be from when I was checking to make sure the website was working.

[Evaluation Notebook](evaluate_results.ipynb)

## Deployment
The model is deployed as a Flask app on the website [triprecommender.online](www.triprecommender.online). 

When the user gets to the website they will be asked to use a slider bar to rate the 5 settings determined from topic modeling on a scale of 0 to 10. When the user selects `Next`, they will scroll down to a new section asks users to rate previous experience. 

This section has the ten random cities selected from the 50 generated by the nearest neighbors model. The user will then use a slider bar to the left if they have been to the location and did not like it, or to the right if they have been to the location and liked it. The slider bar will be kept in the center if the user has not been to the destination. The user then selects a button `Get My Recommendations!` to show their recommendations.

In the recommendations section, the user is prompted to indicate if they are interested in visiting the city. The user submits feedback by selecting the `Submit Feedback` button. If the user would like more information they are also instructed to click on the picture. When this occurs a pop-up with the Rick Steves summary and a link to the city page on his website are shown. If the link is selected, it will open in a new tab.

To run the flask app locally, clone this repository and enter into the terminal:

```FLASK_APP=travel_destination_recommendation.webapp.app flask run```

## Future Exploration
Part of collecting information about the ten random cities is to collect enough information for a true ALS recommender model that I could build in the future.

I want to collect more summaries about each destination so that more topics could be generated in the LDA model. As it currently stands, I have two sets of summaries for 213 destinations, which is not a very large sample. With more data, I would hope to better fit each city into the topics. 

I want to expand this project beyond just European travel. 
