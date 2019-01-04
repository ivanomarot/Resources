#!/bin/env python
# ---------------------------------------------------------------------------------------------------
#
# hwx_rest_api.examples.py
#
# This script contains some examples of API calls to Ambari, Oozie and NiFi.
#
# ---------------------------------------------------------------------------------------------------
import requests
import os
import time
import json

# To be removed eventually (because of NiFi json call)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ambari APIs
# https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/index.md

# NiFi APIs
# https://nifi.apache.org/docs/nifi-docs/rest-api/

# Oozie APIs
# https://oozie.apache.org/docs/4.1.0/WebServicesAPI.html

# Global variables for user and password
user = os.environ["USER"]
pwd = os.environ["USING"]

# Global variables for servers
ambari_host = "https://my-master001:8443"
nifi_host = "https://my-nifi001:9091"
oozie_host = "https://my-master001:11443"

# Oozie user
oozie_user = "my-oozie-admin"

# Point to PEM file
DEFAULT_CA_BUNDLE = os.path.join(os.path.abspath(os.path.dirname(__file__)),'MY.bundle.pem')


# Function to get JSON from URL
def get_json(url, token=None):
    session = requests.Session()
    session.auth = (user, pwd)
    if token is not None:
        session.headers['Accept'] = "*/*"
        session.headers['Authorization'] = "Bearer " + token
        session.headers['Connection'] = "keep-alive"
        session.headers['X-Requested-With'] = "XMLHttpRequest"
    session.verify = DEFAULT_CA_BUNDLE
    r = session.get(url)
    assert r.status_code == 200, "(GET) HTTP Error: " + str(r.status_code)
    return r.json()


# Function to get JSON from NiFi URL
def get_nifi_json(url, token, json_data=None, method="GET"):
    if json_data is None:
        r = requests.request(method, url, headers={'Authorization': 'Bearer ' + token}, verify=False)
    else:
        r = requests.request(method, url, headers={'Content-Type': 'application/json',
                                                   'Authorization': 'Bearer ' + token,
                                                   'Accept': '*/*'}, json=json_data, verify=False)
    assert r.status_code in (200, 201), "(" + method + ") HTTP Error: " + str(r.status_code)
    return r.json()


# Function to get the token for NiFi
def get_nifi_token():

    newtoken = requests.request('POST', nifi_host + '/nifi-api/access/token',
                                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                data={'username': user, 'password': pwd}, verify=False)
    assert newtoken.status_code == 201, "(POST) HTTP Error: " + str(newtoken.status_code)
    return newtoken.text


# Function to display the ambari alert history
def display_ambari_alert_history():

    # Get each cluster from Ambari
    json_data = get_json(ambari_host + '/api/v1/clusters')

    # Loop for each cluster
    for item in json_data["items"]:
        cluster_name = str(item["Clusters"]["cluster_name"])

        # Perform the API call
        json_data2 = get_json(ambari_host + '/api/v1/clusters/' + cluster_name + '/alert_history?fields=*')

        # Loop for all alerts
        for item2 in json_data2["items"]:
            print("cluster_name   : " + str(item2["AlertHistory"]["cluster_name"]))
            print("component_name : " + str(item2["AlertHistory"]["component_name"]))
            print("definition_id  : " + str(item2["AlertHistory"]["definition_id"]))
            print("definition_name: " + str(item2["AlertHistory"]["definition_name"]))
            print("host_name      : " + str(item2["AlertHistory"]["host_name"]))
            print("id             : " + str(item2["AlertHistory"]["id"]))
            print("instance       : " + str(item2["AlertHistory"]["instance"]))
            print("label          : " + str(item2["AlertHistory"]["label"]))
            print("service_name   : " + str(item2["AlertHistory"]["service_name"]))
            print("state          : " + str(item2["AlertHistory"]["state"]))
            print("text           : " + str(item2["AlertHistory"]["text"]))
            print("timestamp      : " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(item2["AlertHistory"]["timestamp"]/1000)))
            print("")

    return


# Function to display the Ambari components per host
def display_ambari_host_components():

    # Get each cluster from Ambari
    json_data = get_json(ambari_host + '/api/v1/clusters')

    # Loop for each cluster
    for item in json_data["items"]:
        cluster_name = str(item["Clusters"]["cluster_name"])

        # Get each host per cluster from Ambari
        json_data2 = get_json(ambari_host + '/api/v1/clusters/' + cluster_name + "/hosts")

        # Loop for each host
        for item2 in json_data2["items"]:
            host_name = str(item2["Hosts"]["host_name"])

            # Get each component per host
            json_data3 = get_json(ambari_host + '/api/v1/clusters/' + cluster_name + "/hosts/" + host_name +
                                  "/host_components?fields=HostRoles/service_name,HostRoles/component_name,"
                                  "HostRoles/display_name")

            # Loop for each component
            for item3 in json_data3["items"]:
                service_name = str(item3["HostRoles"]["service_name"])
                component_name = str(item3["HostRoles"]["component_name"])
                display_name = str(item3["HostRoles"]["display_name"])

                print("cluster_name  : " + cluster_name)
                print("host_name     : " + host_name)
                print("service_name  : " + service_name)
                print("component_name: " + component_name)
                print("display_name  : " + display_name)
                print("")

    return


# Function to display the metrics for NiFi connections
def display_nifi_connections(process_group):

    # Get NiFi Token
    token = get_nifi_token()

    # Get JSON from NiFi API
    json_data = get_nifi_json(nifi_host + '/nifi-api/flow/process-groups/' + process_group, token=token)

    # Loop for each connections
    for item in json_data['processGroupFlow']['flow']["connections"]:
        print("Process group: " + process_group)
        print("Connection ID: " + item['id'])
        print("Source name:   " + item['status']['sourceName'])
        print("Dest. name:    " + item['status']['destinationName'])
        try:
            print("Pct use count: " + str(item['status']['aggregateSnapshot']['percentUseCount']))
        except KeyError:
            print("Pct use count: Not defined")
        try:
            print("Pct use bytes: " + str(item['status']['aggregateSnapshot']['percentUseBytes']))
        except KeyError:
            print("Pct use bytes: Not defined")
        print("")

    for new_process_group in json_data['processGroupFlow']['flow']["processGroups"]:
        display_nifi_connections(new_process_group["id"])

    return


# Function to display the metrics for NiFi connections
def display_nifi_controllers(process_group):

    # Get NiFi Token
    token = get_nifi_token()

    # Get JSON from NiFi API
    json_data = get_nifi_json(nifi_host + '/nifi-api/flow/process-groups/' + process_group, token=token)
    json_data2 = get_nifi_json(nifi_host + '/nifi-api/flow/process-groups/' + process_group + '/controller-services',
                               token=token)

    for i in json_data2['controllerServices']:
        if i["component"]["type"] == 'org.apache.nifi.dbcp.hive.HiveConnectionPool' and i["component"]["properties"]["Validation-query"] is None:
            print('{:10} {:10}    {:40}'.format("Hive ", process_group, i["component"]["name"]))
        elif 'hbase' in i["component"]["type"] and i["component"]["properties"]["HBase Client Retries"] != "30":
            print('{:10} {:10}    {:40} {}'.format("HBase", process_group, i["component"]["name"],
                                                   str(i["component"]["properties"]["HBase Client Retries"])))

    for new_process_group in json_data['processGroupFlow']['flow']["processGroups"]:
        display_nifi_controllers(new_process_group["id"])

    return


# Function to display the metrics for NiFi processors
def display_nifi_processors(process_group):

    # Get NiFi Token
    token = get_nifi_token()

    # Get JSON from NiFi API
    json_data = get_nifi_json(nifi_host + '/nifi-api/process-groups/' + process_group + '/processors', token=token)

    column_format = '{:<70}   {:<20}   {:<10}   {:<36}'
    print(column_format.format('Name', 'Type', 'Node', 'ID'))
    print(column_format.format('-' * 70, '-' * 20, '-' * 10, '-' * 36))

    for processor in json_data["processors"]:
        print(column_format.format(processor["status"]["name"], processor["status"]["aggregateSnapshot"]["runStatus"],
                                   processor["component"]["config"]["executionNode"], processor["id"]))

    print("")

    json_data = get_nifi_json(nifi_host + '/nifi-api/flow/process-groups/' + process_group, token=token)
    for new_process_group in json_data['processGroupFlow']['flow']["processGroups"]:
        display_nifi_processors(new_process_group["id"])

    return


# Function to display the metrics for one NiFi processor
def display_nifi_one_processor(process_id):

    # Get NiFi Token
    token = get_nifi_token()

    # Get JSON from NiFi API
    json_data = get_nifi_json(nifi_host + '/nifi-api/processors/' + process_id, token=token)

    print(json.dumps(json_data))

    print("")

    return


# Function to stop NiFi processors
def stop_nifi_processors(processor_list):

    # Get NiFi Token
    token = get_nifi_token()

    for processor_id in processor_list:

        json_data = get_nifi_json(nifi_host + '/nifi-api/processors/' + processor_id, token=token)
        if json_data["component"]["state"] == "STOPPED":
            print("{:100}: {}".format("Processor ID " + processor_id + " (" + json_data["component"]["name"] + ")",
                                     "Already stopped"))
        else:
            try:
                # This changes the state of the processor to stop it
                modified_processor = {
                    'revision': {
                        'version': json_data["revision"]["version"],
                        'clientId': json_data["revision"]["clientId"]
                    },
                    'status': {
                        "aggregateSnapshot": {
                            "runStatus": "STOPPED"
                        }
                    },
                    'component': {
                        'id': json_data['id'],
                        'state': "STOPPED"
                    },
                    'id': json_data['id']
                }

                print("{:100}: {}".format("Processor ID " + processor_id + " (" + json_data["component"]["name"] + ")",
                                         "Stopping now"))
                # Perform the stop action
                get_nifi_json(nifi_host + '/nifi-api/processors/' + processor_id, token=token,
                              json_data=modified_processor, method="PUT")
            except:
                print("{:100}: {}".format("Processor ID " + processor_id + " (" + json_data["component"]["name"] + ")",
                                         "Error while stopping"))

    return


# Function to display the 'view state' content of a processor
def display_nifi_processor_state(processor_id):

    # Get NiFi Token
    token = get_nifi_token()

    # Get JSON from NiFi API
    try:
        json_data = get_nifi_json(nifi_host + '/nifi-api/processors/' + processor_id + '/state', token=token)

        # Loop for each state
        for state in json_data["componentState"]["clusterState"]["state"]:
            print("Key       : " + state["key"])
            print("Value     : " + state["value"])
            try:
                print("Value (ts): " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(state["value"]))))
            except TypeError:
                print("Value (ts): n/a")

    except AssertionError:
        print("Processor " + processor_id + " doesn't exist or is stateless.")

    return


# Function to display the Data Provenance for a given processor
def display_nifi_data_provenance(processor_id):

    # Get NiFi Token
    token = get_nifi_token()

    json_data = {"provenance": {"request": {"maxResults": 1000, "searchTerms": {"ProcessorID": processor_id}}}}

    # Submit the query to get the data provenance
    json_data = get_nifi_json(nifi_host + '/nifi-api/provenance', token=token, method="POST", json_data=json_data)
    id = json_data["provenance"]["id"]

    # Loop until the query is running in the backend
    boucle = True
    while boucle:
        # Retrieve the result from the query
        json_data = get_nifi_json(nifi_host + '/nifi-api/provenance/' + id, token=token)
        boucle = not json_data["provenance"]["finished"]

    # Loop for each data provenance events
    for event in json_data["provenance"]["results"]["provenanceEvents"]:
        componentName = event["componentName"]
        componentType = event["componentType"]
        eventTime = event["eventTime"]
        eventType = event["eventType"]
        print("componentName: " + componentName)
        print("componentType: " + componentType)
        print("eventTime    : " + eventTime)
        print("eventType    : " + eventType)

    # Delete the query
    get_nifi_json(nifi_host + '/nifi-api/provenance/' + id, token=token, method="DELETE")

    return


# Function to display the state of all Oozie jobs
def display_oozie_jobs():

    # Count the number of latest action with status != SUCCEEDED
    nb_latest_action_not_succeeded = 0

    # Count the coordinator jobs not running
    nb_coord_not_running = 0

    # Get the list of jobs
    json_data = get_json(oozie_host + '/oozie/v2/jobs?jobtype=coordinator&filter=user%3D' + oozie_user +
                         '&len=500&timezone=GMT')

    # Last running coordinator
    coordinator_list = list()

    # Loop for each coordinators
    for item in json_data["coordinatorjobs"]:
        if item["status"] == "RUNNING":
            # Remove the coordJobName if it's already found
            coordinator_list = [i for i in coordinator_list if i["coordJobName"] != item["coordJobName"]]
            # Add the item to the list
            coordinator_list.append(item)
        else:
            # Add of the list only if it's not there
            if not any(i["coordJobName"] == item["coordJobName"] for i in coordinator_list):
                coordinator_list.append(item)

    # Loop for all distinct coordinators
    for item in coordinator_list:
        coordJobName = item["coordJobName"]
        coordJobId = item["coordJobId"]
        status = item["status"]
        if status != "RUNNING":
            nb_coord_not_running += 1

        # Print header
        print("")
        print(coordJobName + " (" + status + ")")
        column_format = '{:<40}   {:<9}   {:<29}   {:<29}   {:<29}   {:<10}   {:<13}'
        print(column_format.format('-' * 40, '-' * 9, '-' * 29, '-' * 29, '-' * 29, '-' * 10, '-' * 13))
        print(column_format.format('Action ID', 'Status', 'Created Time', 'Nominal Time', 'Last Modified Time',
                                   'Error Code', 'Error Message'))
        print(column_format.format('-' * 40, '-' * 9, '-' * 29, '-' * 29, '-' * 29, '-' * 10, '-' * 13))

        # Retrieve the workflow jobs for that coordinator
        json_data = get_json(oozie_host + '/oozie/v2/job/' + coordJobId + '?len=5&timezone=GMT&order=desc')

        # Loop for all actions
        first_action = True
        for action in json_data["actions"]:
            id = action["id"]
            status = action["status"]
            createdTime = action["createdTime"]
            nominalTime = action["nominalTime"]
            lastModifiedTime = action["lastModifiedTime"]
            errorCode = action["errorCode"]
            errorMessage = action["errorMessage"]

            if first_action and status != "SUCCEEDED":
                nb_latest_action_not_succeeded += 1
            first_action = False

            print(column_format.format(id, status, createdTime, nominalTime, lastModifiedTime, str(errorCode),
                                       str(errorMessage)))

        # Print footer
        print(column_format.format('-' * 40, '-' * 9, '-' * 29, '-' * 29, '-' * 29, '-' * 10, '-' * 13))

    # Display a summary
    print("")
    print("Summary")
    print("------------------------------------------------------------------------------------")
    if nb_coord_not_running != 0:
        print("WARNING: " + str(nb_coord_not_running) + " coordinator job(s) is not running (total of " +
              str(len(coordinator_list)) + " coordinator jobs), please investigate.")
    else:
        print("SUCCESS: All " + str(len(coordinator_list)) + " coordinator jobs are running.")
    if nb_latest_action_not_succeeded != 0:
        print("WARNING: " + str(nb_latest_action_not_succeeded) +
              " latest action(s) did not complete with a status of SUCCEEDED, please investigate.")
    else:
        print("SUCCESS: All latest actions have run successfully.")
    print("------------------------------------------------------------------------------------")

    return


# Main procedure
if __name__ == "__main__":

    # display_ambari_alert_history()
    # display_ambari_host_components()
    # display_nifi_connections('root')
    display_nifi_processors('e06c3a43-f331-3030-b112-271b9870166c')
    # display_nifi_one_processor('a1add65c-8466-3884-9c57-f80fe6cc3f12')
    # display_nifi_processor_state("22d332a1-057b-13b2-9997-b16f42a36c3c")
    # display_oozie_jobs()
    # display_nifi_data_provenance('1bca35a3-dc4d-1d33-95bd-49abcbdcbd35')
    # display_nifi_controllers('root')
    proc_list = ['9c37671e-cb70-39bf-ae10-14245caec181', 'adfe0c1e-c03f-3aec-8c5a-c6a0eed336ae',
                  'cecf5692-e1c5-3f67-8e6f-f5a354c78f38', 'ea94cf3c-a5e2-3a9f-abc3-35e7b19db359',
                  'ea94cf3c-a5e2-3a9f-abda-a9c833eff1b8', 'e0328e7e-d449-344b-830f-05907dd8b0cf',
                  'ea0b8256-ad6b-362e-af27-f202abebb93d', '27d73750-b793-1753-8c6b-ea7083161a21',
                  '63fb341e-cd16-1f41-84d0-453c57ce9b84', '78ce3423-5658-15e1-87d6-89cac85aa045',
                  'ad803cec-8e77-1527-87bd-bd51e7254f6d', 'c5a53157-b955-1172-87ad-5a17c0d96c9d',
                  'd6be3eea-12c1-1957-b1c2-d28bc643a65d', 'dbcf3637-6a77-196e-91db-b14c7e7eea67',
                  '0cd909a4-2a5b-3e08-8a1a-1ec85b1e43bf', '2406e641-e877-373c-b6db-dbfb0125b4ff',
                  '5a047f56-4f62-35ad-a187-3bf6b0417ddc', '789b38a7-8295-1f92-a79b-3232e6fa9e89',
                  '13ed704c-4977-321d-bab4-b1377d76f68c', '40918b78-2c17-3c25-91c4-a50a9f608c6b',
                  '54904337-511e-351d-9001-8aeb186e35f2', '875f7a4b-7034-33b2-bcaf-29f57cec58ee',
                  '92499a6d-574e-3bfa-9ce9-ff10dce9823f', 'a3f79cc3-89a1-3f3e-8464-27d8f4c8aadd',
                  'fb5b9471-234f-3ffc-8444-8fd7d02e91fb', '13a32e41-0296-385d-bd4c-73d2634f0173',
                  '326a30ba-df1a-1910-a8d2-ea64a8289a48', 'ac813176-4ca3-1fa5-ac7e-160f6d4e42fa',
                  'cebd1575-4b39-355b-9842-1b2f1d9823f2', 'dd7634ee-fcb0-14ed-8582-6700eed61a5a',
                  'e095a0e9-f7b0-30cd-a511-a46a91151822', 'f60332c0-38e9-1e90-8c25-9105dd02c946',
                  'fb263490-ad15-116f-9cc7-38f48fcf16a2']
    # stop_nifi_processors(proc_list)

    exit(0)
