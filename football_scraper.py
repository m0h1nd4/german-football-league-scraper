#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for data acquisition of the German Football League (DFB) Results for analysis by a neural network"""

import requests
from bs4 import BeautifulSoup


url = r'https://www.worldfootball.net/schedule/'


def get_var():
    fb_data_links = {}
    seite = requests.get(f'{url}/bundesliga-1963-1964-spieltag/')
    bs4_seite = BeautifulSoup(seite.content, 'html.parser')
    gd_box = bs4_seite.find('div', {'class', 'box2'})
    gd_table = gd_box.find('table', {'class', 'auswahlbox'})
    gd_data = gd_table.find_all('option')
    for link in gd_data:
        if link.get('value'):
            link_data = link['value']
            link_text = link.text
            if not link_text.endswith('Round'):
                fb_data_links[str(link_text).split('/')[0]] = [(str(link_data).split('/')[3]),
                                                               f'{url}bundesliga-{str(link_text).split("/")[0]}-{int(str(link_text).split("/")[0]) + 1}-spieltag/']
    #print(fb_data_links) # debug
    return fb_data_links


def link_generator(link_dict):
    link_list = []
    for key, value in link_dict.items():
        for i in reversed(range(1, (int(value[0]) + 1))): # "reversed.(range)" so that the list is created in the correct order
            link_list.append(f'{value[1]}{i}/')
    return reversed(link_list) # reversed to start with the first year of the Bundesliga


def score_finder(link, x):
    #link = 'https://www.worldfootball.net/schedule/bundesliga-1963-1964-spieltag/30/' # debug
    seite = requests.get(link)
    bs4_seite = BeautifulSoup(seite.content, 'html.parser')
    find_box = bs4_seite.find('div', {'class', 'box'})
    find_table = find_box.find('div', {'class', 'data'})
    tr = find_table.find_all('tr')
    date = None # create variable and fill it later

    for tr_data in tr:
        x += 1 # sequential numbering
        a = (tr_data.text)
        back = '\n' # in the "f''" function no "\" can be used
        try:
            if a.split(back)[1] != "": # if date contains a date set the variable
                date = ''.join([(a.split(back)[1]).split('/')[2], (a.split(back)[1]).split('/')[1], (a.split(back)[1]).split('/')[0]])
        except IndexError as e:
            pass
        try:
            with open(f'ergebniss\ergebnisse.csv', 'a', encoding='utf-8', errors='ignore') as ergebnissfile:
                ergebnissfile.write(f"{x},"
                  f"{date},"
                  f"{int(''.join(a.split(back)[2].split(':')))}," # Time specified as seconds
                  f"{a.split(back)[4]}," # player ONE
                  f"{a.split(back)[8]}," # player TWO
                  f"{(((a.split(back)[11]).split(' ')[0]).split(':')[0])}," # Result player ONE
                  f"{(((a.split(back)[11]).split(' ')[0]).split(':')[1])}," # Result player TWO
                  f"{(((a.split(back)[11]).split(' ')[1]).split(':')[0]).replace('(','')}," # unknown
                  f"{(((a.split(back)[11]).split(' ')[1]).split(':')[1]).replace(')','')}\n") # unknown
        except IndexError as e:
            #print(x, e, a.split(back)) # debug
            with open(f'ergebniss\IndexError.txt', 'a', encoding='utf-8', errors='ignore') as file:
                file.write(f'{x},{a.split(back)}\n')
        except ValueError as e:
            #print(x, e, a.split(back)) # debug
            with open(f'ergebniss\ValueError.txt', 'a', encoding='utf-8', errors='ignore') as file:
                file.write(f'{x},{a.split(back)}\n')
    print(f'{x} - {date}')
    #print(data_list) # debug
    return x # return the numbering to continue in the next round


def file_killer():
    with open(f'ergebniss\ergebnisse.csv', 'w', encoding='utf-8') as f: # deletes the old csv file to be able to fill it again
        f.write('')
    with open(f'ergebniss\ValueError.txt', 'w', encoding='utf-8') as f:  # deletes the old txt file to be able to fill it again
        f.write('')
    with open(f'ergebniss\IndexError.txt', 'w', encoding='utf-8') as f:  # deletes the old txt file to be able to fill it again
        f.write('')


def main():
    file_killer()
    x = 0 # x starts from zero to create a consecutive numbering for each game
    for link in (link_generator(get_var())):
        #print(link) # debug
        x = score_finder(link, x)# must run as "x=" so that x can be returned for consecutive numbering


if __name__ == '__main__':
    main()