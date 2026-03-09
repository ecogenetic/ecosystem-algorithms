from nlp.endpoints import nlp_engine as endpoints
from nlp import request_utils
import requests

def no_auth_ping(server, endpoint, headers, message):
    url_endpoint = server + endpoint
    param_dict = {
        "message": message
    }
    resp = requests.get(url_endpoint, headers=headers, params=param_dict)
    meta = resp.json()
    return meta

def b5(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, find, limit, batch_size, gpu_cores=0):
	ep = endpoints.B5
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"find": find,
		"limit": limit,
		"batch_size": batch_size,
		"gpu_cores": gpu_cores
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def mbti(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, find, limit, batch_size, gpu_cores=0):
	ep = endpoints.MBTI
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"find": find,
		"limit": limit,
		"batch_size": batch_size,
		"gpu_cores": gpu_cores
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def ner(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, find, limit, batch_size):
	ep = endpoints.NER
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"find": find,
		"limit": limit,
		"batch_size": batch_size
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def pos(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, find, limit, batch_size):
	ep = endpoints.POS
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"find": find,
		"limit": limit,
		"batch_size": batch_size
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def summarization(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, transformer, find, limit, batch_size, summarization_min, summarization_max, gpu_cores=0):
	ep = endpoints.SUMMARIZATION
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"transformer": transformer,
		"find": find,
		"limit": limit,
		"batch_size": batch_size,
		"summarization_min": summarization_min,
		"summarization_max": summarization_max,
		"gpu_cores": gpu_cores
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def sentence_encoding(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, find, limit, batch_size):
	ep = endpoints.SENTENCE_ENCODING
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"find": find,
		"limit": limit,
		"batch_size": batch_size
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta

def sentiment(auth, input_database, input_collection, output_database, output_collection, groupby_field, transaction_field, text_field, find, limit, batch_size):
	ep = endpoints.SENTIMENT
	param_dict = {
		"input_database": input_database, 
		"input_collection": input_collection,
		"output_database": output_database,
		"output_collection": output_collection,
		"groupby_field": groupby_field,
		"transaction_field": transaction_field,
		"text_field": text_field,
		"find": find,
		"limit": limit,
		"batch_size": batch_size
	}
	resp = request_utils.create(auth, ep, params=param_dict)
	meta = resp.json()
	return meta