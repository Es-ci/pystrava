#!/usr/bin/env python

import operator
from bs4 import BeautifulSoup
import urllib2
import json
import re

class SegmentRoute :
    def __init__(self, api_key, **kwargs) :
        """
        SegmentRoute class can be instantiated by either the segment id
        or by the start and end latlng.
        Instantiating object by the latlng (if they are known), saves the
        segment api query. The cloudmade api key is needed for the route
        lookup.
        SegmentRoute(API-KEY,start = [a,b], end = [c,d])
        SegmentRoute(API-KEY,segment_id=12345)
        """
        self.api_key = api_key
        self.segment_id = kwargs.get('segment_id',0)
        start = kwargs.get('start',[])
        end = kwargs.get('end',[])
        self.segment_latlng = {'start' : start, 'end' : end}

    def get_segment_route_by_id(self) :
        # strava segment query then route call
        pass

    def get_segment_route_by_latlng(self) :
        """
        We have the start and end lat lng so go grab the route 
        Expecting segment_latlng to be formatted as follows:
        {'start':[x,y],'end':[w,z]}
        """
        start = ','.join([str(point) for point in self.segment_latlng['start']]) 
        end = ','.join([str(point) for point in self.segment_latlng['end']]) 
        cloud_url = 'http://routes.cloudmade.com/' + self.api_key + '/api/0.3/'
        url = cloud_url + self.segment_latlng['start'] + ',' + self.segment_latlng['end'] + '/bicycle.js'
        try:
            urlf = urllib2.urlopen(url).read()
        except:
            print "Error calling urlopen().read() cloudmade site down ?"
        else:
            json_cloudmade_rt = json.loads(urlf) 
        json_rt = json_cloudmade_rt.get('route_geometry',[])
        return json_rt

class SegmentMayor :
    def __init__(self,segment_id) :
        self.segment_id = segment_id;
        self.last_segment_effort_offset = 0
        self.seen_seg_rider_list = []
        self.seg_rider_freq_list = []
        return

    def get_segment_offset(self) :
        return self.last_segment_effort_offset

    def get_segment_ride_numbers(self) :
        # we're looking for this pattern : "Ridden|Hiked|etc.. XX Times By YY People"
        # css is capitalizing it, so don't rely on the capitilization
        # group the numbers
        # XXX consider memoization and caching this
        ride_pattern = r'\s+(\d+)\s+\w+\s+\w+\s+(\d+)'
        segment_url = "http://app.strava.com/segments/" + str(self.segment_id)
        try:
            ride_page = urllib2.urlopen(segment_url)
        except:
            print "Error calling urlopen(), is Strava down ?"
        else:
            # success think about using with lxml for some extra speed
            soupy = BeautifulSoup(ride_page)
            segment_text = soupy.find_all(text=True)
            for l in segment_text:
                pattern_match = re.search(ride_pattern,l)
                if pattern_match:
                    return [int(num) for num in list(pattern_match.groups())]
        return [0,0] # improve this XXX

    def get_how_many_rode_segment(self) :
        # get_segment_ride_numbers returns a list, with people who rode|hiked
        # is the second element in list
        return self.get_segment_ride_numbers()[1]

    def get_num_of_times_ridden(self) :
        # get_segment_ride_numbers returns a list, with times ridden|hiked
        # the first element in list
        return self.get_segment_ride_numbers()[0]

    def count_riders(self,rider) :
        # match the rider using the athlete id, then if we have this rider already then 
        # increment his ride count
        if filter(lambda athl: athl == rider['id'] , [z['id'] for z in self.seg_rider_freq_list]):
            self.seg_rider_freq_list[map(operator.itemgetter('id'),self.seg_rider_freq_list).index(rider['id'])]['rides'] += rider['rides']
        else:
            # otherwise, this is a new rider, let's add her
            self.seg_rider_freq_list.append(rider)
        return

    def ignore_dupes(self,rider) :
        # only add the athlete if he's not in our list
        if rider not in self.seen_seg_rider_list :
            self.seen_seg_rider_list.append(rider)
        return

    def get_segment_top_mayors(self):
        sort_freq_ride_list = sorted(self.seg_rider_freq_list,reverse=True,key=lambda ath : ath['rides'])
        #print "\n---- Top 20 Sorted -----"
        #for rider in sort_freq_ride_list[:20] :
            #print "Athlete username: %s Num ridden: %d" % (rider['name'],rider['rides'])

        return sort_freq_ride_list[:20]

    def process_efforts_segment_frequency(self,efforts_data) :
        # we have the json'ed data from strava, now populate our dictionary
        # in this particular case we're only looking for the segment and how many times it's been ridden
        # by users
        athlete_list = [ath['athlete'] for ath in efforts_data['efforts']]
        map((lambda athl,num_rides : athl.setdefault('rides',num_rides)),athlete_list,[athlete_list.count(athl) for athl in athlete_list])
        # have to get rid of dupes first
        filter(self.ignore_dupes,athlete_list)
        # then add rides after we've eliminated the duplicates from list
        filter(self.count_riders,self.seen_seg_rider_list)
        # clear list again
        self.seen_seg_rider_list = []
        return
   
    def process_next_segment_efforts(self,efforts_data) :
        # process the next page(50 efforts) of efforts
        process_efforts_segment_frequency(efforts_data)
        # needs to get sorted by number of times ridden
        # ef will contain last effort so let's get it's date/time
        # max efforts returned is 50, so we might need to grab the next 50
        #print "Num efforts is %d" % len(efforts_data['efforts'])
        return len(efforts_data['efforts']) == 50

def main():
    segm = SyncSegmentMayor(2021733)
    # offset will be passed in from stored value in db
    # XXX need to be rewritten
    segm.get_Mayor_of_Mountain()
    return

if __name__ == '__main__':
    main()
