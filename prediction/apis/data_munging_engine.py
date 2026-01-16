from prediction.endpoints import data_munging_engine as endpoints
from prediction import request_utils
# from prediction.apis import quickflat as qf

def concat_columns2(auth, database, collection, attribute, separator, info=False):
	ep = endpoints.CONCAT_COLUMNS2
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"separator": separator
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_date2(auth, database, collection, attribute, find, info=False):
	ep = endpoints.DATE_ENRICH2
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def auto_normalize_all(auth, database, collection, fields, find, normalized_high, normalized_low, info=False):
	ep = endpoints.AUTO_NORMALIZE_ALL
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"fields": fields,
		"find": find,
		"normalizedHigh": normalized_high,
		"normalizedLow": normalized_low
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def concat_columns(auth, databasename, collection, attribute, info=False):
	ep = endpoints.CONCAT_COLUMNS
	param_dict = {"mongodb": databasename, "collection": collection, "attribute": attribute}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_date(auth, database, collection, attribute, info=False):
	ep = endpoints.DATE_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enum_convert(auth, database, collection, attribute, info=False):
	ep = endpoints.ENUM_CONVERT
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def fill_zeros(auth, database, collection, attribute, info=False):
	ep = endpoints.FILL_ZEROS
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def fill_values(auth, database, collection, find, attribute, value, info=False):
	ep = endpoints.FILL_VALUES
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"find": find,
		"attribute": attribute,
		"value": value
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta


def foreign_key_aggregator(auth, database, collection, attribute, search, mongodbf, collectionf, attributef, fields, info=False):
	ep = endpoints.FOREIGN_KEY_AGGREGATOR
	param_dict = {
		"mongodb": database,
		"collection": collection,
		"attribute": attribute,
		"search": search,
		"mongodbf": mongodbf,
		"collectionf": collectionf,
		"attributef": attributef,
		"fields": fields
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def foreign_key_lookup(auth, database, collection, attribute, search, mongodbf, collectionf, attributef, fields, info=False):
	ep = endpoints.FOREIGN_KEY_LOOKUP
	param_dict = {
		"mongodb": database,
		"collection": collection,
		"attribute": attribute,
		"search": search,
		"mongodbf": mongodbf,
		"collectionf": collectionf,
		"attributef": attributef,
		"fields": fields
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_fragments(auth, database, collection, attribute, strings, info=False):
	ep = endpoints.FRAGMENT_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"stringOnly": strings
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_fragments2(auth, database, collection, attribute, strings, find, info=False):
	ep = endpoints.FRAGMENT_ENRICH2
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"stringOnly": strings,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def generate_features(auth, database, collection, featureset, categoryfield, datefield, numfield, groupby, find, info=False):
	ep = endpoints.GENERATE_FEATURES
	param_dict = {"database": database, "collection": collection, "featureset":featureset, "categoryfield":categoryfield, "datefield":datefield, "numfield":numfield, "groupby":groupby, "find":find}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def generate_features_normalize(auth, database, collection, find, inplace, normalized_high, normalized_low, numfields, info=False):
	ep = endpoints.GENERATE_FEATURES_NORMALIZE
	param_dict = {"database": database, "collection": collection, "find":find, "inPlace": inplace, "normalizedHigh": normalized_high, "normalizedLow": normalized_low, "numfields": numfields}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def get_categories(auth, database, collection, categoryfield, find, total, info=False):
	ep = endpoints.GET_CATEGORIES
	param_dict = {"database": database, "collection":collection, "categoryfield":categoryfield, "total": total, "find": find}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def get_categories_ratio(auth, database, collection, categoryfield, find, total, info=False):
	ep = endpoints.GET_CATEGORIES_RATIOS
	param_dict = {"database": database, "collection":collection, "categoryfield":categoryfield, "total": total, "find": find}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_location(auth, database, collection, attribute, info=False):
	ep = endpoints.LOCATION_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_mcc(auth, database, collection, attribute, find, info=False):
	ep = endpoints.MCC_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def prediction_enrich_fast(auth, database, collection, search, sort, predictor, predictor_label, attributes, skip, limit, info=False):
	ep = endpoints.PREDICTION_ENRICH_FAST_GET
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"search": search,
		"sort": sort,
		"predictor": predictor,
		"predictor_label": predictor_label,
		"attributes": attributes,
		"skip": skip,
		"limit": limit
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta
	
# predicition_enrich(auth, database, collection2, search, sort, predictor, predictor_label, attributes) 
def predicition_enrich(auth, database, collection, search, sort, predictor, predictor_label, attributes, info=False):
	ep = endpoints.PREDICTION_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"search": search,
		"predictor": predictor,
		"predictor_label": predictor_label,
		"attributes": attributes,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def enrich_sic(auth, database, collection, attribute, find, info=False):
	ep = endpoints.SIC_ENRICH
	param_dict = {
		"mongodb": database, 
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

# def quickflat(config, info=False):
# 	quick_flat = qf.QuickFlat(config)
# 	quick_flat.flatten()

def process_client_pulse_reliability(auth, collection, collectionOut, database, find, groupby, mongoAttribute, typeName, info=False):
	ep = endpoints.PROCESS_CLIENT_PULSE_RELIABILITY
	param_dict = {
		"collection": collection,
		"collectionOut": collectionOut,
		"database": database,
		"find": find,
		"groupby": groupby,
		"mongoAttribute": mongoAttribute,
		"type": typeName
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def generate_time_series_features(auth, categoryfield, collection, database, datefield, featureset, find, groupby, numfield, startdate=None, windowsize=1, info=False):
	ep = endpoints.GENERATE_TIME_SERIES_FEATURES
	param_dict = {
		"categoryfield": categoryfield,
		"collection": collection,
		"database": database,
		"datefield": datefield,
		"featureset": featureset,
		"find": find,
		"groupby": groupby,
		"numfield": numfield,
		"startdate": startdate,
		"windowsize": windowsize
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def personality_enrich(auth, category, collection, collectionOut, database, find, groupby, info=False):
	ep = endpoints.PERSONALITY_ENRICH
	param_dict = {
		"category": category,
		"collection": collection,
		"collectionOut": collectionOut,
		"database": database,
		"find": find,
		"groupby": groupby		
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def munge_transactions_aggregate(auth, munging_step, project_id, info=False):
	ep = endpoints.MUNGE_TRANSACTIONS_AGGREGATE
	param_dict = {
		"munging_step": munging_step,
		"project_id": project_id
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def munge_transactions(auth, munging_step, project_id, info=False):
	ep = endpoints.MUNGE_TRANSACTIONS
	param_dict = {
		"munging_step": munging_step,
		"project_id": project_id
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def flatten_document(auth, db, collection, attribute, find, info=False):
	ep = endpoints.FLATTEN_DOCUMENT
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_key(auth, db, collection, attribute, find, info=False):
	ep = endpoints.DELETE_KEY
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"attribute": attribute,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_many_documents(auth, db, collection, find, info=False):
	ep = endpoints.DELETE_MANY_DOCUMENTS
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def process_range(auth, db, collection, attribute, new_attribute, find, rules, info=False):
	ep = endpoints.PROCESS_RANGE
	param_dict = {
		"database": db,
		"collection": collection,
		"mongoAttribute": attribute,
		"newAttribute": new_attribute,
		"find": find,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def nlp_worker(auth, database, collection, database_out, collection_out, attribute, find, model="original", summarization_max=10, summarization_min=5, transformer="t5-small", model_type="nlp_b5_base", info=False):
	ep = endpoints.NLP_WORKER
	param_dict = {
		"database": db,
		"collection": collection,
		"database_out": database_out,
		"collection_out": collection_out,
		"attribute": attribute,
		"find": find,
		"model": model,
		"summarization_max": summarization_max,
		"summarization_min": summarization_min,
		"transformer": transformer,
		"type": model_type,
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_many_documents(auth, db, collection, find, info=False):
	ep = endpoints.DELETE_MANY_DOCUMENTS
	param_dict = {
		"mongodb": db,
		"collection": collection,
		"find": find
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def process_range(auth, db, collection, find, attribute, new_attribute, rules, info=False):
	ep = endpoints.PROCESS_RANGE
	param_dict = {
		"database": db,
		"collection": collection,
		"find": find,
		"mongoAttribute": attribute,
		"newAttribute": new_attribute,
		"rules": rules
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def prediction_enrich_fast_post(auth, json, info=False):
	ep = endpoints.PREDICTION_ENRICH_FAST_POST
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result


def ecosystem_rewards_beta_box_plots(auth,options_store_collection,options_store_database,contextual_variable_one="",contextual_variable_two="",outlier_threshold=0.01,show_low_data=True, info=False):
	"""
	Produce box and whisker plot parameters for Beta distributions in the Ecosystem Rewards algorithm

	:param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
	:param options_store_collection: The MongoDB collection containing the Options Store
	:param options_store_database: The MongoDB database containing the Options Store
	:param contextual_variable_one: The MongoDB collection containing the database
	:param contextual_variable_one: The value of contextual variable one for which the distributions should be shown. An empty string will not apply the filter
	:param contextual_variable_two: The value of contextual variable two for which the distributions should be shown. An empty string will not apply the filter
	:param outlier_threshold: The threshold for outliers, this will be used to determine the min and max values for the box and whisker plot. max will be the value of the CDF at 1-outlier_threshold and min will be the value of the CDF at outlier_threshold
	:param show_low_data: If False, plot parameters will not be produced for distributions without both contacts and responses

	:return: A list of dictionaries where each dictionary contains the box and whisker plot parameters for an option.
	"""
	show_low_data_string = "true"
	if not show_low_data:
		show_low_data_string = "false"

	ep = endpoints.POST_ECOSYSTEM_REWARDS_BETA_DISTRIBUTION_BOX_PLOTS
	json = {
		"options_store_collection": options_store_collection,
		"options_store_database": options_store_database,
		"contextual_variable_one": contextual_variable_one,
		"contextual_variable_two": contextual_variable_two,
		"outlier_threshold": outlier_threshold,
		"show_low_data": show_low_data_string
	}
	resp = request_utils.create(auth, ep, json=json, info=info)

	try:
		result = resp.json()
	except:
		print(f"Error parsing JSON response from server: {resp}")
		raise

	try:
		# Convert formatting to be compatible with matplotlib
		boxes = []
		for box_iter in result:
			box_addition = {
				'label': box_iter["category"],
				'whislo': box_iter["min"],
				'q1': box_iter["q1"],
				'med': box_iter["median"],
				'q3': box_iter["q3"],
				'whishi': box_iter["max"],
				'fliers': []
			}
			boxes.append(box_addition)
	except:
		print(f"Error converting to matplotlib compatible formatting: {result}")
		raise

	return boxes


def ecosystem_rewards_explore(auth,start_time,end_time,options_store_collection,options_store_database,deployment_id,logging_collection="ecosystemruntime",logging_database="logging",sample_size=0,check_indexes=False, info=False):
	"""
	Estimate the amount of exploration being performed by the Ecosystem Rewards algorithm by determining when the most popular offer in a contextual variable segment is not being recommended

	:param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
	:param start_time: The start time for the logging data to be used to estimate the rate of exploration
	:param end_time: The end time for the logging data to be used to estimate the rate of exploration
	:param options_store_collection: The MongoDB collection containing the Options Store
	:param options_store_database: The MongoDB database containing the Options Store
	:param deployment_id: The name of the deployment_id for which the rate of exploration should be quantified
	:param logging_collection: The MongoDB collection containing the contacts logging data
	:param logging_database: The MongoDB database containing the contacts logging data
	:param sample_size: The number of samples to be used to estimate the rate of exploration. A value of 0 will use all data
	:param check_indexes: If True, the function will check if the indexes optimal indexes are present on the logging collection and will create them if necessary

	:return: A dictionary containing the number of offers considered, the number of offers marked as exploration and the exploration rate.
	"""
	check_indexes_string = "true"
	if not check_indexes:
		check_indexes_string = "false"

	ep = endpoints.POST_ECOSYSTEM_REWARDS_EXPLORATION
	json = {
		"start_time": start_time,
		"end_time": end_time,
		"options_store_collection": options_store_collection,
		"options_store_database": options_store_database,
		"predictor": deployment_id,
		"logging_collection": logging_collection,
		"logging_database": logging_database,
		"sample_size": str(sample_size),
		"check_indexes": check_indexes_string
	}
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result


def ecosystem_rewards_explore_approx(auth,start_time,end_time,options_store_collection,options_store_database,deployment_id,logging_collection="ecosystemruntime",logging_database="logging",sample_size=0,threshold=0,score_filter=None,check_indexes=False, info=False):
	"""
	Estimate the amount of exploration being performed by the Ecosystem Rewards algorithm by calculating that a given score for an option would be considered exploration given the Beta distributions of the other options with a higher average propensity

	:param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
	:param start_time: The start time for the logging data to be used to estimate the rate of exploration
	:param end_time: The end time for the logging data to be used to estimate the rate of exploration
	:param options_store_collection: The MongoDB collection containing the Options Store
	:param options_store_database: The MongoDB database containing the Options Store
	:param deployment_id: The name of the deployment_id for which the rate of exploration should be quantified
	:param logging_collection: The MongoDB collection containing the contacts logging data
	:param logging_database: The MongoDB database containing the contacts logging data
	:param sample_size: The number of samples to be used to estimate the rate of exploration. A value of 0 will use all data
	:param threshold: The value added to an Options propensity when filtering for other options with a higher propensity
	:param score_filter: Specify a score value to be excluded from the analysis, for example if offers are manually added in the post scoring logic they can be given a score of 1 and then excluded using this parameter
	:param check_indexes: If True, the function will check if the indexes optimal indexes are present on the logging collection and will create them if necessary

	:return: A dictionary containing the the exploration rate.
	"""
	check_indexes_string = "true"
	if not check_indexes:
		check_indexes_string = "false"

	score_filter_string = "false"
	if score_filter is not None:
		score_filter_string = str(score_filter)

	ep = endpoints.POST_ECOSYSTEM_REWARDS_EXPLORATION_APPROX
	json = {
		"start_time": start_time,
		"end_time": end_time,
		"options_store_collection": options_store_collection,
		"options_store_database": options_store_database,
		"predictor": deployment_id,
		"logging_collection": logging_collection,
		"logging_database": logging_database,
		"sample_size": str(sample_size),
		"threshold": str(threshold),
		"score_filter": score_filter_string,
		"check_indexes": check_indexes_string
	}
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result


def ecosystem_rewards_explore_approx_context(auth, start_time, end_time, options_store_collection, options_store_database,
									 deployment_id, logging_collection="ecosystemruntime", logging_database="logging",
									 sample_size=0, threshold=0, score_filter=None, check_indexes=False, info=False):
	"""
	Estimate the amount of exploration being performed by the Ecosystem Rewards algorithm by calculating that a given score for an option would be considered exploration given the Beta distributions of the other options with a higher average propensity. The results are split by the contextual Variable values in the Dynamic Interaction configuration.

	:param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
	:param start_time: The start time for the logging data to be used to estimate the rate of exploration
	:param end_time: The end time for the logging data to be used to estimate the rate of exploration
	:param options_store_collection: The MongoDB collection containing the Options Store
	:param options_store_database: The MongoDB database containing the Options Store
	:param deployment_id: The name of the deployment_id for which the rate of exploration should be quantified
	:param logging_collection: The MongoDB collection containing the contacts logging data
	:param logging_database: The MongoDB database containing the contacts logging data
	:param sample_size: The number of samples to be used to estimate the rate of exploration. A value of 0 will use all data
	:param threshold: The value added to an Options propensity when filtering for other options with a higher propensity
	:param score_filter: Specify a score value to be excluded from the analysis, for example if offers are manually added in the post scoring logic they can be given a score of 1 and then excluded using this parameter
	:param check_indexes: If True, the function will check if the indexes optimal indexes are present on the logging collection and will create them if necessary

	:return: A list of dictionaries containing the number of offers considered, the contextual variable values and the exploration rate.
	"""
	check_indexes_string = "true"
	if not check_indexes:
		check_indexes_string = "false"

	score_filter_string = "false"
	if score_filter is not None:
		score_filter_string = str(score_filter)

	ep = endpoints.POST_ECOSYSTEM_REWARDS_EXPLORE_APPROX_CONTEXT
	json = {
		"start_time": start_time,
		"end_time": end_time,
		"options_store_collection": options_store_collection,
		"options_store_database": options_store_database,
		"predictor": deployment_id,
		"logging_collection": logging_collection,
		"logging_database": logging_database,
		"sample_size": str(sample_size),
		"threshold": str(threshold),
		"score_filter": score_filter_string,
		"check_indexes": check_indexes_string
	}
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result