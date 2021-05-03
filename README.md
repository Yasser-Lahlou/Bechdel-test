## Bechdel Test app

[Go to Streamlit app](https://share.streamlit.io/yasser-lahlou/bechdel-test/main)

## What is the Bechdel Test ?
The Bechdel test, also known as the Bechdel–Wallace test, is a measure of the representation of women in fiction. It asks whether a work features at least two women who talk to each other about something other than a man.
For more information, please check the Bechdel Test page on [Wikipedia](https://en.wikipedia.org/wiki/Bechdel_test)

## How does the app work ?
Two main steps were required :
* Script scraping and parsing with **scripts_parser.py**
* Script text processing and implementation of the 3 tests with **functions.py**

The app wraping is done with the remaining python script **streamlit.app.py**

## scripts_parser.py
The Internet Movie Script Database (https://imsdb.com/all-scripts.html) contains more than 1000 movie scripts.
The Scraping, done with BeautifulSoup, consists on collecting all the urls on the index page, then doing the same with each individual url found.
Scripts and Script index are then stored in .txt files and .csv file respectively.

NB : Empty and small files were dropped

## functions.py
Various functions are used to :
* generate lists of female and male common male_names
* break a script into scenes (using scene headings)
* extract characters talking in a scene (assuming character names are centered in the page)
* count female characters in a script or a scene
* tokenize dialogues to look for male names (using sklearn CountVectorizer)
* and finally perform the 3 test requirements

## Credits
The movie scripts were provided by [The Internet Movie Script Database](https://imsdb.com/all-scripts.html).
Common female and male lists were provided by Mark Kantrowitz (Copyright (c) January 1991). Thanks to Bill.Ross for the additional names.

![](https://github.com/Yasser-Lahlou/Colorization-app/blob/main/data/Bechdel_test_app_screenshot.png)
