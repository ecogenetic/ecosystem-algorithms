from prediction.endpoints import data_management_engine as endpoints
from prediction import request_utils
from json import dumps
from urllib.parse import quote

# Data Management Engine
def get_document_db_aggregate2(auth, database, collection, aggregate, field, limit, projections, skip, sort, info=False):
	ep = endpoints.GET_MONGO_DB_AGGREGATE2
	param_dict = {
		"database": database, 
		"collection": collection,
		"aggregate": aggregate,
		"field": field,
		"limit": limit,
		"projections": projections,
		"skip": skip,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def add_document_collection(auth, database, collection, info=False):
	ep = endpoints.ADD_MONGO_COLLECTION
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def add_document_database(auth, database, info=False):
	ep = endpoints.ADD_MONGO_DATABASE
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def add_documents(auth, json, info=False):
	ep = endpoints.ADD_MONGO_DOCUMENTS
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def csv_file_to_json(auth, csv_file, json_file, info=False):
	ep = endpoints.CSV_FILE_TO_JSON
	param_dict = {
		"csv_file": csv_file,
		"json_file": json_file
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def csv_import(auth, database, collection, csv_file, info=False):
	ep = endpoints.CSV_FILE_TO_MONGO_DB_IMPORT
	param_dict = {
		"database": database, 
		"collection": collection,
		"csv_file": csv_file
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def csv_import2(auth, database, collection, csv_file, headerline, import_type, info=False):
	ep = endpoints.CSV_FILE_TO_MONGO_DB_IMPORT2
	param_dict = {
		"database": database, 
		"collection": collection,
		"csv_file": csv_file,
		"headerline": headerline,
		"type": import_type

	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def delete_all_documents(auth, doc_json, info=False):
	ep = endpoints.DELETE_ALL_MONGO_DOCUMENTS
	resp = request_utils.create(auth, ep, json=doc_json, info=info)
	response = resp.json()
	return response

def delete_documents(auth, doc_json, info=False):
	ep = endpoints.DELETE_MONGO_DOCUMENTS
	resp = request_utils.create(auth, ep, json=doc_json, info=info)
	response = resp.json()
	return response

def drop_document_collection(auth, database, collection, info=False):
	ep = endpoints.DROP_MONGO_COLLECTION
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def drop_document_collection_index(auth, database, collection, index, info=False):
	ep = endpoints.DROP_MONGO_COLLECTION_INDEX
	param_dict = {
		"database": database, 
		"collection": collection,
		"index": index
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def drop_document_database(auth, database, info=False):
	ep = endpoints.DROP_MONGO_DATABASE
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def dump_document_database(auth, database, collection, folder, option, info=False):
	ep = endpoints.DUMP_MONGO_DATABASE
	param_dict = {
		"database": database,
		"collection": collection,
		"folder": folder,
		"option": option
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def export_documents(auth, filename, filetype, database, collection, field, sort, projection, limit, info=False):
	ep = endpoints.EXPORT_MONGO_DOCUMENTS 
	param_dict = {
		"file_name": filename,
		"file_type": filetype,
		"database": database, 
		"collection": collection,
		"field": field,
		"sort": sort,
		"projection": projection,
		"limit": limit
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta

def get_document_collection_indexes(auth, database, collection, info=False):
	ep = endpoints.GET_MONGO_COLLECTION_INDEXES
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_data_aggregate(auth, database, collection, field, projections, aggregate, sort, info=False):
	ep = endpoints.GET_MONGO_DB_AGGREGATE 
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"projections": projections,
		"aggregate": aggregate,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	return meta
	
def get_document_db_collections(auth, database, info=False):
	ep = endpoints.GET_MONGO_DB_COLLECTIONS
	param_dict = {
		"database": database
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_document_db_collection_stats(auth, database, collection, info=False):
	ep = endpoints.GET_MONGO_DB_COLLECTION_STATS
	param_dict = {
		"database": database, 
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_data(auth, database, collection, field, limit, projections, skip, info=False):
	ep = endpoints.GET_MONGO_DB_FIND
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"limit": limit,
		"projections": projections, 
		"skip": skip
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta
	
def get_document_db_find_labels(auth, database, collection, field, projections, skip, info=False):
	ep = endpoints.GET_MONGO_DB_FIND_LABELS
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"projections": projections, 
		"skip": skip
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_data_sort(auth, database, collection, field, limit, projections, skip, sort, info=False):
	ep = endpoints.GET_MONGO_DB_FIND_SORT
	param_dict = {
		"database": database, 
		"collection": collection,
		"field": field,
		"limit": limit,
		"projections": projections, 
		"skip": skip,
		"sort": sort
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def get_document_db_list(auth, server=None, info=False):
	ep = endpoints.GET_MONGO_DB_LIST
	if server == None:
		server = auth.get_server()
	param_dict = {
		"server": server
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	meta = resp.json()
	if "data" in meta:
		meta = meta["data"]
	return meta

def import_documents(auth, database, collection, file_name, file_type, info=False):
	ep = endpoints.IMPORT_MONGO_DOCUMENTS
	param_dict = {
		"database": database,
		"collection": collection,
		"file_name": file_name,
		"file_type": file_type
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def restore_document_database(auth, database, collection, folder, info=False):
	ep = endpoints.RESTORE_MONGO_DATABASE
	param_dict = {
		"database": database,
		"collection": collection,
		"folder": folder
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def create_document_collection_index(auth, database, collection, index, info=False):
	ep = endpoints.CREATE_MONGO_COLLECTION_INDEX
	param_dict = {
		"database": database,
		"collection": collection,
		"index": index
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def post_mongo_db_aggregate_pipeline(auth, json, info=False):
	if "pipeline" not in json:
		raise ValueError("pipeline key is missing from the json input structure")
	try:
		pipeline = json["pipeline"]
		pipeline = quote(dumps(pipeline,ensure_ascii=False))
		json["pipeline"] = pipeline
	except:
		print("WARNING: Unexpected error during unicode processing of pipeline, proceeding with input pipeline")
	ep = endpoints.POST_MONGO_DB_AGGREGATE_PIPELINE
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

def rename_collection(auth, database, collection, new_collection, info=False):
	ep = endpoints.RENAME_COLLECTION
	param_dict = {
		"database": database,
		"collection": collection,
		"new_collection": new_collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def update_key_name(auth, database, collection, find, from_key, to_key, info=False):
	ep = endpoints.UPDATE_KEY_NAME
	param_dict = {
		"database": database,
		"collection": collection,
		"find": find,
		"from": from_key,
		"to": to_key
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_document_labels(auth, database, collection, info=False):
	ep = endpoints.GET_MONGO_DOCUMENT_LABELS
	param_dict = {
		"database": database,
		"collection": collection
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def execute_mongo_db_script(auth, json, info=False):
	ep = endpoints.EXECUTE_MONGO_DB_SCRIPT
	resp = request_utils.create(auth, ep, json=json, info=info)
	result = resp.json()
	return result

# Data Management Engine: Cassandra
def get_cassandra_sql(auth, sql, info=False):
	ep = endpoints.GET_CASSANDRA_SQL
	param_dict = {
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_cassandra_to_mongo(auth, database, collection, sql, info=False):
	"""
	Execute a Cassandra SQL query and ingest the data to a MongoDB collection. The ecosystem server should be configured
	to connect to the target Cassandra servers.

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param database: Database to ingest the data to
	:param collection: Collection to ingest the data to
	:param sql: Cassandra SQL query to execute
	"""
	ep = endpoints.GET_CASSANDRA_TO_MONGODB
	param_dict = {
		"database": database,
		"collection": collection,
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

# Data Management Engine: Presto
def create_presto_sql(auth, connection, sql, info=False):
	ep = endpoints.CREATE_PRESTO_SQL
	param_dict = {
		"connection": connection,
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

def get_presto_sql(auth, connection, sql, info=False):
	ep = endpoints.GET_PRESTO_SQL
	param_dict = {
		"connection": connection,
		"sql": sql
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result

# Data Management Engine: Hive
def get_hive_to_mongo(auth, database, collection, sql, connection_string, info=False):
	"""
	Execute a Hive SQL query and ingest the data to a MongoDB collection.

	:param auth: Token for accessing the ecosystem-server. Created using jwt_access.
	:param database: Database to ingest the data to
	:param collection: Collection to ingest the data to
	:param sql: Hive SQL query to execute
	:param connection_string: Connection string to connect to the target Hive server
	"""
	ep = endpoints.GET_HIVE_TO_MONGODB
	param_dict = {
		"database": database,
		"collection": collection,
		"sql": sql,
        "connection_string": connection_string
	}
	resp = request_utils.create(auth, ep, params=param_dict, info=info)
	result = resp.json()
	return result