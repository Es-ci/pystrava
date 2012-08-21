#!/usr/bin/env python

import strava

def sort_segment_rider_freq(seg_freq_list) :
	return(seg_freq_list[1])

def get_Duke_of_Mountain(strava,segment_id) :
	effort_offset = 0
	segment_freq_dict = {}
	efforts_data = strava.get_segment_efforts(segment_id)
	#  go through and iterrate over the segment efforts
	# Strava returns 50 ride efforts at a time
	while strava.process_efforts_segment_frequency(efforts_data,segment_freq_dict):
		# call get efforts repeatedly
		effort_offset += 50
		efforts_data = {} # clear it
		#print "offset is now %d" % effort_offset
		efforts_data = strava.get_segment_efforts(segment_id,offset = effort_offset)
	print "For Segment id: %d Total: %d" % (segment_id,len(segment_freq_dict))
	#for username in segment_freq_dict.keys() :
	#	print "Athlete username: %s Num ridden: %d" % (username,segment_freq_dict[username])
       	sort_freq_ride_list = sorted(segment_freq_dict.items(),reverse=True,key=sort_segment_rider_freq)
	
	print "\n---- Top 20 Sorted -----"
	for rider in sort_freq_ride_list[:20] :
		print "Athlete username: %s Num ridden: %d" % (rider[0],rider[1])

	return sort_freq_ride_list

def main():
	s = strava.Strava()
	get_Duke_of_Mountain(s,2021733)
	return

if __name__ == '__main__':
	main()
