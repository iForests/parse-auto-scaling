# parse-auto-scaling

## The Problem

[Parse](https://parse.com/) requires you to manually adjust the request limit, but it's not an easy task especially in the middle of the night. If  the request limit of your app is regular at a specific time, this script could help you save time and money.

#### Before:

![Before](https://raw.githubusercontent.com/iForests/parse-auto-scaling/master/images/before.png)

#### After:

![Before](https://raw.githubusercontent.com/iForests/parse-auto-scaling/master/images/after.png)

## Installation

Install [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/), [pytz](http://pytz.sourceforge.net/), and [requests](http://www.python-requests.org/en/latest/) before you run the script:

    pip3 install beautifulsoup4 pytz requests
    
## Settings & Usage

## Not Implemented (yet)

* Error handling
	* Wrong e-mail or password
* Get the csv file of the served requests, predict the appropriate request limits, and automatically adjust it.
