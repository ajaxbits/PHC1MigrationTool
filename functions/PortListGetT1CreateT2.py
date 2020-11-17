import sys
import os
import time
from time import sleep
import requests
import urllib3

cert = False

def PortListGet(url_link_final, tenant1key):
    t1portlistall = []
    t1portlistname = []
    t1portlistid = []
    print("Getting All Port List...")
    payload  = {}
    url = url_link_final + 'api/portlists'
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    index = describe.find('\"portLists\"')
    if index != -1:
        indexpart = describe[index+10:]
        startIndex = 0
        while startIndex != -1: 
            startIndex = indexpart.find('{')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex:endIndex+1]
                    t1portlistall.append(str(indexid))
                    indexpart = indexpart[endIndex:]
    while index != -1:
            index = describe2.find('\"name\"')
            if index != -1:
                indexpart = describe2[index+6:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-1]
                        t1portlistname.append(str(indexid))
                        describe2 = indexpart[endIndex:]
                        index = describe2.find('\"ID\"')
                        if index != -1:
                            indexpart = describe2[index+3:]
                            startIndex = indexpart.find(':')
                            if startIndex != -1: #i.e. if the first quote was found
                                endIndex = indexpart.find('}', startIndex + 1)
                                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                    indexid = indexpart[startIndex+1:endIndex]
                                    t1portlistid.append(str(indexid))
                                    print(indexid)
                                    describe2 = indexpart[endIndex:]
    #print(t1portlistid)
    print("Done!")
    return t1portlistall, t1portlistname, t1portlistid

def PortListCreate(t1portlistall, t1portlistname, url_link_final_2, tenant2key):
    t2portlistid = []
    print("Transfering All Port List...")
    for count, dirlist in enumerate(t1portlistname):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/portlists/search'
        headers = {
        "api-secret-key": tenant2key,
        "api-version": "v1",
        "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
        describe = str(response.text)
        index = describe.find(dirlist)
        if index != -1:
            index = describe.find("\"ID\"")
            if index != -1:
                indexpart = describe[index+4:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        payload = t1portlistall[count]
                        url = url_link_final_2 + 'api/portlists/' + str(indexid)
                        headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                        }
                        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                        t2portlistid.append(str(indexid))
                        print(indexid)
        else:
            payload = t1portlistall[count]
            url = url_link_final_2 + 'api/portlists'
            headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
            describe = str(response.text)
            index = describe.find("\"ID\"")
            if index != -1:
                indexpart = describe[index+4:]
                startIndex = indexpart.find(':')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex]
                        t2portlistid.append(str(indexid))
                        print(indexid)
    #print("Finished Transfering All Port List.")
    #print(t2portlistid)
    print("Done!")
    return t2portlistid