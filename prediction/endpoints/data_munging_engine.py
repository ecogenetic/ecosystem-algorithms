# Data Munging Engine
CONCAT_COLUMNS2 = {
	"type": "get",
	"endpoint": "/2/concatColumns",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DATE_ENRICH2 = {
	"type": "get",
	"endpoint": "/2/dateEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
AUTO_NORMALIZE_ALL = {
	"type": "get",
	"endpoint": "/autoNormalizeAll",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
CONCAT_COLUMNS = {
	"type": "get",
	"endpoint": "/concatColumns",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
DATE_ENRICH = {
	"type": "get",
	"endpoint": "/dateEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
ENUM_CONVERT = {
	"type": "get",
	"endpoint": "/enumConvert",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FILL_ZEROS = {
	"type": "get",
	"endpoint": "/fillZeros",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FILL_VALUES = {
	"type": "get",
	"endpoint": "/fillValues",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FOREIGN_KEY_AGGREGATOR = {
	"type": "get",
	"endpoint": "/foreignKeyAggregator",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FOREIGN_KEY_LOOKUP = {
	"type": "get",
	"endpoint": "/foreignKeyLookup",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FRAGMENT_ENRICH = {
	"type": "get",
	"endpoint": "/fragmentEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
FRAGMENT_ENRICH2 = {
	"type": "get",
	"endpoint": "/fragmentEnrich2",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GENERATE_FEATURES = {
	"type": "get",
	"endpoint": "/generateFeatures",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GENERATE_FEATURES_NORMALIZE = {
	"type": "get",
	"endpoint": "/generateFeaturesNormalize",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_CATEGORIES = {
	"type": "get",
	"endpoint": "/getCategories",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GET_CATEGORIES_RATIOS = {
	"type": "get",
	"endpoint": "/getCategoriesRatios",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
LOCATION_ENRICH = {
	"type": "get",
	"endpoint": "/locationEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
MCC_ENRICH = {
	"type": "get",
	"endpoint": "/mccEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
PREDICTION_ENRICH = {
	"type": "get",
	"endpoint": "/predictionEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
PREDICTION_ENRICH_FAST_GET = {
	"type": "get",
	"endpoint": "/predictionEnrichFast",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
SIC_ENRICH = {
	"type": "get",
	"endpoint": "/sicEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
PROCESS_CLIENT_PULSE_RELIABILITY = {
	"type": "get",
	"endpoint": "/processClientPulseReliability",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
GENERATE_TIME_SERIES_FEATURES = {
	"type": "get",
	"endpoint": "/generateTimeSeriesFeatures",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

PERSONALITY_ENRICH = {
	"type": "get",
	"endpoint": "/personalityEnrich",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

MUNGE_TRANSACTIONS_AGGREGATE = {
	"type": "get",
	"endpoint": "/mungeTransactionsAggregate",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

MUNGE_TRANSACTIONS = {
	"type": "get",
	"endpoint": "/mungeTransactions",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

FLATTEN_DOCUMENT = {
	"type": "get",
	"endpoint": "/flattenDocument",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

DELETE_KEY = {
	"type": "get",
	"endpoint": "/deleteKey",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

NLP_WORKER = {
	"type": "get",
	"endpoint": "/nlpWorker",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

DELETE_MANY_DOCUMENTS = {
	"type": "get",
	"endpoint": "/deleteManyDocuments",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

PROCESS_RANGE = {
	"type": "get",
	"endpoint": "/processRange",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

PREDICTION_ENRICH_FAST_POST = {
	"type": "post",
	"endpoint": "/predictionEnrichFast",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"	
}

POST_ECOSYSTEM_REWARDS_EXPLORATION = {
	"type": "post",
	"endpoint": "/postEcosystemRewardsExploration",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

POST_ECOSYSTEM_REWARDS_EXPLORATION_APPROX = {
	"type": "post",
	"endpoint": "/postEcosystemRewardsExplorationApprox",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

POST_ECOSYSTEM_REWARDS_EXPLORE_APPROX_CONTEXT = {
	"type": "post",
	"endpoint": "/postEcosystemRewardsExploreApproxContext",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

POST_ECOSYSTEM_REWARDS_BETA_DISTRIBUTION_BOX_PLOTS = {
	"type": "post",
	"endpoint": "/postEcosystemRewardsBetaDistributionBoxPlots",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}