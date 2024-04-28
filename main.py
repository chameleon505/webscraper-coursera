import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import argparse


def scrape_coursera_courses():
    course_info = []

    for page_num in range(1, 10):
        url = f'https://www.coursera.org/courses?query=free&page={page_num}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            course_ul = soup.find('ul', class_='cds-9 css-reop8o cds-10')

            if course_ul:
                for course_div in course_ul.find_all('div', class_='css-1evtm7z'):
                    title = course_div.find('h3').text.strip()
                    educator = course_div.find('p').text.strip()
                    rating = course_div.find('p', class_='css-2xargn').text.strip()
                    div = course_div.find('div', class_='cds-CommonCard-metadata')
                    level = div.find('p', class_='css-vac8rf').text.strip().split('·')[0].strip()
                    course_info.append({'title': title, 'educator': educator, 'rating': rating, 'level': level})

        else:
            print(f"Failed to retrieve page {page_num}.")

    return course_info

def search_course(course_title, courses_info):
    found_courses = [course for course in courses_info if course['title'].lower() == course_title.lower()]
    return found_courses.pop()
def search_level(level, courses_info):
    found_titles = [course['title'] for course in courses_info if level.lower() == course['level'].lower()]
    return '\n'.join(found_titles)
def search_rating(min_rating, courses_info):
    found_titles = [course['title'] for course in courses_info if float(course['rating']) >= min_rating]
    return '\n'.join(found_titles)
def search_educator(educator, courses_info):
    found_titles = [course['title'] for course in courses_info if educator.lower() == course['educator'].lower()]
    return '\n'.join(found_titles)
courses = scrape_coursera_courses()
parser = argparse.ArgumentParser(description='Search for Coursera courses by various attributes.')
parser.add_argument('-t', '--title', help='Search courses by title', type=str)
parser.add_argument('-l', '--level', help='Search courses by level', type=str)
parser.add_argument('-e', '--educator', help='Search courses by educator', type=str)
parser.add_argument('-r', '--rating', help='Search courses by rating', type=float)


args = parser.parse_args()

if args.title:
    found_courses = search_course(args.title, courses)
    if found_courses:
        print(found_courses)
    else:
        print("No courses found with the specified title.")
elif args.level:
    found_courses = search_level(args.level, courses)
    if found_courses:
        print(found_courses)

    else:
        print("No courses found with the specified level.")
elif args.educator:
    found_courses = search_educator(args.educator, courses)
    if found_courses:
        print(found_courses)

    else:
        print("No courses found with the specified educator.")
elif args.rating:
    min_rating = float(args.rating)
    found_courses = search_rating(min_rating, courses)
    if found_courses:
        print(found_courses)
    else:
        print("No courses found with the specified rating or higher.")
else:
    df = pd.DataFrame(courses)
    df.to_csv('coursera.csv')
