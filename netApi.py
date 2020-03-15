#!/usr/bin/python3

import paramiko
from netmiko import Netmiko
import time
from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
import requests
import json


def connect(host, user, password, conf):
    twrssh = paramiko.SSHClient()
    twrssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    twrssh.connect(hostname=host, port=22, username=user, password=password, look_for_keys=False)
    remote = twrssh.invoke_shell()
    remote.send('term len 0\n')
    for command in conf:
        remote.send(f' {command} \n')
        time.sleep(2)
        buf = remote.recv(65000)
        output = buf.decode('utf-8')
    twrssh.close()


app = Flask(__name__)

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'tsadmin':
        return 'Bpovtmg1!'
    return None

#                  Error Handling                     #
#######################################################
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'bad request'}), 400)
#######################################################


# devices list
devices = {"cisco": {"host": "172.16.200.2", "username": "tsadmin", "password": "Bpovtmg1!"},
           "aruba_up": {"host": "192.168.100.201", "username": "admin", "password": "abc123"},
           "aruba_down": {"host": "192.168.100.200", "username": "admin", "password": "abc123"},
           "forti": {"host": "172.16.20.1", "username": "terasky", "password": "bpovtm315"}}

#                  Devices details                    #
#######################################################
cisco_host = devices.get('cisco').get('host')
cisco_username = devices.get('cisco').get('username')
cisco_password = devices.get('cisco').get('password')
aruba_up_host = devices.get('aruba_up').get('host')
aruba_down_host = devices.get('aruba_down').get('host')
aruba_username = devices.get('aruba_up').get('username')
aruba_password = devices.get('aruba_up').get('password')
forti_host = devices.get('forti').get('host')
forti_username = devices.get('forti').get('username')
forti_password = devices.get('forti').get('password')
#######################################################

# Cisco calls
@app.route('/cisco/api/v1.0/vlan', methods=['POST'])
# @auth.login_required
def cisco_add_vlan():
    req_data = request.get_json(force=True)
    vlan_id = req_data['vlan_id']
    vlan_name = req_data['vlan_name']
    cisco_conf = ['conf t', f'vlan {vlan_id}', f'name {vlan_name}', 'end', 'wr']
    connect(cisco_host, cisco_username, cisco_password, cisco_conf)
    text = {"vlan_id": f"{vlan_id}", "vlan_name": f"{vlan_name}"}
    return jsonify(text)


@app.route('/cisco/api/v1.0/vlan', methods=['POST'])
def check_if_vlan_exists():
    req_data = request.get_json(force=True)
    vlan_id = req_data['vlan_id']
    vlan_name = req_data['vlan_name']
    cisco = {'device_type': 'cisco_ios', 'ip': '172.16.200.2', 'username': 'tsadmin', 'password': 'Bpovtmg1!'}
    switches = [cisco]
    for devices in switches:
        net_connect = Netmiko(**devices)
        command = "show vlan"
        # print()
        # print(net_connect.find_prompt())
        output = net_connect.send_command(command)
        net_connect.disconnect()
        lines = output.split('\n')
        id_arr = []
        name_arr = []
        for x in range(2, len(lines)-8):
            id = lines[x].split(' ')[0]
            id_arr.append(id)
            if len(id) == 1:
                name = lines[x].split(' ')[4]
            if len(id) == 2:
                name = lines[x].split(' ')[3]
            if len(id) == 3:
                name = lines[x].split(' ')[2]
            if len(id) == 4:
                name = lines[x].split(' ')[1]
            name_arr.append(name)
        if vlan_id in id_arr and vlan_name in name_arr:
            print(f"vlan {vlan_name} already exists")
            return "false"
        elif vlan_id in id_arr:
            print(f"vlan {vlan_id} already exists")
            return "id"
        elif vlan_name in name_arr:
            print(f"Name {vlan_name} already exists")
            return "name"
        else:
            return "true"


# Aruba calls
@app.route('/aruba/api/v1.0/vlan', methods=['POST'])
# @auth.login_required
def aruba_add_vlan():
    req_data = request.get_json(force=True)
    vlan_id = req_data['vlan_id']
    vlan_name = req_data['vlan_name']
    aruba_conf = ['conf t', f'vlan {vlan_id}', f'name {vlan_name}', 'tagged 1-49', 'write memory']
    connect(aruba_up_host, aruba_username, aruba_password, aruba_conf)
    connect(aruba_down_host, aruba_username, aruba_password, aruba_conf)
    text = {"vlan_id": f"{vlan_id}", "vlan_name": f"{vlan_name}"}
    return jsonify(text)

# Fortigate calls
@app.route('/forti/api/v1.0/vlan', methods=['POST'])
# @auth.login_required
def forti_add_vlan():
    req_data = request.get_json(force=True)
    vlan_id = req_data['vlan_id']
    vlan_name = req_data['vlan_name']
    gateway = req_data['gateway']
    mask = req_data['mask']
    forti_conf = ['config system interface', f'edit {vlan_name}', f'set ip {gateway} {mask}',
                          'set interface "dmz"', f'set vlanid {vlan_id}', 'set vdom "root"',
                          'set allowaccess ping',
                          'next', 'end',
                          'config system zone', 'edit DMZ', f'append interface {vlan_name}', 'next', 'end']
    connect(forti_host, forti_username, forti_password, forti_conf)
    text = {"vlan_id": f"{vlan_id}", "vlan_name": f"{vlan_name}"}
    return jsonify(text)

# Slack calls
@app.route('/slack/api/v1.0/message', methods=['POST'])
def send_slack_message():
    req_data = request.get_json(force=True)
    vlan_id = req_data['vlan_id']
    vlan_name = req_data['vlan_name']
    username = req_data['username']
    requests.packages.urllib3.disable_warnings()  # Ignore from requests module
    url = "https://hooks.slack.com/services/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"
    payload = {"text": f"Hey {username}, VLAN {vlan_name} with ID {vlan_id} add to TS LAB"}
    headers = {'Content-Type': "application/json"}
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)
    return str(payload)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
