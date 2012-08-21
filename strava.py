#!/usr/bin/env python

import json
import urllib
import urllib2

class Strava:
	def __init__(self,strava_email = None,token = None):
		self.user_id = None
		self.strava_email = strava_email
		self.token = token
		self.api_url = "http://www.strava.com/api/"

	def call_api(self,url,args=None):
		# need to better handle those exceptions in the caller
		try:
			urlf = urllib2.urlopen(url,args).read()
		except:
			print "Error calling urlopen().read()"
		else:
			return urlf
	
	def is_authenticated(self):
		return self.token != None

	def strava_auth(self,email,password):
		# ssl needed here post, see if we can use https for other apis as well
		url = 'https://www.strava.com/api/v2/authentication/login'
		args = { 'email':email, 'password':password }
		encoded_args = urllib.urlencode(args)
		strava_auth_json =  self.process_strava_json_data(self.call_api(url,encoded_args))
		# save a couple of things
		self.strava_email = email
		self.token = strava_auth_json['token']
		print "Athlete: %s Token: %s" % (strava_auth_json['athlete']['name'],strava_auth_json['token'])
		return

	def process_strava_json_data(self,urlf) :
		# convert strava json
		return json.loads(urlf)

	def get_athlete(self,athlete_id):
		# requires an authetication token
		if athlete_id == None:
			print "athlete id is required"
			return

		if self.is_authenticated() != True:
			print "athlete show api requires authentication. Please use auth method before calling"
			return

		# this requires api ver 2
		api_ver = 2
		ath_api_url = self.api_url + "v%d/athletes/%d?token=%s" % (api_ver,athlete_id,self.token)
		print ath_api_url
		ath_data =  self.process_strava_json_data(self.call_api(ath_api_url))
		print ath_data
		return

	def get_all_bikes(self,athlete_id):
		if athlete_id == None:
			print "athlete id is required"
			return

		if self.is_authenticated() != True:
			print "show bikes api requires authentication. Please use auth method before calling"
			return

		# this requires api ver 2
		api_ver = 2
		bike_api_url = self.api_url + "v%d/athletes/%d/bikes?token=%s" % (api_ver,athlete_id,self.token)
		print bike_api_url
		bike_data =  self.process_strava_json_data(self.call_api(bike_api_url))
		print bike_data
		return

	def get_bike_details(self,athlete_id,bike_id):
		if athlete_id == None:
			print "athlete id is required"
			return

		if bike_id == None:
			print "bike id is required"
			return

		if self.is_authenticated() != True:
			print "show bike api requires authentication. Please use auth method before calling"
			return

		# this requires api ver 2
		api_ver = 2
		bike_api_url = self.api_url + "v%d/athletes/%d/bikes/%d?token=%s" % (api_ver,athlete_id,bike_id,self.token)
		print bike_api_url
		bike_data =  self.process_strava_json_data(self.call_api(bike_api_url))
		print bike_data
		return

	def get_segment_info(self,segment_id):
		if segment_id == None:
			print "segment id is required for getting the segment info"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		segment_id_api_url = self.api_url + "v%d/segments/%d" % (api_ver,segment_id)
		print segment_id_api_url
		segment_id_data =  self.process_strava_json_data(self.call_api(segment_id_api_url))
		print segment_id_data
		return

	def get_club_id(self,club_id):
		# really it's a search for a club id matching the passed string name
		if club_id == None:
			print "club name is required for getting the club"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		club_id_api_url = self.api_url + "v%d/clubs?name=%s" % (api_ver,club_id)
		print club_id_api_url
		club_id_data =  self.process_strava_json_data(self.call_api(club_id_api_url))
		print club_id_data
		return

	def get_club_info(self,club_id):
		if club_id == None:
			print "club id is required for getting the club"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		club_id_api_url = self.api_url + "v%d/clubs/%d" % (api_ver,club_id)
		print club_id_api_url
		club_id_data =  self.process_strava_json_data(self.call_api(club_id_api_url))
		print club_id_data
		return

	def get_club_members(self,club_id):
		if club_id == None:
			print "club id is required for getting the club members"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		club_mem_api_url = self.api_url + "v%d/clubs/%d/members" % (api_ver,club_id)
		print club_mem_api_url
		club_mem_data =  self.process_strava_json_data(self.call_api(club_mem_api_url))
		print club_mem_data
		return

	def get_segment_efforts(self,segment_id,club_id = None,athlete_id = None,athlete_name = None,
			        start_date = None,end_date = None,start_id = None,best = None, offset = None):
		if segment_id == None:
			print "Segment ID is required for effort query"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		effort_api_url = self.api_url + "v%d/segments/%d/efforts" % (api_ver,segment_id)
		# by club id
		if club_id:
			effort_api_url += "?clubId=%d" % club_id
		# by athlete id
		if athlete_id:
			effort_api_url += "?athleteId=%d" % athlete_id
		# by athlete name
		if athlete_name:
			effort_api_url += "?athleteName=%s" % athlete_name
		# by start date. Dates are formatted YYYY-MM-DD
		# startDate: Optional. Day on which to start search for Efforts. 
		# The date should be formatted YYYY-MM-DD. The date is the local time of when the effort started.
		if start_date:
			effort_api_url += "?startDate=%s" % start_date
		# by end date. Dates are formatted YYYY-MM-DD
		if end_date:
			effort_api_url += "?endDate=%s" % end_date
		# by start id
		if start_id:
			effort_api_url += "?startId=%d" % start_id
		# best boolean	
		# best: Optional. Shows an best efforts per athlete sorted by elapsed time ascending (segment leaderboard).
		if best:	
			effort_api_url += "?best=true"
		# strava returns only 50 efforts at a time, offset would be needed for popular segments
		if offset:
			effort_api_url += "?offset=%d" % offset
		# going to start getting into a loop that uses start date over and over in order to build the table
		print effort_api_url
		return self.process_strava_json_data(self.call_api(effort_api_url))

	def process_efforts_segment_frequency(self,efforts_data,segment_freq_dict) :
		# we have the json'ed data from strava, now populate our dictionary
		# in this particular case we're only looking for the segment and how many times it's been ridden
		# by users
		offset = False
		num_effs = 0
		for ef in efforts_data['efforts']:
			num_effs += 1
			if ef['athlete']['username'] not in segment_freq_dict:
				segment_freq_dict[ef['athlete']['username']] = 1
			else:
				segment_freq_dict[ef['athlete']['username']] += 1
		# needs to get sorted by number of times ridden
		# ef will contain last effort so let's get it's date/time
		# max efforts returned is 50, so we might need to grab the next 50
		print "Num efforts is %d" % num_effs
		if num_effs == 50:
			print "Num efforts max of 50"
			offset = True
		return offset
	
	def get_ride(self,ride_id):
		if ride_id == None:
			print "Ride ID is required for effort query"
			return
		# start constructing the api url
		api_ver = 2 # this api is using v2 api
		effort_api_url = self.api_url + "v%d/rides/%d" % (api_ver,ride_id)
		print effort_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(effort_api_url))
		print ride_data

	def get_ride_segment_efforts(self,ride_id):
		if ride_id == None:
			print "Ride ID is required for ride segment effort query"
			return
		# start constructing the api url
		api_ver = 2 # this api is using v2 api
		effort_api_url = self.api_url + "v%d/rides/%d/efforts" % (api_ver,ride_id)
		print effort_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(effort_api_url))
		print ride_data

	def get_ride_effort_for_segment(self,ride_id,ride_segment_id):
		if ride_id == None:
			print "ride id is required for ride effort for segment query"
			return
		# this ride_segment_id is obtained from the segment effort call
		# it's different from the regular segment id
		# poor/confusing strava documentation with regards to how to use this api
		if ride_segment_id == None:
			print "ride segment id is required for ride effort for segment query"
			return
 
		# start constructing the api url
		api_ver = 2 # this api is using v2 api
		effort_api_url = self.api_url + "v%d/rides/%d/efforts/%d" % (api_ver,ride_id,ride_segment_id)
		print effort_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(effort_api_url))
		print ride_data

	def get_effort_info(self,effort_id):
		if effort_id == None:
			print "effort id is required for show ride effort"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v2 api
		effort_api_url = self.api_url + "v%d/efforts/%d" % (api_ver,effort_id)
		print effort_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(effort_api_url))
		print ride_data

	def get_ride_efforts(self,ride_id):
		if ride_id == None:
			print "ride id is required for show ride efforts"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v2 api
		ride_api_url = self.api_url + "v%d/rides/%d/efforts" % (api_ver,ride_id)
		print ride_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(ride_api_url))
		print ride_data

	def get_ride_map_details(self,ride_id,threshold=None):
		if ride_id == None:
			print "ride id is required for show ride efforts"
			return
		# start constructing the api url
		api_ver = 2 # this api is using v2 api
		ride_api_url = self.api_url + "v%d/rides/%d/map_details?token=%s" % (api_ver,ride_id,self.token)
		if threshold != None:
			ride_api_url += "&threshold=%d" % (threshold)
		print ride_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(ride_api_url))
		print ride_data

	def search_ride(self,club_id = None,athlete_id = None,athlete_name = None,
		        start_date = None,end_date = None,start_id = None,offset = None):
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		ride_api_url = self.api_url + "v%d/rides" % (api_ver)
		# by club id
		if club_id:
			ride_api_url += "?clubId=%d" % club_id
		# by athlete id
		if athlete_id:
			ride_api_url += "?athleteId=%d" % athlete_id
		# by athlete name
		if athlete_name:
			ride_api_url += "?athleteName=%s" % athlete_name
		# by start date. Dates are formatted YYYY-MM-DD
		# startDate: Optional. Day on which to start search for rides. 
		# The date should be formatted YYYY-MM-DD. The date is the local time of when the ride started.
		if start_date:
			ride_api_url += "?startDate=%s" % start_date
		# by end date. Dates are formatted YYYY-MM-DD
		if end_date:
			ride_api_url += "?endDate=%s" % end_date
		# by start id
		if start_id:
			ride_api_url += "?startId=%d" % start_id
		# strava returns only 50 rides at a time, offset would be needed for popular segments
		if offset:
			ride_api_url += "?offset=%d" % offset
		# going to start getting into a loop that uses start date over and over in order to build the table
		print ride_api_url
		rides =  self.process_strava_json_data(self.call_api(ride_api_url))
		print rides
		return rides
	
	# XXX this API doesn't seem to work right now
	def search_segment(self,segment_name,offset = None):
		if segment_name == None:
			print "segment name is required for segment search"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v1 api
		segment_api_url = self.api_url + "v%d/segments?name=%s" % (api_ver,segment_name)
		# strava returns only 50 rides at a time, offset would be needed for popular segments
		if offset:
			segment_api_url += "?offset=%d" % offset
		# going to start getting into a loop that uses start date over and over in order to build the table
		print segment_api_url
		segments =  self.process_strava_json_data(self.call_api(segment_api_url))
		print segments
		return segments

	def get_ride_extended_info(self,ride_id = None):
		if ride_id == None:
			print "ride id is required for show ride extended info"
			return
		# start constructing the api url
		api_ver = 1 # this api is using v2 api
		ride_api_url = self.api_url + "v%d/rides/%d" % (api_ver,ride_id)
		print ride_api_url
		# grab ride info from strava
		ride_data = self.process_strava_json_data(self.call_api(ride_api_url))
		print ride_data
		return ride_data

	# test v3 api
	def search_segments_by_latlng(self,start_latlng,end_latlng,zoom=13,min_cat=0,max_cat=5,activity='cycling'):
		if start_latlng == None:
			print "starting latlng required"
			return
		if end_latlng == None:
			print "end latlng required"
			return
		# start constructing the api url
		api_ver = 3 # this api is using v1 api
		segment_api_url = self.api_url + "v%d/segments/search?bounds=%f,%f," % (api_ver,start_latlng[0],start_latlng[1])
		segment_api_url += "%f,%f&zoom=%d&" % (end_latlng[0],end_latlng[1],zoom)
		segment_api_url += "min_cat=%d&max_cat=%d&activity_type=%s" % (min_cat,max_cat,activity)
		# going to start getting into a loop that uses start date over and over in order to build the table
		print segment_api_url
		segments =  self.process_strava_json_data(self.call_api(segment_api_url))
		print segments
		return segments
 
def main():
	return

if __name__ == '__main__':
	main()
