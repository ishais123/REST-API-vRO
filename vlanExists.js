if (exists == "id" || exists == "false")
{
	System.log("Vlan already exists")
	return false
}

if (exists == "name")
{
	System.log("Vlan name already exists")
	return false
}

if (exists == "true")
{
	System.log("Pre-check passed, starting to configure the VLAN....")
	return true
}
