# alpaca-bot
This is a python bot, which can pull market data and place transactions via Alpaca, meant for developpers as a starting template for trading bots.

Licensed under Creative Commons Attribution-NonCommercial 4.0 (no affiliation to Alpaca, this is 3rd party software)
--------------------
# How to run 


![App Screenshot failed to load](https://github.com/rutgervanweehaeghe/alpaca-bot/blob/main/alpacabot_1.png)

--------------
1. open up the python file :

2. Make sure the Python is installed and that the correct dependancies are installed

3. Insert your public and private Alpaca API Keys

4. Change the stock to whatever stock you want to trade (make sure you have the right abreviation)

5. Change the metrics (volume of BUY's SELL's) to whatever you like

6. Make sure the trading hours for your stock match those in the "market_open ()" function (right now they are set for Apple stock)

7. Adjust the trade logic to your liking

8. Run using cmd
9. Type py 'alp_tradingbot.py' in the project folder 

### ! Note how the code runs paper money for now, this can be adjusted in 'BASE_URL' but make sure you know the difference between 'paper' and 'live' (fake money vs real money)
----------------

# Disclaimer

### This software is meant to be a educational tool or module for developers looking to integrate Alpaca API into their trading bot, this software is not meant to be used as a 'finished product' to trade on the stock market, as it is now equiped with the 'trade-logic' to do so. Right now the actual trading logic is minimum and the code is solely meant for developers to have an example of a working framework interacting with Alpaca API, removing the hours spend trying to figure the syntax, and logic of this add-on. For a functioning trading bot, complex trading logic would have to be added. 

### Also, can no assurance be given to the safety or reliability of the software

### The author is not responsible for any losses made trading, using this software ! 

### Trade at your own risk !

