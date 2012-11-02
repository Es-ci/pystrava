#!/usr/bin/env python

import operator
import strava

class SegmentMayor :
    def __init__(self,segment_id) :
        self.segment_id = segment_id;
        self.last_segment_effort_offset = 0
        self.seen_seg_rider_list = []
        self.seg_rider_freq_list = []

    def get_segment_offset(self) :
        return self.last_segment_effort_offset

    def count_riders(self,rider) :
        # match the rider using the athlete id, then if we have this rider already then 
        # increment his ride count
        if filter(lambda athl: athl == rider['id'] , [z['id'] for z in self.seg_rider_freq_list]):
            self.seg_rider_freq_list[map(operator.itemgetter('id'),self.seg_rider_freq_list).index(rider['id'])]['rides'] += rider['rides']
        else:
            # otherwise, this is a new rider, let's add her
            self.seg_rider_freq_list.append(rider)

    def ignore_dupes(self,rider) :
        # only add the athlete if he's not in our list
        if rider not in self.seen_seg_rider_list :
            self.seen_seg_rider_list.append(rider)


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
        # needs to get sorted by number of times ridden
        # ef will contain last effort so let's get it's date/time
        # max efforts returned is 50, so we might need to grab the next 50
        #print "Num efforts is %d" % len(efforts_data['efforts'])
        return len(efforts_data['efforts']) == 50
    
    def get_Mayor_of_Mountain(self,effort_offset = 0) :
        s = strava.Strava()
        # need to call this with the save offset if available
        efforts_data = s.get_segment_efforts(self.segment_id,offset = effort_offset)
        #print efforts_data
        #  go through and iterrate over the segment efforts
        # Strava returns 50 ride efforts at a time
        while self.process_efforts_segment_frequency(efforts_data):
            # call get efforts repeatedly
            effort_offset += 50
            efforts_data = {} # clear it
            #print "offset is now %d" % effort_offset
            efforts_data = s.get_segment_efforts(self.segment_id,offset = effort_offset)
        # if this was the last bunch, make sure to add to the offset that last bunch of efforts
        if len(efforts_data['efforts']) < 50 :
            effort_offset += len(efforts_data['efforts'])
        # save the offset so it can be used in future if needed
        self.last_segment_effort_offset = effort_offset
        #print "For Segment id: %d Effort Offset: %d" % (self.segment_id,effort_offset)
        #print "Freq Segment List:"
        #print self.seg_rider_freq_list
        sort_freq_ride_list = sorted(self.seg_rider_freq_list,reverse=True,key=lambda ath : ath['rides'])
        print "\n---- Top 20 Sorted -----"
        for rider in sort_freq_ride_list[:20] :
            print rider
            print "Athlete username: %s Num ridden: %d" % (rider['name'],rider['rides'])

        return sort_freq_ride_list[:20] , effort_offset 

def main():
    segm = SegmentMayor(2021733)
    # offset will be passed in from stored value in db
    segm.get_Mayor_of_Mountain()
    return

if __name__ == '__main__':
    main()
