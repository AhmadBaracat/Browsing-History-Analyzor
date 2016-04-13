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
    con = lite.connect('History.db')
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM history_visits ")
        rows = cur.fetchall()

        l = []

        #fill the list with domain and timeOpened
        for row in rows:
            #add 978307200 because the time here is the number of
            #seconds since 00:00:00 UTC on 1 January 2001.
            timeOpened = row[2] + 978307200

            #get the domain from the history_items table
            cur.execute("SELECT * FROM history_items WHERE Id=" + str(row[0]))
            rows2 = cur.fetchall()

            #initialize the domain so that websites with no domain names extracted
            #are all grouped together
            domain = "domain"

            for row2 in rows2:
                domain = row2[2]

            if domain != None:
                l.append((domain,timeOpened))


        #sort the list
        l.sort(key=lambda tup: tup[1])

        timeSpentDic = {}
        #subtract each subsequent website visits to get the total time spent on
        #the website for a maximum of 5 mins per website
        #add the list elements to dictionary and add the total time spent
        for i in range(1, len(l)):
            currentElemnt = l[i-1]
            nextElement = l[i]

            key = currentElemnt[0]
            startTime = currentElemnt[1]
            endTime = nextElement[1]

            timeDiff = endTime - startTime
            if key in avgTimePerDomain:
                timeSpent = min(avgTimePerDomain[key], datetime.timedelta(seconds =timeDiff).total_seconds())
            else:
                timeSpent = min(5*60, datetime.timedelta(seconds =timeDiff).total_seconds())

            '''
            if key == "joelcalifa":
                print(startTime)
                print(endTime)
                print(timeDiff)
                print(timeSpent)
                print(currentElemnt[0])
                print(nextElement[0])
            '''

            if key in timeSpentDic:
                timeSpentDic[key] += timeSpent
            else:
                timeSpentDic[key] = timeSpent



        #sort the dictionary
        sortedTimeSpentDic = sorted(timeSpentDic.items(), key=operator.itemgetter(1),reverse=True)

        #display it
        for e in sortedTimeSpentDic:
            if e[1]/3600 > 1:
                print e[0] + " " + str(e[1]/3600)

def getWebsitesByNumberOfHits():
    con = lite.connect('History.db')
    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM history_items")
        rows = cur.fetchall()
        d = {}
        for row in rows:
            if str(row[2]) in d:
                d[str(row[2])] += row[3]
            else:
                d[str(row[2])] = row[3]


            #print "id: {0}".format(row[0])
            #print "title: {0}".format(row[3])
            #print "\n"
            '''
            cur.execute("SELECT * FROM history_items WHERE Id=" + str(row[0]))
            rows2 = cur.fetchall()
            for row2 in rows2:
                print "url: {0}".format(row2[1])
                print "visit_count: {0}".format(row2[3])
                print "daily_visit_count: {0}".format(row2[4])
                print "weekly_visit_count: {0}".format(row2[5])
            '''
        sorted_x = sorted(d.items(), key=operator.itemgetter(1),reverse=True)

        for e in sorted_x:
            print e

main()
