# -*- coding: utf-8 -*-
"""
Created on Mon Okt 09 20:44:00 2017

Scraping Buzzfeed for quiz titles, with option to break down by category.

@author: Adapted from Elle's tabloid_scrapers.py code (in scrapers repo) by Katie
"""



def get_subgroup_from_user():
    import inquirer
    questions = [
        inquirer.List('subcat',
                message="Pick a subcategory",
                choices=['All Quizzes', 'Personality', 'Disney', 'Can We Guess', 
                    'Food', 'Would You Rather', 'Love', 'Trivia'],
            ),
    ]
    answers = inquirer.prompt(questions)
    answerdict = {'All Quizzes':'?page=', 'Personality':'-personality?page=', 'Disney':'-disney?page=',
        'Can We Guess':'-can-we-guess?page=', 'Food':'-food?page=', 'Would You Rather':'-would-you-rather?page=',
        'Love':'-love?page=', 'Trivia':'-trivia?page='}
    return [answers['subcat'], answerdict[answers['subcat']]]

def get_pagenum_from_user():
    import inquirer
    questions = [
        inquirer.List('pagenum',
                message="Pick a number of pages (only 7 at a time as of now, sorry)",
                choices=[1,2,3,4,5,6,7],
            ),
    ]
    answers = inquirer.prompt(questions)
    return answers['pagenum']

def write_results_to_file(results, basename):
    outfilename = "Results/%s.txt" % basename
    if len(results) >= 1:
        for item in range(0, len(results)):
            # Find out what our file number should be
            file_num = item            
            outfile = open(outfilename, 'a', encoding='utf-8')
            outfile.write(results[item])
            outfile.write('\n')
            outfile.close()

def write_results_to_masterfile(results, basename):
    outfilename = "Results/%s_Master.txt" % basename
    if len(results) >= 1:
        for item in range(0, len(results)):
            if results[item] not in open(outfilename).read(): 
                # Find out what our file number should be
                file_num = item            
                outfile = open(outfilename, 'a', encoding='utf-8')
                outfile.write(results[item])
                outfile.write('\n')
                outfile.close()

def quizScraper():
    from bs4 import BeautifulSoup
    import requests
    import string
    import re
    from selenium import webdriver
    from dateutil import parser
    from datetime import datetime, timedelta
    import time
    import os
    from sys import platform

    ### Get Subgroup from the user ###
    subgroup_tup = get_subgroup_from_user()
    subgroup = subgroup_tup[1]
    subgroup_string = ''.join(subgroup_tup[0].split())

    print(subgroup_string)

    ### Get number of pages from user ###
    pagenum = int(get_pagenum_from_user())


    # Pull the HTML for the page using Selenium--->bs4 pipeline

    for x in range(0, pagenum):
        page_link = "https://www.buzzfeed.com/us/feedpage/feed/quizzes" + subgroup + str(x + 1)
        
        if platform == "linux" or platform == "linux2":
            cwd = os.getcwd()
            browser = webdriver.Chrome(cwd + '/chromedriver')
        elif platform == "win32" or platform == "win64":
            browser = webdriver.Chrome()
        else:
            cwd = os.getcwd()
            browser = webdriver.Chrome(cwd + '/chromedriver')

        browser.get(page_link)
        html = browser.page_source
        browser.close()
        browser.quit()
        soup = BeautifulSoup(html, 'html.parser')
        titles_found = soup.find_all(class_ = "xs-mb05 xs-pt05 sm-pt0 xs-text-4 sm-text-2 bold")
        subheads_found = soup.find_all(class_ = "js-card__description xs-hide sm-block xs-mb1 xs-text-4 text-gray-lighter")
        
        titles = [x.get_text() for x in titles_found]
        subheads = [x.get_text() for x in subheads_found]
        



        #write_results_to_file(titles, (subgroup_string + '_' + datetime.now().strftime("%Y%m%d_%H%M")))
        write_results_to_masterfile(titles, subgroup_string)
        
  

quizScraper()


