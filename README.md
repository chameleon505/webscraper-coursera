# webscraper-coursera
Python script for scraping and searching Coursera courses with automatic CSV export functionality



## Usage

Run the script using Python 3.9 or above, and provide command-line options to search for courses based on their attributes. If no options are provided, the script will automatically generate a CSV file named coursera.csv containing all course information.


```bash
python script.py -t "Python"        # Search courses by title
python script.py -l "Intermediate"  # Search courses by level
python script.py -r 4.5             # Search courses by rating
```
## Dependencies


Python 3.9+
BeautifulSoup4
Requests
Pandas
