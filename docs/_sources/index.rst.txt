.. Ecosystem Notebooks documentation master file, created by
   sphinx-quickstart on Thu Apr  4 07:58:30 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ecosystem Notebooks
===================

The Ecosystem Notebooks python package provides access to the ecosystem.Ai real-time, interaction science platform - details of which can be found on the ecosystem.Ai developer site https://developer.ecosystem.ai/docs/

Installation
------------

Install ecosystem.Ai by following either the local setup guide (https://developer.ecosystem.ai/docs/quick_start/local_setup) or the cloud marketplace setup guide (https://developer.ecosystem.ai/docs/quick_start/marketplace).

To use Ecosystem Notebooks, install it using pip:

.. code-block:: console

   (.venv) $ pip install ecosystem-notebooks

Connect to ecosystem.Ai using the url of your ecosystem.Ai server and a valid username and password for your server:

.. code-block:: python

   from prediction import jwt_access
   auth = jwt_access.Authenticate("http://ecosystem-server:3001/api", "ecosystem_username", "ecosystem_password")

If everything is set up correctly a ``Login Successful.`` message will be displayed.

Get Started
-----------

The Ecosystem Notebooks package provides two main modules: `prediction` and `runtime`. The `prediction` module is used to interact with the server APIs of ecosystem.Ai, while the `runtime` module is used to interact with the runtime APIs of ecosystem.Ai.

Here we'll work through configuring your first deployment using a pretrained H2O.ai model using the server. Pushing the deployment to a runtime instance and testing the response received from the runtime instance.

.. code-block:: python

   #Import the required ecosystem.Ai modules
   from prediction.apis import deployment_management as dm
   from prediction.apis import ecosystem_generation_engine as ge
   from prediction.apis import data_management_engine as dme
   from prediction.apis import online_learning_management as ol
   from prediction.apis import prediction_engine as pe
   from prediction.apis import worker_file_service as fs
   from prediction import jwt_access
   from runtime.apis import predictor_engine as o
   from runtime import access
   import pprint

   #Authenticate with the ecosystem.Ai server
   auth = jwt_access.Authenticate("http://ecosystem-server:3001/api", "ecosystem_username", "ecosystem_password")

   #The name and details of of the project and deployment on which you will be working.
   project_id = "demo_project"
   project_description = "Demo project for ecosystem.Ai"
   project_type = "Recommender"
   purpose = "Demo"
   project_start_date = "2024-01-01"
   project_end_date = "2024-01-31"
   data_science_lead = "ecosystem.Ai"
   data_lead = "ecosystem.Ai"
   deployment_id = "simple_model_deployment"
   deployment_description = "Simple model deployment using a pretrained H2O.ai model"
   runtime_path="http://localhost:8014"

   #Create a project. This set is not required if you will be working in an existing project
   dm.create_project(auth,project_id,project_description,project_type,purpose,project_start_date,project_end_date,data_science_lead,data_lead)

   model_configuration = define_deployment_model_configuration(models_to_load=["model_id"])

   #Configure the lookup to the customer feature store
   parameter_access = dm.define_deployment_parameter_access(
       auth,
       lookup_key="msisdn",
       lookup_type="int",
       database="prod_estore_gsm_recommender",
       table_collection="fs_score_all_estore_gsm_recommender_rel_1",
       datasource="mongodb",
       virtual_variables=virtual_variables
   )

   #Create your deployment
   version = "001"
   deployment_step = dm.create_deployment(
       auth,
       project_id=project_id,
       deployment_id=deployment_id,
       description=deployment_description,
       version=version,
       plugin_post_score_class="PostScoreBasic.java",
       plugin_pre_score_class="PrePredictCustomer.java",
       scoring_engine_path_dev=runtime_path,
       mongo_connect="mongodb://mongouser:mongopassword@ecosystem-server:54445/?authSource=admin",
       parameter_access=parameter_access,
       model_configuration=model_configuration,
   )

   #Push deployment and produce properties file
   push_result = ge.process_push(auth_local,deployment_step)
   if "ErrorMessage" in push_result:
       print(push_result["ErrorMessage"])
   else:
       print(push_result["properties"])

   #Test your deployment
   post_invocations_input = {
                               "campaign": deployment_id
                             , "subcampaign": "none"
                             , "channel": "notebooks"
                             , "customer": 12345
                             , "userid": "test"
                             , "numberoffers": 2
                             , "params": "{}"
                           }
   offer_response = o.invocations(auth_runtime, post_invocations_input)
   pp.pprint(offer_response)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   prediction.rst
   prediction.apis.rst
   runtime.rst
   runtime.apis.rst
   modules.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
