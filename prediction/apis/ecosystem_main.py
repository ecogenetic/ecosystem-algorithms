from prediction.endpoints import ecosystem_main as endpoints
from prediction import request_utils

def create_profile(auth, json, info=False):
	ep = endpoints.CREATE
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def profiles(auth, info=False):
	ep = endpoints.PROFILES
	resp = request_utils.create(auth, ep, info=info)
	result = resp.json()
	return result
