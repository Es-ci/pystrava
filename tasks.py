from functools import partial
from celery import task, chord

from mayorly.strava import Strava
from mayorly.strava_util import SegmentMayor

@task(name='tasks.get_segment_efforts_for_given_offset')
def get_segment_mayors_offset(strv,segment_id,offset) :
    print "Start segId: %d api for offset: %d" % (segment_id,offset)
    efforts_data = strv.get_segment_efforts(segment_id,offset=offset)
    return efforts_data

@task(name='tasks.merge_segment_mayor_results')
def merge_segment_mayor_results(segment_efforts) :
    combine_segment_efforts = partial(combine_efforts,efforts=segment_efforts)
    # starting from second entry till end. Merge with first entry
    map(combine_segment_efforts, segment_efforts[1:])
    # now trim and only leave the first entry after the merge
    map(lambda entry : segment_efforts.remove(entry), segment_efforts[1:])
    print "Merge complete size returned: %d" % (len(segment_efforts[0]['efforts']))
    return segment_efforts

def combine_efforts(effort_item,efforts=None) :
    # each api call will return an effort dict containing a list of the efforts
    # let's append to the first list entry
    # XXX need to add a check for efforts not None
    for ef in effort_item['efforts'] :
        efforts[0]['efforts'].append(ef)
    return

def is_segment_task_pending(task_id) :
    # problem is that celery returns 'PENDING' even for a 
    # nonexiting task id

    # if our db task id is 0 then we want to start a task
    if task_id == '' :
        pending = 'NOT PENDING'
    else:
        print task_id
        pending = merge_segment_mayor_results.AsyncResult(task_id).status 
    return pending == 'STARTED'

def get_mayors_task_status(task_id) :
    return merge_segment_mayor_results.AsyncResult(task_id).status

def get_mayors_task_results(task_id) :
    # Make sure this is called with a valid task_id, otherwise it will block.
    mayor_results = merge_segment_mayor_results.AsyncResult(task_id).get()
    seg_id = mayor_results[0]['segment']['id']
    print seg_id
    seg_util = SegmentMayor(seg_id)
    seg_util.process_efforts_segment_frequency(mayor_results[0])
    return seg_util.get_segment_top_mayors()

def get_Mayor_of_Mountain(segment_id,num_rides) :
    #print "Grabbing strv inst for rides " + type(num_rides)
    # grab a strava instance
    strv = Strava()
    # create subtasks headers for segment
    result_list = [get_segment_mayors_offset.subtask((strv,segment_id,offset)) for offset in xrange(0,num_rides,50)]
    print result_list
    # barrier callback aka body
    segment_done_callback = merge_segment_mayor_results.subtask()
    async_result = chord(result_list)(segment_done_callback)
    return async_result.id
