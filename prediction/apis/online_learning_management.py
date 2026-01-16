from prediction.apis import algorithm_client_pulse as cp
from prediction.apis import data_management_engine as dme

from datetime import datetime
import json
import uuid


def online_learning_ecosystem_rewards_setup_feature_store(
    auth,
    contextual_variables,
    setup_feature_store_db,
    setup_feature_store_collection,
    offer_name_column,
    offer_db=None,
    offer_collection=None,
    list_of_offers=None
):
    """
    Add contextual variables to a setup feature store for the ecosystem rewards dynamic recommender using a collection
    containing the relevant offers.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param offer_db: The database containing the offers.
   :param offer_collection: The collection containing the offers.
   :param offer_name_column: The column in the collection containing the offer names.
   :param contextual_variables: A dictionary containing the contextual variables names as keys. Each value in the dictionary should be a list containing the possible values of the contextual variables.
   :param setup_feature_store_db: The database to store the setup feature store in.
   :param setup_feature_store_collection: The collection to store the setup feature store in.
   :param list_of_offers: A list of offers to be used in the setup feature store. If not provided, all offers in the offer collection will be used.

    """
    if not isinstance(offer_db, (str,type(None))):
        raise TypeError("offer_db should be a string")
    if not isinstance(offer_collection, (str,type(None))):
        raise TypeError("offer_collection should be a string")
    if not isinstance(offer_name_column, (str,type(None))):
        raise TypeError("offer_name_column should be a string")
    if not isinstance(contextual_variables, dict):
        raise TypeError("contextual_variables should be a dictionary")
    if not isinstance(setup_feature_store_db, str):
        raise TypeError("setup_feature_store_db should be a string")
    if not isinstance(setup_feature_store_collection, str):
        raise TypeError("setup_feature_store_collection should be a string")
    if not isinstance(list_of_offers, (list, type(None))):
        raise TypeError("list_of_offers should be a list or None")

    if list_of_offers is None and (offer_db is None or offer_collection is None):
        raise ValueError("Either list_of_offers or offer_db and offer_collection must be specified")

    try:
        if list_of_offers is None:
            sample_offer_collection = dme.get_data(auth, offer_db, offer_collection, {}, 1, {}, 0)
            if len(sample_offer_collection) == 0:
                raise ImportError(f"Mongo collection {offer_collection} in database {offer_db} appears to be empty")
            if offer_name_column not in sample_offer_collection:
                raise KeyError(f"{offer_name_column}, specified as the offer_name_column, not found as a field in "
                               f"{offer_collection}")
    except Exception as error:
        print("Unexpected error occured while validating offer_db and offer_collection")
        raise
    
    if len(contextual_variables) > 2:
        raise KeyError("At most two contextual variables can be specified for the ecosystem rewards algorithm")
    for context_var_iter in contextual_variables:
        if not isinstance(contextual_variables[context_var_iter], list):
            raise TypeError("The value for each key in the contextual variables dictionary should be a list of "
                            "possible segment values")

    if list_of_offers is not None:
        offer_db = setup_feature_store_db
        offer_collection = setup_feature_store_collection
        if len(list_of_offers) == 0:
            raise ValueError("list_of_offers should not be empty")
        dme.delete_all_documents(auth,{"database":offer_db,"collection":offer_collection})
        for offer_iter in list_of_offers:
            offer_doc = {offer_name_column: offer_iter}
            insert_doc = {"database": offer_db, "collection":offer_collection, "document": offer_doc}
            dme.add_documents(auth, insert_doc)

    contextual_fields = list(contextual_variables.keys())
    if len(contextual_fields) == 2:
        dme.post_mongo_db_aggregate_pipeline(auth,
            {
            "database":offer_db
            ,"collection":offer_collection
            ,"pipeline":[
                {"$group":{"_id":"$"+offer_name_column}}
                ,{"$project":{offer_name_column:"$_id","_id":0}}
                ,{"$addFields":{contextual_fields[0]:contextual_variables[contextual_fields[0]]}}
                ,{"$unwind":"$"+contextual_fields[0]}
                ,{"$addFields":{contextual_fields[1]:contextual_variables[contextual_fields[1]]}}
                ,{"$unset":"_id"}
                ,{"$unwind":"$"+contextual_fields[1]}
                ,{"$out":{"db":setup_feature_store_db,"coll":setup_feature_store_collection}}
            ]
            }
        )
    elif len(contextual_fields) == 1:
        dme.post_mongo_db_aggregate_pipeline(auth,
            {
            "database":offer_db
            ,"collection":offer_collection
            ,"pipeline":[
                {"$group":{"_id":"$"+offer_name_column}}
                ,{"$project":{offer_name_column:"$_id","_id":0}}
                ,{"$addFields":{contextual_fields[0]:contextual_variables[contextual_fields[0]]}}
                ,{"$unwind":"$"+contextual_fields[0]}
                ,{"$out":{"db":setup_feature_store_db,"coll":setup_feature_store_collection}}
            ]
            }
        )
    else:
        print("WARNING: No contextual variables specified, writing a collection with a list of unique offers")
        dme.post_mongo_db_aggregate_pipeline(auth,
            {
            "database":offer_db
            ,"collection":offer_collection
            ,"pipeline":[
                {"$group":{"_id":"$"+offer_name_column}}
                ,{"$project":{offer_name_column:"$_id","_id":0}}
                ,{"$out":{"db":setup_feature_store_db,"coll":setup_feature_store_collection}}
            ]
            }
        )


def update_options_store(
        auth,
        name = None,
        uuid = None
):
    """
    Update the options store for the specified online learning configuration.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param name: The name of the online learning configuration. Either name or uuid must be specified.
   :param uuid: The UUID of the online learning configuration. Either name or uuid must be specified.

    """
    if name is None and uuid is None:
        raise ValueError("Either name or uuid must be specified")
    if name is not None and uuid is not None:
        raise ValueError("Either name or uuid must be specified but not both")
    if name is not None:
        if not isinstance(name, str):
            raise TypeError("name should be a string")
    if uuid is not None:
        if not isinstance(uuid, str):
            raise TypeError("uuid should be a string")

    try:
        existing_configurations = cp.list_pulse_responder_dynamic(auth)["data"]
        selected_configuration = {}
        for config_iter in existing_configurations:
            if (config_iter["name"] == name) or (config_iter["uuid"] == uuid):
                if selected_configuration != {}:
                    raise ValueError(f"More than one configuration matches the name or uuid specified: {selected_configuration} and {config_iter}")
                selected_configuration = config_iter

        if selected_configuration == {}:
            raise ValueError(f"No configuration matches the name or uuid specified")
    except Exception as error:
        print("Unexpected error occurred while extracting Dynamic Interaction configuration for specified name or uuid")
        raise

    try:
        cp_update_doc = {
            "type":"generateUpdatedOptions"
            ,"name":selected_configuration["name"]
            ,"uuid":selected_configuration["uuid"]
            ,"engagement_type":selected_configuration["randomisation"]["approach"]
            ,"feature_store_database":selected_configuration["feature_store_database"]
            ,"feature_store_collection":selected_configuration["feature_store_collection"]
            ,"contextual_variable_one_values":selected_configuration["contextual_variables"]["contextual_variable_one_values"]
            ,"contextual_variable_two_values":selected_configuration["contextual_variables"]["contextual_variable_two_values"]
            ,"contextual_variable_one_name":selected_configuration["contextual_variables"]["contextual_variable_one_name"]
            ,"contextual_variable_two_name":selected_configuration["contextual_variables"]["contextual_variable_two_name"]
            ,"contextual_variable_one_from_data_source":selected_configuration["contextual_variables"]["contextual_variable_one_from_data_source"]
            ,"contextual_variable_two_from_data_source":selected_configuration["contextual_variables"]["contextual_variable_two_from_data_source"]
            ,"contextual_variable_one_lookup":selected_configuration["contextual_variables"]["contextual_variable_one_lookup"]
            ,"contextual_variable_two_lookup":selected_configuration["contextual_variables"]["contextual_variable_two_lookup"]
            ,"offer_key":selected_configuration["contextual_variables"]["offer_key"]
            ,"tracking_key":selected_configuration["contextual_variables"]["tracking_key"]
            ,"options_store_database":selected_configuration["options_store_database"]
            ,"options_store_collection":selected_configuration["options_store_collection"]
            ,"prior_success_reward":selected_configuration["randomisation"]["prior_success_reward"]
            ,"prior_fail_reward":selected_configuration["randomisation"]["prior_fail_reward"]
            ,"take_up":selected_configuration["contextual_variables"]["take_up"]
        }
        update_response = cp.update_client_pulse_responder(auth, cp_update_doc)
        return update_response
    except Exception as error:
        print("Unexpected error occurred while updating the options store")
        raise


def generate_options_store(
        auth,
        name = None,
        uuid = None
):
    """
    Generate the options store for the specified online learning configuration.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param name: The name of the online learning configuration. Either name or uuid must be specified.
   :param uuid: The UUID of the online learning configuration. Either name or uuid must be specified.

    """
    if name is None and uuid is None:
        raise ValueError("Either name or uuid must be specified")
    if name is not None and uuid is not None:
        raise ValueError("Either name or uuid must be specified but not both")
    if name is not None:
        if not isinstance(name, str):
            raise TypeError("name should be a string")
    if uuid is not None:
        if not isinstance(uuid, str):
            raise TypeError("uuid should be a string")

    try:
        existing_configurations = cp.list_pulse_responder_dynamic(auth)["data"]
        selected_configuration = {}
        for config_iter in existing_configurations:
            if (config_iter["name"] == name) or (config_iter["uuid"] == uuid):
                if selected_configuration != {}:
                    raise ValueError(f"More than one configuration matches the name or uuid specified: {selected_configuration} and {config_iter}")
                selected_configuration = config_iter

        if selected_configuration == {}:
            raise ValueError(f"No configuration matches the name or uuid specified")
    except Exception as error:
        print("Unexpected error occurred while extracting Dynamic Interaction configuration for specified name or uuid")
        raise

    try:
        cp_update_doc = {
            "type":"generateDefaultOptions"
            ,"name":selected_configuration["name"]
            ,"uuid":selected_configuration["uuid"]
            ,"engagement_type":selected_configuration["randomisation"]["approach"]
            ,"feature_store_database":selected_configuration["feature_store_database"]
            ,"feature_store_collection":selected_configuration["feature_store_collection"]
            ,"contextual_variable_one_values":selected_configuration["contextual_variables"]["contextual_variable_one_values"]
            ,"contextual_variable_two_values":selected_configuration["contextual_variables"]["contextual_variable_two_values"]
            ,"contextual_variable_one_name":selected_configuration["contextual_variables"]["contextual_variable_one_name"]
            ,"contextual_variable_two_name":selected_configuration["contextual_variables"]["contextual_variable_two_name"]
            ,"contextual_variable_one_from_data_source":selected_configuration["contextual_variables"]["contextual_variable_one_from_data_source"]
            ,"contextual_variable_two_from_data_source":selected_configuration["contextual_variables"]["contextual_variable_two_from_data_source"]
            ,"contextual_variable_one_lookup":selected_configuration["contextual_variables"]["contextual_variable_one_lookup"]
            ,"contextual_variable_two_lookup":selected_configuration["contextual_variables"]["contextual_variable_two_lookup"]
            ,"offer_key":selected_configuration["contextual_variables"]["offer_key"]
            ,"tracking_key":selected_configuration["contextual_variables"]["tracking_key"]
            ,"options_store_database":selected_configuration["options_store_database"]
            ,"options_store_collection":selected_configuration["options_store_collection"]
            ,"prior_success_reward":selected_configuration["randomisation"]["prior_success_reward"]
            ,"prior_fail_reward":selected_configuration["randomisation"]["prior_fail_reward"]
            ,"take_up":selected_configuration["contextual_variables"]["take_up"]
        }
        update_response = cp.update_client_pulse_responder(auth, cp_update_doc)
        return update_response
    except Exception as error:
        print("Unexpected error occurred while generating the options store")
        raise


def create_online_learning(
        auth,
        name,
        description,
        feature_store_collection,
        feature_store_database,
        options_store_database,
        options_store_collection,
        contextual_variables_offer_key,
        score_connection="http://ecosystem-runtime:8091",
        score_database="ecosystem_meta",
        score_collection="dynamic_engagement",
        algorithm="ecosystem_rewards",
        options_store_connection="",
        batch="false",       
        feature_store_connection="",
        contextual_variables_contextual_variable_one_from_data_source=False,
        contextual_variables_contextual_variable_one_lookup="",
        contextual_variables_contextual_variable_one_name="",
        contextual_variables_contextual_variable_two_from_data_source=False,
        contextual_variables_contextual_variable_two_name="",
        contextual_variables_contextual_variable_two_lookup="",
        contextual_variables_tracking_key="",
        contextual_variables_take_up="",
        batch_database_out="",
        batch_collection_out="",
        batch_threads=1,
        batch_collection="",
        batch_userid="",
        batch_contextual_variables="",
        batch_number_of_offers=1,
        batch_database="",
        batch_pulse_responder_list="",
        batch_find="{}",
        batch_options="",
        batch_campaign="",
        batch_execution_type="",
        randomisation_calendar="None",
        randomisation_test_options_across_segment="",
        randomisation_processing_count=1000,
        randomisation_discount_factor=0.75,
        randomisation_batch="false",
        randomisation_prior_fail_reward=0.1,
        randomisation_cross_segment_epsilon=0,
        randomisation_success_reward=1,
        randomisation_interaction_count="0",
        randomisation_epsilon=0,
        randomisation_prior_success_reward=1,
        randomisation_fail_reward=0.1,
        randomisation_max_reward=10,
        randomisation_cache_duration=0,
        randomisation_processing_window=86400000,
        randomisation_random_action=0.2,
        randomisation_decay_gamma="1",
        randomisation_learning_rate=0.25,
        randomisation_missing_offers="none",
        randomisation_training_data_source="feature_store",
        virtual_variables=None,
        dynamic_eligibility=None,
        replace=False,
        update=False,
        create_options_index=True,
        create_covering_index=True
):
    """
   Create a new online learning configuration.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param name: The name of the online learning configuration.
   :param description: The description of the online learning configuration.
   :param feature_store_collection: The collection containing the setup feature store.
   :param feature_store_database: The database containing the setup feature store.
   :param options_store_database: The database containing the options store.
   :param options_store_collection: The collection containing the options store.
   :param contextual_variables_offer_key: The key in the setup feature store collection that contains the offer.
   :param score_connection: Used when batch processing is enabled. The connection string to the runtime engine to use for batch processing.
   :param score_database: The database where the online learning configuration is stored
   :param score_collection: The collection where the online learning configuration is stored
   :param algorithm: The algorithm to use for the online learning configuration. Currently only "ecosystem_rewards", "bayesian_probabilistic" and "q_learning" are supported.
   :param options_store_connection: The connection string to the options store.
   :param batch: A boolean indicating whether batch processing should be enabled.
   :param feature_store_connection: The connection string to the setup feature store.
   :param contextual_variables_contextual_variable_one_from_data_source: A boolean indicating whether the first contextual variable should be read from the deployment customer lookup.
   :param contextual_variables_contextual_variable_one_name: The field in the setup feature store to be used for the first contextual variable.
   :param contextual_variables_contextual_variable_one_lookup: The key in the deployment customer lookup that contains the first contextual variable.
   :param contextual_variables_contextual_variable_two_name: The field in the setup feature store to be used for the second contextual variable.
   :param contextual_variables_contextual_variable_two_lookup: The key in the deployment customer lookup that contains the second contextual variable.
   :param contextual_variables_contextual_variable_two_from_data_source: A boolean indicating whether the second contextual variable should be read from the deployment customer lookup.
   :param contextual_variables_tracking_key: The field in the setup feature store to be used for the tracking key.
   :param contextual_variables_take_up: The field in the setup feature store to be used for the take-up.
   :param batch_database_out: The database to store the batch output in.
   :param batch_collection_out: The collection to store the batch output in.
   :param batch_threads: The number of threads to use for batch processing.
   :param batch_collection: The collection to read the batch data from.
   :param batch_userid: The user to be passed to the batch runtime.
   :param batch_contextual_variables: The contextual variables to be used in the batch processing.
   :param batch_number_of_offers: The number of offers to be used in the batch processing.
   :param batch_database: The database to read the batch data from.
   :param batch_pulse_responder_list: The list of runtimes to be used in the batch processing.
   :param batch_find: The query to be used to find the batch data.
   :param batch_options: The options to be used in the batch processing.
   :param batch_campaign: The campaign to be used in the batch processing.
   :param batch_execution_type: The execution type to be used in the batch processing. Allowed values are "internal" and "external".
   :param randomisation_calendar: The calendar to be used.
   :param randomisation_test_options_across_segment: Boolean variable indicating whether offers should be tested outside of their allowed contextual variable segments.
   :param randomisation_processing_count: The number of interactions to be processed.
   :param randomisation_discount_factor: The discount factor to be used in the randomisation.
   :param randomisation_batch: Boolean variable indicating whether batch processing should be enabled.
   :param randomisation_prior_fail_reward: The prior fail reward to be used in the randomisation.
   :param randomisation_cross_segment_epsilon: The cross segment epsilon to be used in the randomisation.
   :param randomisation_success_reward: The success reward to be used in the randomisation.
   :param randomisation_interaction_count: The number of interactions to be used in the randomisation.
   :param randomisation_epsilon: The epsilon to be used in the randomisation.
   :param randomisation_prior_success_reward: The prior success reward to be used in the randomisation.
   :param randomisation_fail_reward: The fail reward to be used in the randomisation.
   :param randomisation_max_reward: The maximum reward to be used in the randomisation.
   :param randomisation_cache_duration: The cache duration to be used in the randomisation.
   :param randomisation_processing_window: The processing window to be used in the randomisation.
   :param randomisation_random_action: The random action to be used in the randomisation.
   :param randomisation_decay_gamma: The decay gamma to be used in the randomisation.
   :param randomisation_learning_rate: The learning rate to be used in the randomisation.
   :param randomisation_missing_offers: The approach used to add scores for offers not present in the training set for the bayesian probabilistic algorithm. Allowed values are "none" and "uniform".
   :param randomisation_training_data_source: The data source to be used for training the q-learning algorithm. Allowed values are "feature_store" and "logging".
   :param virtual_variables: A list of virtual variables to be used in the online learning configuration.
   :param dynamic_eligibility: A dictionary specifying the eligibility rules to be applied when selecting offers for the online learning configuration.
   :param replace: A boolean indicating whether the online learning configuration should be replaced if it already exists.
   :param update: A boolean indicating whether the online learning configuration should be updated if it already exists.
   :param create_options_index: A boolean indicating whether an index should be created on the options store collection. This index greatly improves responses times.
   :param create_covering_index: A boolean indicating whether a covering index should be created on the options store collection. A covered index greatly improves responses times but does not make all fields in the options store available in the post scoring logic.

   :return: The UUID identifier for the online learning configuration which should be linked to the deployment for the project.
    """
    # TODO enhance error checking and handling
    # Check for existence of online learning configuration with the same name
    existing_configurations = cp.list_pulse_responder_dynamic(auth)
    if not replace and not update:
        if len([d for d in existing_configurations["data"] if d["name"] == name]) > 0:
            raise ValueError(f"There is an existing online learning configuration named {name} and replace and update are both False")

    if update:
        if len([d for d in existing_configurations["data"] if d["name"] == name]) == 0:
            raise ValueError(f"Update is set to true and no existing configuration with name {name} can be found")
        update_uuid = [d["uuid"] for d in existing_configurations["data"] if d["name"] == name][0]

    if not isinstance(randomisation_missing_offers, str):
        raise TypeError("randomisation_missing_offers should be a string")
    if randomisation_missing_offers not in ["none", "uniform"]:
        raise ValueError("randomisation_missing_offers should be either 'none' or 'uniform'")

    if algorithm not in ["ecosystem_rewards","bayesian_probabilistic","q_learning"]:
        raise ValueError("algorithm must be ecosystem_rewards, bayesian_probabilistic or q_learning algorithm for other algorithms please use the "
                         "ecosystem.Ai workbench")

    # Initialise configuration document and store input parameters
    config_doc = {}
    config_doc["name"] = name
    config_doc["description"] = description
    
    config_doc["feature_store_collection"] = feature_store_collection
    config_doc["feature_store_database"] = feature_store_database
    config_doc["feature_store_connection"] = feature_store_connection
    
    config_doc["options_store_database"] = options_store_database
    config_doc["options_store_collection"] = options_store_collection
    config_doc["options_store_connection"] = options_store_connection
    
    config_doc["score_collection"] = score_collection
    config_doc["score_database"] = score_database
    config_doc["score_connection"] = score_connection
    
    config_doc["batch"] = batch
    config_doc["options"] = []
    config_doc["date_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    config_doc["description"] = description
    if update:
        config_doc["uuid"] = update_uuid
    else:
        config_doc["uuid"] = str(uuid.uuid4())
    
    # Get values for contextual variables
    if contextual_variables_contextual_variable_one_name != "":
        contextual_variable_value_set_from_virtual_variables = False
        if virtual_variables is not None:
            for virtual_var_iter in virtual_variables:
                if virtual_var_iter["name"] == contextual_variables_contextual_variable_one_name:
                    contextual_variable_value_set_from_virtual_variables = True
                    contextual_virtual_variable = virtual_var_iter
                    contextual_variable_one_values = [contextual_virtual_variable["default"]]
                    for val_iter in contextual_virtual_variable["buckets"]:
                        contextual_variable_one_values.append(val_iter["label"])
        if not contextual_variable_value_set_from_virtual_variables:
            contextual_variable_one_values_pipeline = [
                {"$group":{"_id":"None","values":{"$addToSet":"$"+contextual_variables_contextual_variable_one_name}}}
            ]
            contextual_variable_one_values = dme.post_mongo_db_aggregate_pipeline(
                    auth,
                    {"database": feature_store_database, "collection": feature_store_collection, "pipeline": contextual_variable_one_values_pipeline}
            )[0]["values"]
    else:
        contextual_variable_one_values = []
    
    if contextual_variables_contextual_variable_two_name != "":
        contextual_variable_value_set_from_virtual_variables = False
        if virtual_variables is not None:
            for virtual_var_iter in virtual_variables:
                if virtual_var_iter["name"] == contextual_variables_contextual_variable_two_name:
                    contextual_variable_value_set_from_virtual_variables = True
                    contextual_virtual_variable = virtual_var_iter
                    contextual_variable_two_values = [contextual_virtual_variable["default"]]
                    for val_iter in contextual_virtual_variable["buckets"]:
                        contextual_variable_two_values.append(val_iter["label"])
        if not contextual_variable_value_set_from_virtual_variables:
            contextual_variable_two_values_pipeline = [
                {"$group":{"_id":"None","values":{"$addToSet":"$"+contextual_variables_contextual_variable_two_name}}}
            ]
            contextual_variable_two_values = dme.post_mongo_db_aggregate_pipeline(
                    auth,
                    {"database": feature_store_database, "collection": feature_store_collection, "pipeline": contextual_variable_two_values_pipeline}
            )[0]["values"]
    else:
        contextual_variable_two_values = []
    
    contextual_variables = {
        "offer_key": contextual_variables_offer_key,
        "offer_values": [],
        "contextual_variable_one_from_data_source": contextual_variables_contextual_variable_one_from_data_source,
        "contextual_variable_one_lookup": contextual_variables_contextual_variable_one_lookup,
        "contextual_variable_one_name": contextual_variables_contextual_variable_one_name,
        "contextual_variable_one_values": contextual_variable_one_values,
        "contextual_variable_two_from_data_source": contextual_variables_contextual_variable_two_from_data_source,
        "contextual_variable_two_name": contextual_variables_contextual_variable_two_name,
        "contextual_variable_two_lookup": contextual_variables_contextual_variable_two_lookup,
        "contextual_variable_two_values": contextual_variable_two_values,
        "tracking_key": contextual_variables_tracking_key,
        "take_up": contextual_variables_take_up
    }
    if algorithm == "bayesian_probabilistic":
        training_variable_sample = dme.get_data(auth, feature_store_database, feature_store_collection, {}, 1, {}, 0)
        training_variables = list(training_variable_sample.keys())
        for rem_iter in [contextual_variables_offer_key,contextual_variables_tracking_key,contextual_variables_take_up,"_id"]:
            if rem_iter in training_variables:
                training_variables.remove(rem_iter)
        training_variables_dict = {}
        for training_variable_iter in training_variables:
            training_variable_values_pipeline = [
                {"$group":{"_id":"None","values":{"$addToSet":"$"+training_variable_iter}}}
            ]
            training_variable_values = dme.post_mongo_db_aggregate_pipeline(
                    auth,
                    {"database": feature_store_database, "collection": feature_store_collection, "pipeline": training_variable_values_pipeline}
            )[0]["values"]
            training_variables_dict[training_variable_iter] = training_variable_values
        contextual_variables["training_variable_values"] = training_variables_dict

    config_doc["contextual_variables"] = contextual_variables
    
    batch_settings = {
        "database_out": batch_database_out,
        "collection_out": batch_collection_out,
        "batchUpdateMessage": "",
        "threads": batch_threads,
        "collection": batch_collection,
        "userid": batch_userid,
        "contextual_variables": batch_contextual_variables,
        "number_of_offers": batch_number_of_offers,
        "batch_outline": "",
        "pulse_responder_list": batch_pulse_responder_list,
        "database": batch_database,
        "find": batch_find,
        "options": batch_options,
        "campaign": batch_campaign,
        "execution_type": batch_execution_type
    }
    config_doc["batch_settings"] = batch_settings

    if algorithm == "ecosystem_rewards":
        approach = "binaryThompson"
    elif algorithm == "bayesian_probabilistic":
        approach = "naiveBayes"
    elif algorithm == "q_learning":
        approach = "Q-Learning Algorithm"
    randomisation = {
            "calendar": randomisation_calendar,
            "test_options_across_segment": randomisation_test_options_across_segment,
            "processing_count": randomisation_processing_count,
            "discount_factor": randomisation_discount_factor,
            "batch": randomisation_batch,
            "prior_fail_reward": randomisation_prior_fail_reward,
            "approach": approach,
            "cross_segment_epsilon": randomisation_cross_segment_epsilon,
            "success_reward": randomisation_success_reward,
            "interaction_count": randomisation_interaction_count,
            "epsilon": randomisation_epsilon,
            "prior_success_reward": randomisation_prior_success_reward,
            "fail_reward": randomisation_fail_reward,
            "max_reward": randomisation_max_reward,
            "cache_duration": randomisation_cache_duration,
            "processing_window": randomisation_processing_window,
            "random_action": randomisation_random_action,
            "decay_gamma": randomisation_decay_gamma,
            "learning_rate": randomisation_learning_rate,
            "missing_offers": randomisation_missing_offers,
            "training_data_source": randomisation_training_data_source
        }
    config_doc["randomisation"] = randomisation
  
    config_doc["lookup_fields"] = []
    if virtual_variables is not None:
        config_doc["virtual_variables"] = virtual_variables
    else:
        config_doc["virtual_variables"] = []
    
    properties_list = [
        {"uuid":config_doc["uuid"], "type":"dynamic_engagement", "name":"dynamic_engagement", "database":"mongodb", "db":config_doc["score_database"], "table":config_doc["score_collection"], "update":True}
        ,{"uuid":config_doc["uuid"], "type":"dynamic_engagement_options", "name":"dynamic_engagement", "database":"mongodb", "db":config_doc["options_store_database"], "table":config_doc["options_store_collection"], "update":True}
    ]
    config_doc["properties"] = "predictor.corpora={}".format(json.dumps(properties_list))

    if create_covering_index:
        covering_index_projection = {"_id":0,"uuid":1,"optionKey":1,"alpha":1,"beta":1}
        if contextual_variables_contextual_variable_one_name != "":
            covering_index_projection["contextual_variable_one"] = 1
        if contextual_variables_contextual_variable_two_name != "":
            covering_index_projection["contextual_variable_two"] = 1
        if dynamic_eligibility is not None:
            if "options_store_fields" in dynamic_eligibility:
                projection_fields = []
                for table_iter in dynamic_eligibility["options_store_fields"]:
                    for field_iter in table_iter["fields"]:
                        projection_fields.append(field_iter)
                    index_fields = set(projection_fields)
                    for ind_field_iter in index_fields:
                        covering_index_projection[ind_field_iter] = 1
            dynamic_eligibility["projection"] = [covering_index_projection]
        else:
            dynamic_eligibility = {}
            dynamic_eligibility["projection"] = [covering_index_projection]

    if dynamic_eligibility is not None:
        config_doc["dynamic_eligibility"] = dynamic_eligibility

    if replace:
        if len([d for d in existing_configurations["data"] if d["name"] == name]) > 0:
            cp.delete_pulse_responder_dynamic(auth,score_database,score_collection,{"name":name})
        
        dme.add_documents(auth, {"database": config_doc["score_database"], "collection": config_doc["score_collection"], "document": config_doc})
        doc_delete = {
            "database": config_doc["options_store_database"]
            ,"collection": config_doc["options_store_collection"]
        }
        dme.delete_all_documents(auth, doc_delete)

    cp.save_pulse_responder_dynamic(auth, config_doc)

    cp_update_doc = {
        "type":"generateUpdatedOptions"
        ,"name":config_doc["name"]
        ,"uuid":config_doc["uuid"]
        ,"engagement_type":"binaryThompson"
        ,"feature_store_database":config_doc["feature_store_database"]
        ,"feature_store_collection":config_doc["feature_store_collection"]
        ,"contextual_variable_one_values":contextual_variable_one_values
        ,"contextual_variable_two_values":contextual_variable_two_values
        ,"contextual_variable_one_name":config_doc["contextual_variables"]["contextual_variable_one_name"]
        ,"contextual_variable_two_name":config_doc["contextual_variables"]["contextual_variable_two_name"]
        ,"contextual_variable_one_from_data_source":config_doc["contextual_variables"]["contextual_variable_one_from_data_source"]
        ,"contextual_variable_two_from_data_source":config_doc["contextual_variables"]["contextual_variable_two_from_data_source"]
        ,"contextual_variable_one_lookup":config_doc["contextual_variables"]["contextual_variable_one_lookup"]
        ,"contextual_variable_two_lookup":config_doc["contextual_variables"]["contextual_variable_two_lookup"]
        ,"offer_key":config_doc["contextual_variables"]["offer_key"]
        ,"tracking_key":config_doc["contextual_variables"]["tracking_key"]
        ,"options_store_database":config_doc["options_store_database"]
        ,"options_store_collection":config_doc["options_store_collection"]
        ,"prior_success_reward":config_doc["randomisation"]["prior_success_reward"]
        ,"prior_fail_reward":config_doc["randomisation"]["prior_fail_reward"]
        ,"take_up":config_doc["contextual_variables"]["take_up"]
        ,"dynamic_eligibility":config_doc["dynamic_eligibility"]
    }
    cp.update_client_pulse_responder(auth, cp_update_doc)

    if dynamic_eligibility is not None:
        if "options_store_fields" in dynamic_eligibility:
            for table_iter in dynamic_eligibility["options_store_fields"]:
                if table_iter["datasource"] == "mongodb":
                    dme.create_document_collection_index(auth, table_iter["database"], table_iter["collection"], {table_iter["lookup_keys"]["foreignField"]:1})
                    lookup_dict = {"$lookup":{
                        "localField":table_iter["lookup_keys"]["localField"]
                        ,"foreignField":table_iter["lookup_keys"]["foreignField"]
                        ,"from":table_iter["collection"]
                        ,"as":"subs"
                    }}
                    add_dict = {"$addFields":{}}
                    for field_iter in table_iter["fields"]:
                        add_dict["$addFields"][field_iter] = {"$arrayElemAt":[f"$subs.{field_iter}",0]}
                    table_pipeline = [
                        lookup_dict
                        ,add_dict
                        ,{"$unset":"subs"}
                        #TODO: allow for different databases once mongo version increments
                        ,{"$out":config_doc["options_store_collection"]}
                    ]
                    dme.post_mongo_db_aggregate_pipeline(auth,
                                                         {
                                                             "database": config_doc["options_store_database"]
                                                             , "collection": config_doc["options_store_collection"]
                                                             , "pipeline": table_pipeline
                                                         }
                                                         )
                elif table_iter["datasource"] == "cassandra":
                    data_check = dme.get_cassandra_sql(auth, "SELECT * FROM {} LIMIT 1".format(table_iter["collection"]))
                    if data_check["data"] == []:
                        print("WARNING: It looks like {} is empty or does not exist".format(table_iter["collection"]))
                    else:
                        sql = "SELECT * FROM {}".format(table_iter["collection"])
                        col = "temp_options_store_lookup"
                        db = config_doc["options_store_database"]
                        dme.get_cassandra_to_mongo(auth, db, col, sql)
                        dme.create_document_collection_index(auth, db, col, {table_iter["lookup_keys"]["foreignField"]:1})
                        lookup_dict = {"$lookup":{
                            "localField":table_iter["lookup_keys"]["localField"]
                            ,"foreignField":table_iter["lookup_keys"]["foreignField"]
                            ,"from":col
                            ,"as":"subs"
                        }}
                        add_dict = {"$addFields":{}}
                        for field_iter in table_iter["fields"]:
                            add_dict["$addFields"][field_iter] = {"$arrayElemAt":[f"$subs.{field_iter}",0]}
                        table_pipeline = [
                            lookup_dict
                            ,add_dict
                            ,{"$unset":"subs"}
                            #TODO: allow for different databases once mongo version increments
                            ,{"$out":config_doc["options_store_collection"]}
                        ]
                        print(table_pipeline)
                        dme.post_mongo_db_aggregate_pipeline(auth,
                                                             {
                                                                 "database": config_doc["options_store_database"]
                                                                 , "collection": config_doc["options_store_collection"]
                                                                 , "pipeline": table_pipeline
                                                             }
                                                             )

    if create_options_index:
        index_dict = {"uuid":1,"optionKey":1}
        if contextual_variables_contextual_variable_one_name != "":
            index_dict["contextual_variable_one"] = 1
        if contextual_variables_contextual_variable_one_name != "":
            index_dict["contextual_variable_two"] = 1
        index_fields = []
        if dynamic_eligibility is not None:
            if "options_store_fields" in dynamic_eligibility:
                for table_iter in dynamic_eligibility["options_store_fields"]:
                    for field_iter in table_iter["fields"]:
                        index_fields.append(field_iter)
        index_fields = set(index_fields)
        for ind_field_iter in index_fields:
            index_dict[ind_field_iter] = 1
        if create_covering_index:
            index_dict["alpha"] = 1
            index_dict["beta"] = 1
        dme.create_document_collection_index(auth, config_doc["options_store_database"], config_doc["options_store_collection"], index_dict)

    print("MESSAGE: Online learning configuration created")
    return config_doc["uuid"]


def get_dynamic_interaction_uuid(auth,dynamic_interaction_name):
    """
    Get the UUID of a dynamic interaction configuration.

    :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
    :param dynamic_interaction_name: The name of the dynamic interaction configuration.

    :return: The UUID of the dynamic interaction configuration.
    """
    # Check for existence of online learning configuration with the same name
    existing_configurations = cp.list_pulse_responder_dynamic(auth)
    selected_configuration = {}
    try:
        for config_iter in existing_configurations["data"]:
            if config_iter["name"] == dynamic_interaction_name:
                if selected_configuration == {}:
                    selected_configuration = config_iter
                elif selected_configuration["uuid"] != config_iter["uuid"]:
                    print("WARNING: More than one configuration matches the name specified")
                    raise ValueError(f"More than one configuration matches the name specified: {selected_configuration} and {config_iter}")
                elif selected_configuration["uuid"] == config_iter["uuid"]:
                    print("WARNING: More than one configuration matches the name specified")
    except Exception as error:
        print("Unexpected error occurred while getting the dynamic interaction uuid")
        raise

    return selected_configuration["uuid"]

def update_online_learning(
        auth,
        uuid,
        name=None,
        description=None,
        feature_store_collection=None,
        feature_store_database=None,
        options_store_database=None,
        options_store_collection=None,
        contextual_variables_offer_key=None,
        score_connection=None,
        score_database=None,
        score_collection=None,
        algorithm=None,
        options_store_connection=None,
        batch=None,
        feature_store_connection=None,
        contextual_variables_contextual_variable_one_from_data_source=None,
        contextual_variables_contextual_variable_one_lookup=None,
        contextual_variables_contextual_variable_one_name=None,
        contextual_variables_contextual_variable_two_from_data_source=None,
        contextual_variables_contextual_variable_two_name=None,
        contextual_variables_contextual_variable_two_lookup=None,
        contextual_variables_tracking_key=None,
        contextual_variables_take_up=None,
        batch_database_out=None,
        batch_collection_out=None,
        batch_threads=None,
        batch_collection=None,
        batch_userid=None,
        batch_contextual_variables=None,
        batch_number_of_offers=None,
        batch_database=None,
        batch_pulse_responder_list=None,
        batch_find=None,
        batch_options=None,
        batch_campaign=None,
        batch_execution_type=None,
        randomisation_calendar=None,
        randomisation_test_options_across_segment=None,
        randomisation_processing_count=None,
        randomisation_discount_factor=None,
        randomisation_batch=None,
        randomisation_prior_fail_reward=None,
        randomisation_cross_segment_epsilon=None,
        randomisation_success_reward=None,
        randomisation_interaction_count=None,
        randomisation_epsilon=None,
        randomisation_prior_success_reward=None,
        randomisation_fail_reward=None,
        randomisation_max_reward=None,
        randomisation_cache_duration=None,
        randomisation_processing_window=None,
        randomisation_random_action=None,
        randomisation_decay_gamma=None,
        randomisation_learning_rate=None,
        randomisation_missing_offers=None,
        randomisation_training_data_source=None,
        virtual_variables=None,
        lookup_fields=None,
):
    """
    Update an existing online learning configuration with a specified UUID. Note that the options store will not be refreshed as part of the update.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param uuid: The UUID of the online learning configuration to be updated.
   :param name: The name of the online learning configuration.
   :param description: The description of the online learning configuration.
   :param feature_store_collection: The collection containing the setup feature store.
   :param feature_store_database: The database containing the setup feature store.
   :param options_store_database: The database containing the options store.
   :param options_store_collection: The collection containing the options store.
   :param contextual_variables_offer_key: The key in the setup feature store collection that contains the offer.
   :param score_connection: Used when batch processing is enabled. The connection string to the runtime engine to use for batch processing.
   :param score_database: The database where the online learning configuration is stored
   :param score_collection: The collection where the online learning configuration is stored
   :param algorithm: The algorithm to use for the online learning configuration. Currently only "ecosystem_rewards", "bayesian_probabilistic" and "q_learning" are supported.
   :param options_store_connection: The connection string to the options store.
   :param batch: A boolean indicating whether batch processing should be enabled.
   :param feature_store_connection: The connection string to the setup feature store.
   :param contextual_variables_contextual_variable_one_from_data_source: A boolean indicating whether the first contextual variable should be read from the deployment customer lookup.
   :param contextual_variables_contextual_variable_one_name: The field in the setup feature store to be used for the first contextual variable.
   :param contextual_variables_contextual_variable_one_lookup: The key in the deployment customer lookup that contains the first contextual variable.
   :param contextual_variables_contextual_variable_two_name: The field in the setup feature store to be used for the second contextual variable.
   :param contextual_variables_contextual_variable_two_lookup: The key in the deployment customer lookup that contains the second contextual variable.
   :param contextual_variables_contextual_variable_two_from_data_source: A boolean indicating whether the second contextual variable should be read from the deployment customer lookup.
   :param contextual_variables_tracking_key: The field in the setup feature store to be used for the tracking key.
   :param contextual_variables_take_up: The field in the setup feature store to be used for the take-up.
   :param batch_database_out: The database to store the batch output in.
   :param batch_collection_out: The collection to store the batch output in.
   :param batch_threads: The number of threads to use for batch processing.
   :param batch_collection: The collection to read the batch data from.
   :param batch_userid: The user to be passed to the batch runtime.
   :param batch_contextual_variables: The contextual variables to be used in the batch processing.
   :param batch_number_of_offers: The number of offers to be used in the batch processing.
   :param batch_database: The database to read the batch data from.
   :param batch_pulse_responder_list: The list of runtimes to be used in the batch processing.
   :param batch_find: The query to be used to find the batch data.
   :param batch_options: The options to be used in the batch processing.
   :param batch_campaign: The campaign to be used in the batch processing.
   :param batch_execution_type: The execution type to be used in the batch processing. Allowed values are "internal" and "external".
   :param randomisation_calendar: The calendar to be used.
   :param randomisation_test_options_across_segment: Boolean variable indicating whether offers should be tested outside of their allowed contextual variable segments.
   :param randomisation_processing_count: The number of interactions to be processed.
   :param randomisation_discount_factor: The discount factor to be used in the randomisation.
   :param randomisation_batch: Boolean variable indicating whether batch processing should be enabled.
   :param randomisation_prior_fail_reward: The prior fail reward to be used in the randomisation.
   :param randomisation_cross_segment_epsilon: The cross segment epsilon to be used in the randomisation.
   :param randomisation_success_reward: The success reward to be used in the randomisation.
   :param randomisation_interaction_count: The number of interactions to be used in the randomisation.
   :param randomisation_epsilon: The epsilon to be used in the randomisation.
   :param randomisation_prior_success_reward: The prior success reward to be used in the randomisation.
   :param randomisation_fail_reward: The fail reward to be used in the randomisation.
   :param randomisation_max_reward: The maximum reward to be used in the randomisation.
   :param randomisation_cache_duration: The cache duration to be used in the randomisation.
   :param randomisation_processing_window: The processing window to be used in the randomisation.
   :param randomisation_random_action: The random action to be used in the randomisation.
   :param randomisation_decay_gamma: The decay gamma to be used in the randomisation.
   :param randomisation_learning_rate: The learning rate to be used in the randomisation.
   :param randomisation_missing_offers: The approach used to add scores for offers not present in the training set for the bayesian probabilistic algorithm. Allowed values are "none" and "uniform".
   :param randomisation_training_data_source: The data source to be used for training the q-learning algorithm. Allowed values are "feature_store" and "logging".
   :param virtual_variables: A list of virtual variables to be used in the online learning configuration.
   :param lookup_fields: The fields in the contextual variables lookup up feature store

   :return: The UUID identifier for the online learning configuration which should be linked to the deployment for the project.
    """
    # Check for existence of online learning configuration with the same name
    if not isinstance(uuid, str):
        raise TypeError("uuid should be a string")

    try:
        existing_configurations = cp.list_pulse_responder_dynamic(auth)["data"]
        selected_configuration = {}
        for config_iter in existing_configurations:
            if config_iter["uuid"] == uuid:
                if selected_configuration != {}:
                    raise ValueError(
                        f"More than one configuration matches the name or uuid specified: {selected_configuration} and {config_iter}")
                selected_configuration = config_iter

        if selected_configuration == {}:
            raise ValueError(f"No configuration matches the name or uuid specified")
    except Exception as error:
        print("Unexpected error occurred while extracting Dynamic Interaction configuration for specified name or uuid")
        raise

    if randomisation_missing_offers is not None:
        if not isinstance(randomisation_missing_offers, str):
            raise TypeError("randomisation_missing_offers should be a string")
        if randomisation_missing_offers not in ["none", "uniform"]:
            raise ValueError("randomisation_missing_offers should be either 'none' or 'uniform'")

    if algorithm is not None:
        if algorithm not in ["ecosystem_rewards","bayesian_probabilistic","q_learning"]:
            raise ValueError("algorithm must be ecosystem_rewards, bayesian_probabilistic or q_learning algorithm for other algorithms please use the "
                             "ecosystem.Ai workbench")

    # Initialise configuration document and store input parameters
    if name is not None: selected_configuration["name"] = name
    if description is not None: selected_configuration["description"] = description

    if feature_store_collection is not None: selected_configuration["feature_store_collection"] = feature_store_collection
    if feature_store_database is not None: selected_configuration["feature_store_database"] = feature_store_database
    if feature_store_connection is not None: selected_configuration["feature_store_connection"] = feature_store_connection

    if options_store_database is not None: selected_configuration["options_store_database"] = options_store_database
    if options_store_collection is not None: selected_configuration["options_store_collection"] = options_store_collection
    if options_store_connection is not None: selected_configuration["options_store_connection"] = options_store_connection

    if score_collection is not None: selected_configuration["score_collection"] = score_collection
    if score_database is not None: selected_configuration["score_database"] = score_database
    if score_connection is not None: selected_configuration["score_connection"] = score_connection

    if batch is not None: selected_configuration["batch"] = batch
    #if name is not None: selected_configuration["options"] = []
    selected_configuration["date_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
    if description is not None: selected_configuration["description"] = description

    # Get values for contextual variables
    update_contextual_variable_one_values = False
    update_contextual_variable_two_values = False
    if contextual_variables_contextual_variable_one_name is not None:
        update_contextual_variable_one_values = True
    if contextual_variables_contextual_variable_two_name is not None:
        update_contextual_variable_two_values = True
    if feature_store_database is not None or feature_store_collection is not None:
        update_contextual_variable_one_values = True
        update_contextual_variable_two_values = True

    contextual_variable_one_values = None
    if update_contextual_variable_one_values:
        if contextual_variables_contextual_variable_one_name is None:
            contextual_variables_contextual_variable_one_name = selected_configuration["contextual_variables"]["contextual_variable_one_name"]
        contextual_variable_one_values_pipeline = [
            {"$group":{"_id":"None","values":{"$addToSet":"$"+contextual_variables_contextual_variable_one_name}}}
        ]
        contextual_variable_one_values = dme.post_mongo_db_aggregate_pipeline(
            auth,
            {"database": feature_store_database, "collection": feature_store_collection, "pipeline": contextual_variable_one_values_pipeline}
        )[0]["values"]

    contextual_variable_two_values = None
    if update_contextual_variable_two_values:
        if contextual_variables_contextual_variable_two_name is None:
            contextual_variables_contextual_variable_two_name = selected_configuration["contextual_variables"]["contextual_variable_two_name"]
        contextual_variable_two_values_pipeline = [
            {"$group":{"_id":"None","values":{"$addToSet":"$"+contextual_variables_contextual_variable_two_name}}}
        ]
        contextual_variable_two_values = dme.post_mongo_db_aggregate_pipeline(
            auth,
            {"database": feature_store_database, "collection": feature_store_collection, "pipeline": contextual_variable_two_values_pipeline}
        )[0]["values"]

    contextual_variables = selected_configuration["contextual_variables"]
    if contextual_variables_offer_key is not None: contextual_variables["offer_key"] = contextual_variables_offer_key
    if contextual_variables_contextual_variable_one_from_data_source is not None: contextual_variables["contextual_variable_one_from_data_source"] = contextual_variables_contextual_variable_one_from_data_source
    if contextual_variables_contextual_variable_one_lookup is not None: contextual_variables["contextual_variable_one_lookup"] = contextual_variables_contextual_variable_one_lookup
    if contextual_variables_contextual_variable_one_name is not None: contextual_variables["contextual_variable_one_name"] = contextual_variables_contextual_variable_one_name
    if contextual_variable_one_values is not None: contextual_variables["contextual_variable_one_values"] = contextual_variable_one_values
    if contextual_variables_contextual_variable_two_from_data_source is not None: contextual_variables["contextual_variable_two_from_data_source"] = contextual_variables_contextual_variable_two_from_data_source
    if contextual_variables_contextual_variable_two_name is not None: contextual_variables["contextual_variable_two_name"] = contextual_variables_contextual_variable_two_name
    if contextual_variables_contextual_variable_two_lookup is not None: contextual_variables["contextual_variable_two_lookup"] = contextual_variables_contextual_variable_two_lookup
    if contextual_variable_two_values is not None: contextual_variables["contextual_variable_two_values"] = contextual_variable_two_values
    if contextual_variables_tracking_key is not None: contextual_variables["tracking_key"] = contextual_variables_tracking_key
    if contextual_variables_take_up is not None: contextual_variables["take_up"] = contextual_variables_take_up

    if algorithm == "bayesian_probabilistic":
        training_variable_sample = dme.get_data(auth, feature_store_database, feature_store_collection, {}, 1, {}, 0)
        training_variables = list(training_variable_sample.keys())
        for rem_iter in [contextual_variables_offer_key,contextual_variables_tracking_key,contextual_variables_take_up,"_id"]:
            if rem_iter in training_variables:
                training_variables.remove(rem_iter)
        training_variables_dict = {}
        for training_variable_iter in training_variables:
            training_variable_values_pipeline = [
                {"$group":{"_id":"None","values":{"$addToSet":"$"+training_variable_iter}}}
            ]
            training_variable_values = dme.post_mongo_db_aggregate_pipeline(
                    auth,
                    {"database": feature_store_database, "collection": feature_store_collection, "pipeline": training_variable_values_pipeline}
            )[0]["values"]
            training_variables_dict[training_variable_iter] = training_variable_values
        contextual_variables["training_variable_values"] = training_variables_dict
    selected_configuration["contextual_variables"] = contextual_variables

    batch_settings = selected_configuration["batch_settings"]
    if batch_database_out is not None: batch_settings["database_out"] = batch_database_out
    if batch_collection_out is not None: batch_settings["collection_out"] = batch_collection_out
    if batch_threads is not None: batch_settings["threads"] = batch_threads
    if batch_collection is not None: batch_settings["collection"] = batch_collection
    if batch_userid is not None: batch_settings["userid"] = batch_userid
    if batch_contextual_variables is not None: batch_settings["contextual_variables"] = batch_contextual_variables
    if batch_number_of_offers is not None: batch_settings["number_of_offers"] = batch_number_of_offers
    if batch_pulse_responder_list is not None: batch_settings["pulse_responder_list"] = batch_pulse_responder_list
    if batch_database is not None: batch_settings["database"] = batch_database
    if batch_find is not None: batch_settings["find"] = batch_find
    if batch_options is not None: batch_settings["options"] = batch_options
    if batch_campaign is not None: batch_settings["campaign"] = batch_campaign
    if batch_execution_type is not None: batch_settings["execution_type"] = batch_execution_type
    selected_configuration["batch_settings"] = batch_settings

    approach = None
    if algorithm == "ecosystem_rewards":
        approach = "binaryThompson"
    elif algorithm == "bayesian_probabilistic":
        approach = "naiveBayes"
    elif algorithm == "q_learning":
        approach = "Q-Learning Algorithm"
    randomisation = selected_configuration["randomisation"]
    if randomisation_calendar is not None: randomisation["calendar"] =  randomisation_calendar
    if randomisation_test_options_across_segment is not None: randomisation["test_options_across_segment"] = randomisation_test_options_across_segment
    if randomisation_processing_count is not None: randomisation["processing_count"] = randomisation_processing_count
    if randomisation_discount_factor is not None: randomisation["discount_factor"] = randomisation_discount_factor
    if randomisation_batch is not None: randomisation["batch"] = randomisation_batch
    if randomisation_prior_fail_reward is not None: randomisation["prior_fail_reward"] = randomisation_prior_fail_reward
    if approach is not None: randomisation["approach"] = approach
    if randomisation_cross_segment_epsilon is not None: randomisation["cross_segment_epsilon"] = randomisation_cross_segment_epsilon
    if randomisation_success_reward is not None: randomisation["success_reward"] = randomisation_success_reward
    if randomisation_interaction_count is not None: randomisation["interaction_count"] = randomisation_interaction_count
    if randomisation_epsilon is not None: randomisation["epsilon"] = randomisation_epsilon
    if randomisation_prior_success_reward is not None: randomisation["prior_success_reward"] = randomisation_prior_success_reward
    if randomisation_fail_reward is not None: randomisation["fail_reward"] = randomisation_fail_reward
    if randomisation_max_reward is not None: randomisation["max_reward"] = randomisation_max_reward
    if randomisation_cache_duration is not None: randomisation["cache_duration"] = randomisation_cache_duration
    if randomisation_processing_window is not None: randomisation["processing_window"] = randomisation_processing_window
    if randomisation_random_action is not None: randomisation["random_action"] = randomisation_random_action
    if randomisation_decay_gamma is not None: randomisation["decay_gamma"] = randomisation_decay_gamma
    if randomisation_learning_rate is not None: randomisation["learning_rate"] = randomisation_learning_rate
    if randomisation_missing_offers is not None: randomisation["missing_offers"] = randomisation_missing_offers
    if randomisation_training_data_source is not None: randomisation["training_data_source"] = randomisation_training_data_source
    selected_configuration["randomisation"] = randomisation

    if lookup_fields is not None: selected_configuration["lookup_fields"] = lookup_fields
    if virtual_variables is not None: selected_configuration["virtual_variables"] = virtual_variables

    properties_list = [
        {"uuid":selected_configuration["uuid"], "type":"dynamic_engagement", "name":"dynamic_engagement", "database":"mongodb", "db":selected_configuration["score_database"], "table":selected_configuration["score_collection"], "update":True}
        ,{"uuid":selected_configuration["uuid"], "type":"dynamic_engagement_options", "name":"dynamic_engagement", "database":"mongodb", "db":selected_configuration["options_store_database"], "table":selected_configuration["options_store_collection"], "update":True}
    ]
    selected_configuration["properties"] = "predictor.corpora={}".format(json.dumps(properties_list))

    cp.save_pulse_responder_dynamic(auth, selected_configuration)

    print("MESSAGE: Online learning configuration updated")
    return selected_configuration["uuid"]