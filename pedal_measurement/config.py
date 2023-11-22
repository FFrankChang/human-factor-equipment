
SPEED_RANGE = {'start':62, 'end':55 ,'type':'speed'}
BRAKE_RANGE = {'start':25, 'end':17 ,'type':'brake'}

def cal_speed(num):
	num = float(num)
	num = num - SPEED_RANGE['start']
	return round(num/(SPEED_RANGE['end']-SPEED_RANGE['start']),4)

def cal_brake(num):
	num = float(num)
	num = num - BRAKE_RANGE['start']
	return round(num/(BRAKE_RANGE['end']-BRAKE_RANGE['start']),4)