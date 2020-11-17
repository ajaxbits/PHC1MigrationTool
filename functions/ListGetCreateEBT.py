import sys
import os
import time
from time import sleep
import requests
import urllib3

cert = False

def ListEventTask(url_link_final, tenant1key):
    payload = {}
    url = url_link_final + 'api/eventbasedtasks'
    headers = {
    "api-secret-key": tenant1key,
    "api-version": "v1",
    "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    index = 0
    oldetname = []
    oldetid = []
    while index != -1:
        index = describe.find('\"name\"')
        if index != -1:
            indexpart = describe[index+6:]
            startIndex = indexpart.find('\"')
            if startIndex != -1: 
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: 
                    indexid = indexpart[startIndex+1:endIndex-1]
                    oldetname.append(str(indexid))
        index = describe.find('\"ID\"')
        if index != -1:
            indexpart = describe[index+4:]
            startIndex = indexpart.find(':')
            if startIndex != -1: 
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: 
                    indexid = indexpart[startIndex+1:endIndex]
                    oldetid.append(str(indexid))
                    describe = indexpart[endIndex:]
                else:
                    endIndex = indexpart.find('}', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: 
                        indexid = indexpart[startIndex+1:endIndex]
                        oldetid.append(str(indexid))
                        describe = indexpart[endIndex:]
        
                    
    return enumerate(oldetname), oldetid
def GetEventTask(etIDs, url_link_final, tenant1key):
    allet = []
    nameet = []
    print ('Getting Target Task...')
    for part in etIDs:
        payload = {}
        url = url_link_final + 'api/eventbasedtasks/' + str(part)
        headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
        }
        response = requests.request("GET", url, headers=headers, data=payload, verify=cert)

        describe = str(response.text)
        allet.append(describe)
        index = describe.find('\"name\"')
        if index != -1:
            indexpart = describe[index+6:]
            startIndex = indexpart.find('\"')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find(',', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex+1:endIndex-1]
                    nameet.append(str(indexid))
                    describe = indexpart[endIndex:]
    print(allet)
    print(nameet)
    return allet, nameet

def CreateEventTask(allet, nameet, url_link_final_2, tenant2key):
    print ('Creating Task to target Account...')
    for count, dirlist in enumerate(nameet):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/eventbasedtasks/search'
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
                        payload = allet[count]
                        url = url_link_final_2 + 'api/eventbasedtasks/' + str(indexid)
                        headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                        }
                        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
        else:
            payload = allet[count]
            url = url_link_final_2 + 'api/eventbasedtasks'
            headers = {
            "api-secret-key": tenant2key,
            "api-version": "v1",
            "Content-Type": "application/json",
            }
            response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
            
        print(str(response.text))