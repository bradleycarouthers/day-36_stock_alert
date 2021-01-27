# day-36_stock_alert
Day 36 of 100

For testing purposes I imagined the user is following/invested in Tesla. It takes the cost of the stock at market close yesterday and the day before yesterday to measure the difference.

Then it searches for 3 recent news articles that may explain this difference, whether positive or negative. Finally, it takes each article and sends them to the user as an SMS, along with a message of if the stock has increased or decreased. (I used the graph up and down emojis, respectively)

This way a person can stay updated on pertinent information about their chosen stock(s). A condition is set so the user only gets an SMS if there is a sizable percent difference.
