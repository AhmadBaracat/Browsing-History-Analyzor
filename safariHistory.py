import sqlite3 as lite
import sys
import operator
import time
import datetime

avgTimePerDomain = {"google":20, "youtube":60*10}

def main():
    getWebsitesByTimeSpent()
    getWebsitesByNumberOfHits()

def getWebsitesByTimeSpent():
    #copy the History.db file from ~/Library/Safari/History.db to your current folder
    con = lite.connect('History.db')
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM history_visits")
        historyVisits = cur.fetchall()

        domainTimeOpenedList = []

        #fill the list with domain and timeOpened
        for historyVisit in historyVisits:
            #add 978307200 because the time here is the number of
            #seconds since 00:00:00 UTC on 1 January 2001.
            timeOpened = historyVisit[2] + 978307200

            #get the domain from the history_items table
            cur.execute("SELECT * FROM history_items WHERE Id=" + str(historyVisit[0]))
            historyItems = cur.fetchall()

            #initialize the domain so that websites with no domain names extracted
            #are all grouped together
            domain = "domain"

            for historyItem in historyItems:
                domain = historyItem[2]

            if domain != None:
                domainTimeOpenedList.append((domain,timeOpened))


        #sort the list
        domainTimeOpenedList.sort(key=lambda tup: tup[1])

        timeSpentDic = {}
        #subtract each subsequent website visits to get the total time spent on
        #the website for a maximum of 5 mins per website or the average time per domain
        #add the list elements to dictionary and add the total time spent
        for i in range(1, len(domainTimeOpenedList)):
            currentElemnt = domainTimeOpenedList[i-1]
            nextElement = domainTimeOpenedList[i]

            key = currentElemnt[0]
            startTime = currentElemnt[1]
            endTime = nextElement[1]

            timeDiff = endTime - startTime
            if key in avgTimePerDomain:
                timeSpent = min(avgTimePerDomain[key], datetime.timedelta(seconds =timeDiff).total_seconds())
            else:
                timeSpent = min(5*60, datetime.timedelta(seconds =timeDiff).total_seconds())

            if key in timeSpentDic:
                timeSpentDic[key] += timeSpent
            else:
                timeSpentDic[key] = timeSpent


        #sort the dictionary
        sortedTimeSpentDic = sorted(timeSpentDic.items(), key=operator.itemgetter(1),reverse=True)

        #display it
        for element in sortedTimeSpentDic:
            if element[1]/3600 > 1:
                print element[0] + " " + str(element[1]/3600)

def getWebsitesByNumberOfHits():
    con = lite.connect('History.db')
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM history_items")
        historyItems = cur.fetchall()

        numberOfHitsDic = {}

        #count the total number of hits for each domain
        for historyItem in historyItems:
            key = str(historyItem[2])
            if key in numberOfHitsDic:
                numberOfHitsDic[key] += historyItem[3]
            else:
                numberOfHitsDic[key] = historyItem[3]

        #sort the dictionary
        sortedNumberOfHitsDic = sorted(numberOfHitsDic.items(), key=operator.itemgetter(1),reverse=True)

        #display it
        for element in sortedNumberOfHitsDic:
            print element

main()
