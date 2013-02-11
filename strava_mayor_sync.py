from strava import Strava
from strava_util import SegmentMayor

class SyncSegmentMayor(SegmentMayor) :
    def __init__(self,segment_id):
        SegmentMayor.__init__(self,segment_id)

    def get_Mayor_of_Mountain(self,effort_offset = 0) :
        s = Strava()
        s_util = SegmentMayor(self.segment_id)
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
    
        return s_util.get_segment_top_mayors()
