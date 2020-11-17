import sys
import os
import time
from time import sleep
import requests
import urllib3

cert = False

def IpListGet(url_link_final, tenant1key):
    t1iplistall = []
    t1iplistname = []
    t1iplistid = []
    print("Getting All IP List...")
    payload  = {}
    url = url_link_final + 'api/iplists'
    headers = {
        "api-secret-key": tenant1key,
        "api-version": "v1",
        "Content-Type": "application/json",
    }
    response = requests.request("GET", url, headers=headers, data=payload, verify=cert)
    describe = str(response.text)
    describe2 = str(response.text)
    index = describe.find('\"ipLists\"')
    if index != -1:
        indexpart = describe[index+11:]
        startIndex = 0
        while startIndex != -1: 
            startIndex = indexpart.find('{')
            if startIndex != -1: #i.e. if the first quote was found
                endIndex = indexpart.find('}', startIndex + 1)
                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                    indexid = indexpart[startIndex:endIndex+1]
                    t1iplistall.append(str(indexid))
                    indexpart = indexpart[endIndex:]
    index = describe.find('\"ipLists\"')
    while index != -1:
            index = describe2.find('\"name\"')
            if index != -1:
                indexpart = describe2[index+6:]
                startIndex = indexpart.find('\"')
                if startIndex != -1: #i.e. if the first quote was found
                    endIndex = indexpart.find(',', startIndex + 1)
                    if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                        indexid = indexpart[startIndex+1:endIndex-1]
                        t1iplistname.append(str(indexid))
                        describe2 = indexpart[endIndex:]
                        index = describe2.find('\"ID\"')
                        if index != -1:
                            indexpart = describe2[index+3:]
                            startIndex = indexpart.find(':')
                            if startIndex != -1: #i.e. if the first quote was found
                                endIndex = indexpart.find('}', startIndex + 1)
                                if startIndex != -1 and endIndex != -1: #i.e. both quotes were found
                                    indexid = indexpart[startIndex+1:endIndex]
                                    t1iplistid.append(str(indexid))
                                    print(indexid)
                                    describe2 = indexpart[endIndex:]
    #print("All IP List ID...")
    #print(t1iplistid)
    print("Done!")
    return t1iplistall, t1iplistname, t1iplistid

def IpListCreate(t1iplistall, t1iplistname, url_link_final_2, tenant2key):
    t2iplistid = []
    print("Transfering All IP List...")
    for count, dirlist in enumerate(t1iplistname):
        payload = "{\"searchCriteria\": [{\"fieldName\": \"name\",\"stringValue\": \"" + dirlist + "\"}]}"
        url = url_link_final_2 + 'api/iplists/search'
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
                        payload = t1iplistall[count]
                        url = url_link_final_2 + 'api/iplists/' + str(indexid)
                        headers = {
                        "api-secret-key": tenant2key,
                        "api-version": "v1",
                        "Content-Type": "application/json",
                        }
                        response = requests.request("POST", url, headers=headers, data=payload, verify=cert)
                        t2iplistid.append(str(indexid))
                        print(indexid)
        else:
            payload = t1iplistall[count]
            url = url_link_final_2 + 'api/iplists'
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
                        t2iplistid.append(str(indexid))
                        print(indexid)
    #print("Finished Transfering All IP List.")
    #print(t2iplistid)
    print("Done!")
    return t2iplistid