Management
----------------

To retrieve a list of random ingredients,
you can use the ``management.create_deployment()`` function:

.. py:function:: management.online_learning_ecosystem_rewards_setup_feature_store(auth,offer_db,offer_collection,offer_name_column,contextual_variables,setup_feature_store_db,setup_feature_store_collection)

   Add contextual variables to a setup feature store for the ecosystem rewards dynamic recommender using a collection containing the relevant offers.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param offer_db: The database containing the offers.
   :param offer_collection: The collection containing the offers.
   :param offer_name_column: The column in the collection containing the offer names.
   :param contextual_variables: A dictionary containing the contextual variables names as keys. Each value in the dictionary should be a list containing the possible values of the contextual variables.
   :param setup_feature_store_db: The database to store the setup feature store in.
   :param setup_feature_store_collection: The collection to store the setup feature store in.

.. py:function:: management.create_online_learning(auth,name,description,feature_store_collection,feature_store_database,options_store_database,options_store_collection,contextual_variables_offer_key[,score_connection = "http://ecosystem-runtime:8091",score_database = "ecosystem_meta",score_collection = "dynamic_engagement",algorithm = "ecosystem_rewards",options_store_connection = "",batch = "false",feature_store_connection = "",contextual_variables_contextual_variable_one_from_data_source = False,contextual_variables_contextual_variable_one_lookup = "",contextual_variables_contextual_variable_one_name = "",contextual_variables_contextual_variable_two_from_data_source = False,contextual_variables_contextual_variable_two_name = "",contextual_variables_contextual_variable_two_lookup = "",contextual_variables_tracking_key = "",contextual_variables_take_up = "",batch_database_out = "",batch_collection_out = "",batch_threads = 1,batch_collection = "",batch_userid = "",batch_contextual_variables = "",batch_number_of_offers = 1,batch_database = "",batch_pulse_responder_list = "",batch_find = "{}",batch_options = "",batch_campaign = "",batch_execution_type = "",randomisation_calendar = "None",randomisation_test_options_across_segment = "",randomisation_processing_count = 1000,randomisation_discount_factor = 0.75,randomisation_batch = "false",randomisation_prior_fail_reward = 0.1,randomisation_cross_segment_epsilon = 0,randomisation_success_reward = 1,randomisation_interaction_count = "0",randomisation_epsilon = 0,randomisation_prior_success_reward = 1,randomisation_fail_reward = 0.1,randomisation_max_reward = 10,randomisation_cache_duration = 0,randomisation_processing_window = 86400000,randomisation_random_action = 0.2,randomisation_decay_gamma = "1",randomisation_learning_rate = 0.25,replace = False])

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
   :param algorithm: The algorithm to use for the online learning configuration. Currently only "ecosystem_rewards" is supported.
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
   :param contextual_variables_take_up: The field in the setup feature store to be used for the take up.
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
   :param replace: A boolean indicating whether the online learning configuration should be replaced if it already exists.

   :return: The UUID identifier for the online learning configuration which should be linked to the deployment for the project. 

.. py:function:: management.create_project(auth,project_id,project_description,project_type,purpose,project_start_date,project_end_date,data_science_lead,data_lead)

   Create a new project

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param project_id: The name of the project to be created.
   :param project_description: Description of the project.
   :param project_type: The type of the project.
   :param purpose: The purpose of the project.
   :param project_start_date: The start date of the project.
   :param project_end_date: The end date of the project.
   :param data_science_lead: The data science lead of the project.
   :param data_lead: The data lead of the project.

.. py:function:: management.create_deployment(auth,project_id,deployment_id,description,plugin_pre_score_class,plugin_post_score_class,version,project_status,[budget_tracker="default",complexity="Low",performance_expectation="High",model_configuration="default",setup_offer_matrix="default",multi_armed_bandit="default",whitelist="default",model_selector="default",pattern_selector="default",logging_collection_response="ecosystemruntime_response",logging_collection="ecosystemruntime",logging_database="logging",mongo_connect="mongodb://ecosystem_user:EcoEco321@ecosystem-server:54445/?authSource=admin",mongo_server_port="ecosystem-server:54445",mongo_ecosystem_password="EcoEco321",mongo_ecosystem_user="ecosystem_user",scoring_engine_path_dev="http://ecosystem-runtime:8091",scoring_engine_path_test="http://ecosystem-runtime2:8091",scoring_engine_path_prod="http://ecosystem-runtime3:8091",models_path="/data/deployed/",data_path="/data/",build_server_path="",git_repo_path_branch="",download_path="",git_repo_path="",parameter_access="default",corpora="default",extensive_validation=False])

   Create or update a deployment linked to an existing project.

   :param auth: Token for accessing the ecosystem-server. Created using the jwt_access package.
   :param project_id: The name of the project to add the deployment step to.
   :param deployment_id: The name of the deployment step that is to be created.
   :param description: Description of the deployment step
   :param version: The version of the deployment step being created. The combination of version and deployment_id cannot already exists within the deployment, i.e. you cannot overwrite an existing deployment
   :param project_status: Specifies the environment to which the deployment should be sent when it is pushed. The allowed values are experiment, validate, production, disable.
   :param plugin_pre_score_class: The name of the pre score logic class to be used in the runtime. Only default classes can be selected here. To create custom classes please use the ecosystem-runtime-locabuild repo or edit the classes in the workbench. The allowed values are PrePredictCustomer.java
   :param plugin_post_score_class: The name of the post score logic class to be used in the runtime. Only default classes can be selected here. To create custom classes please use the ecosystem-runtime-locabuild repo or edit the classes in the workbench. The allowed values are PostScoreBasic.java, PostScoreRecommender.java, PlatformDynamicEngagement.java, PostScoreRecommenderOffers.java, PostScoreRecommenderMulti.java and PostScoreNetwork.java
   :param budget_tracker: A dictionary of parameters required for managing the budget tracker functionality TODO <Need input from Jay on how this actually works>
   :param complexity: Indicate the expected complexity of the deployment, allowed values are Low, Medium and High
   :param performance_expectation: Indicate the expected performance of the deployment, allowed values are Low, Medium and High
   :param model_configuration: A dictionary of the parameters specifying the models used in the project. The key item in the dictionary is models_load - a comma separated string of the names of the models to be used in the deployment. model_note and model_outline fields can also be added for tracking purposes
   :param setup_offer_matrix: A dictionary of parameters specifying the location of the offer matrix - a dataset containing information about the offers that could be recommended. The dictionary must contain a datasource, database, collection and offer_lookup_id. Datasource can be one of mongodb, cassandra or presto. Database and collection specify the location of the offer_matrix in the datasource. Offer_lookup_id is the name of the column which contains the unique identifier for the offers - allowed values are offer, offer_name and offer_id
   :param multi_armed_bandit: A dictionary specifying the dynamic recommender behavior of the deployment. The dictionary must contain epsilon, duration and pulse_responder_id. epsilon is a portion of interactions that are presented with random results and should be a number between 0 and 1. duration is the period for which recommendations are cached in milliseconds TODO <Check this with Jay> . pulse_responder_id is the uuid of a Dynamic Interaction configuration, if not Dynamic Interaction configuration is being linked set this to ""
   :param whitelist: A dictionary of parameters specifying the location of the whitelist - a dataset of customers and the list of offers for which they are eligible. The data set should contain two fields; customer_key and white_list. customer_key is the unique customer identifier and white_list is a list of offer_names for which the customer is eligible. The dictionary must contain a datasource, database and collection. Datasource can be one of mongodb, cassandra or presto. Database and collection specify the location of the whitelist in the datasource.
   :param model_selector: TODO <Check purpose of lookup field with Jay> A dictionary of parameters specifying the behavior of the model selector functionality. The model selector allows different models to be used based on the value of a field in the specified data set. The dictionary must contain datasource, database, table_collection, selector_column, selector and lookup.  Datasource can be one of mongodb, cassandra or presto. Database and collection specify the location of the model_selector dataset in the datasource. The selector_column is the name of the column in the dataset which is used to select between the different models. Lookup is a dictionary with the structure {"key":"customer","value":123 or '123',"fields'':"selector_column"}, where key is the field containing the unique customer identifier, value specified the type of the identifier as either a string ('123') or a number (123) and fields is the name of the selector column. Selector is the rule set used to choose models based on the values in the selector column. Selector is a dictionary with the format {"key_value_a":[0],"key_value_b":[1], ...} where the keys are the values of the fields in the selector column used to choose different models and the values are the indices of the model to be used, with the order as specified in the model_configuration argument
   :param pattern_selector: TODO <Check pattern selector behavior with Jay> A dictionary containing the parameters defining the behavior of the pattern selector. The dictionary contains two parameters; pattern and duration. pattern is a comma separated list of numbers which specifies the intervals at which customers are able to receive updated offers. duration defines the time intervals specified in the pattern parameter
   :param parameter_access: A dictionary specifying the location from which customer data should be looked up. parameter_access should contain lookup, datasource, database, table_collection, lookup, lookup_defaults, fields, lookup_fields, create_virtual_variables and virtual_variables. lookup is a dictionary with the structure {"key":"customer","value":123 or '123'}, where key is the field containing the unique customer identifier, value specified the type of the identifier as either a string ('123') or a number (123). datasource can be one of mongodb, cassandra or presto. database and table_collection specify the location of the customer lookup in the datasource. fields is a comma separated list of the fields that should be read from the customer lookup. lookup_defaults are the default values to be used if the customer lookup fails, set to "" to not specify defaults. lookup_fields is the fields parameter in a list form ordered alphabetically create_virtual_variable is True if virtual variables are defined and False if not, virtual variables are defined by segmenting or combining fields from the customer lookup for us in the deployment. virtual_variables is a dictionary defining the virtual variables, which has the following form.
   :param corpora: A list of additional datasets that are read by the deployment. corpora is a list of dictionaries where each dictionary gives the details of a data set. The dictionaries must have the following keys; database (mongodb or cassandra), db (the database containing the corpora), table (the collection containing the corpora), name (the name of the corpora used in the deployment) and type (static, dynamic or experiment). The dictionary can optionally contain a key field which, if present, is used as a lookup for each row or the corpora, where the default is to have the rows loaded as an array. The type field in the dictionary specifies how the corpora is loaded. A static type is loaded at deployment, a dynamic type is loaded at each prediction and experiment is a special type used for configuring network runtimes
   :param logging_database: The mongo database where the deployment logs will be stored
   :param logging_collection: The mongo collection where the predictions presented will be stored
   :param logging_collection_response: The mongo collection where the customer responses to the predictions will be stored
   :param mongo_connect: The connection string to the mongo database used by the deployment
   :param mongo_server_port: The server and port in the mongo connection string
   :param mongo_ecosystem_password: The password in the mongo connection string
   :param mongo_ecosystem_user: The username in the mongo connection string
   :param scoring_engine_path_dev: The url of the container to send the configuration to when the project status is experiment
   :param scoring_engine_path_test: The url of the container to send the configuration to when the project status is validate
   :param scoring_engine_path_prod: The url of the container to send the configuration to when the project status is production
   :param models_path: The folder in the container where the models will be stored
   :param data_path: The folder in the container where the generic data used by the container will be stored
   :param build_server_path: The url of the build server to be used if customer logic is built into the container and a new container needs to be built containing said logic
   :param git_repo_path: The git repo to store the customer logic
   :param git_repo_path_branch: The branch to use for the repo specified in git_repo_path_branch
   :param download_path: The url on Docker Hub where the built container will be pushed
   :param extensive_validation: Indicator of whether potentially time consuming validation should be run before the deployment is created. This additional validation is checking whether the fields in the model_parameter are present in the linked collection and vice-versa

   :return: The deployment configuration.