import platform
import os
####################################################################################
#All OS functions
####################################################################################
def find_os():
	out=platform.system()
	return(out)
def get_user_profile():
	if platform.system()=='Windows':
		out=os.environ['USERPROFILE']
	else:
		out=os.path.expanduser('~')
	return(out)
