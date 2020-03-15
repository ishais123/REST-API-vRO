var operation = "/slack/api/v1.0/message";
var method = "POST";
var body = {"vlan_id": id, "vlan_name": name};
var payload = JSON.stringify(body);

var request = netApi.createRequest(method , operation , payload)
request.setHeader("Content-Type" , "application/json")
var out = request.execute()
var out_str = out.contentAsString
System.log("Slack message sent!")
