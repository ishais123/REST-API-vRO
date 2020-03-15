var operation = "/api/v1/logical-switches";
var method = "POST";
var body = {"_revision": 0, "display_name": name, "transport_zone_id": "91045f1d-1e1d-4188-833f-2936dba17030", "vlan": id, "admin_state": "UP"};
var payload = JSON.stringify(body);

var request = nsxManager.createRequest(method , operation , payload)
request.setHeader("Content-Type" , "application/json")
var out = request.execute()
var out_str = out.contentAsString
System.log("logical switch " + name + " confiured in nsx with vlan id " + id)
