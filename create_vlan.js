var restHost = RESTHostManager.createHost("DynamicRequest");
var transientHost = RESTHostManager.createTransientHostFrom(restHost);
var baseUrl = "http://172.16.20.33"
transientHost.url = baseUrl;
var contentType = "application/json"

var ciscoUri = "/cisco/api/v1.0/vlan"
var ciscoData = {"vlan_id": id, "vlan_name": name};
var ciscoPayload = JSON.stringify(ciscoData);
var requestUrl = baseUrl + ciscoUri;
System.log("Request full URL: " + requestUrl);
var request = transientHost.createRequest("POST", ciscoUri, ciscoPayload);
request.contentType = contentType;
var response;
response = request.execute();

var arubaUri = "/aruba/api/v1.0/vlan"
var arubaData = {"vlan_id": id, "vlan_name": name};
var arubaPayload = JSON.stringify(arubaData);
var requestUrl = baseUrl + arubaUri;
System.log("Request full URL: " + requestUrl);
var request = transientHost.createRequest("POST", arubaUri, arubaPayload);
request.contentType = contentType;
var response;
response = request.execute();

var fortiUri = "/forti/api/v1.0/vlan"
var fortiData = {"vlan_id": id, "vlan_name": name, "gateway": gateway, "mask": mask};
var fortiPayload = JSON.stringify(fortiData);
var requestUrl = baseUrl + fortiUri;
System.log("Request full URL: " + requestUrl);
var request = transientHost.createRequest("POST", fortiUri, fortiPayload);
request.contentType = contentType;
var response;
response = request.execute();


System.log("Content as string: " + response.contentAsString);

statusCode = response.statusCode;
statusCodeAttribute = statusCode;
System.log("Status code: " + statusCode);
contentLength = response.contentLength;
headers = response.getAllHeaders();
contentAsString = response.contentAsString;
System.log("Content as string: " + contentAsString);

