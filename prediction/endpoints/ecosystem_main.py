# Ecosystem Main
# Ecosystem Main Admin
CREATE = {
	"type": "post",
	"endpoint": "/create",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}

PROFILES = {
	"type": "get",
	"endpoint": "/profiles",
	"call_message": "{type} {endpoint}",
	"error_message": "{type} {endpoint} {response_code}"
}
