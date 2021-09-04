'''
Author: Jess Summerhill
Project: A sport betting analytics web scrapper
Date: 6-7-2020

Project Specs:
In this project, I going to hardcode a date range for the client to get a data set from,
so he can build his or her models.
Future requirements will be needed to improve specifications 

'''


import sports_fout as spf, requests as req
from collections import defaultdict as dd
from bs4 import BeautifulSoup as bsoup
from datetime import date as dt, timedelta as timed

class SportsWebScraper:
    def __init__(self):
        return None

    def main(self):
        # Get the main URL
        rurl = "https://www.teamrankings.com"
        burl = "https://www.teamrankings.com/nfl/team-stats/"

        wsrc = req.get(burl)

        # Setup xpaths
        bsoupy = bsoup(wsrc.content, 'lxml')

        # setup all my functions
        def get_team_names(soupy, root):
            # Find all the team names, and save them to a new list.
            teams = []
            new_url = ""
            expanded = soupy.find_all("ul", {"class": "expand-content hidden"})

            for e in expanded:
                tnames = e.find("a", href=True).get_text()
                if tnames == "Points per Game":
                    turl = e.find("a", href=True)
                    new_url = root + turl.get('href')
                    break

            nreq = req.get(new_url)
            nnsoupy = bsoup(nreq.content, 'lxml')
            nno_wrap = nnsoupy.find_all("td", {"class", "text-left nowrap"})

            for n in nno_wrap:
                tname = n.find("a", href=True).get_text()
                teams.append(tname)
            return teams

        def get_key_names(soupy):
            # Get all of the Titles from all the stats
            key_names = []
            choosey = soupy.find("ul", {"class", "chooser-list"})
            expanded = choosey.find_all("li")

            for e in expanded:
                ehyper = e.find("a", href=True)

                if ehyper.get('href') != '#':
                    tnames = ehyper.get_text()
                    key_names.append(tnames)
            return key_names

        def get_stat_urls(soupy, root, dt_str):
            # Find all of the stat URLs
            surls = []
            choosey = soupy.find("ul", {"class", "chooser-list"})
            expanded = choosey.find_all("li")

            for e in expanded:
                ehyper = e.find("a", href=True)

                if ehyper.get('href') != '#':
                    url = root + ehyper.get('href') + dt_str
                    surls.append(url)

            return surls

        def req_get_wrapper(l, urlsl = []):
            # get the request from the url list, and then save the first column of data
            surl = urlsl[l]

            rsrc = req.get(surl)
            # get a new request from a new url
            ssoup = bsoup(rsrc.content, 'lxml')

            nwrapy = ssoup.find_all("td", {"class", "text-left nowrap"})

            return nwrapy

        key_list, urlstat_list, wrappers, sdict_list, team_list = [], [], [], [], []
        key1 = "Team Names"

        team_list = get_team_names(bsoupy, rurl)
        key_list = get_key_names(bsoupy)

        start_date = dt(month=9, day=2, year=2019)
        end_date = dt(month=1, day=6, year=2020)

        while start_date < end_date:
            start_date += timed(days=7)
            dtstring = "?date=" + str(start_date)
            urlstat_list = get_stat_urls(bsoupy, rurl, dtstring)

            data_dict = dd(dict)
            for t in team_list:
                data_dict[t][key1] = t

            wrappers = []
            for idx in range(0, len(urlstat_list)):
                wrappers.append(req_get_wrapper(idx, urlstat_list))

                for wr in wrappers[idx]:
                    team_name = wr.find("a", href=True).get_text()
                    data = wr.find_next("td").contents[0]
                    colname = key_list[idx]
                    data_dict[team_name][colname] = data

            for key, val in data_dict.items():
                sdict_list.append(val)

            dt_filename = start_date.strftime("%m_%d_%Y")

            fname = spf.sfout.dt_file_format(dt_filename)
            spf.sfout.output_csvfile(fname, key1, key_list, sdict_list)
            sdict_list = []

        return None

s_scrap = SportsWebScraper()

s_scrap.main()
