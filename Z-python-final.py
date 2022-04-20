import datetime, requests, schedule, time, json, csv, os


# Login Details
rawurl = 'https://subdomain.zendesk.com/api/v2/incremental/tickets?start_time='
rawurl2 = 'https://subdomain.zendesk.com/api/v2/incremental/users?start_time='
API_USER = "" + '/token'
TOKEN_KEY = "*****"

#Analysis data
day_secs = 60*60*24
month_seconds = day_secs*30
ValueList = [
    "id",
    "created_at",
    "requester_id",
    "updated_at"    
    ]
ValueList2 = [
    "id",
    "name",
    "updated_at"   
    ]

###################################### AUTH AND EXTRACT PROCESS
def AuthAndGetData():
    onemonthago = int(datetime.datetime.now().timestamp() - month_seconds)
    url = rawurl + str(onemonthago)
    print(url)
    # Do the HTTP get request
    response = requests.get(url, auth=(API_USER,TOKEN_KEY))
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    newrow = ValueList
    # Create a new file in .csv
    with open(str(datetime.datetime.now().date())+".csv", 'w', newline='') as csvw:
        writer = csv.writer(csvw)
        writer.writerow(newrow)
        newrow=[]
        # Loop JSON => CSV
        for i in data['tickets']:
            newrow=[]
            for k in ValueList:
                newrow.append(i[k])
            writer.writerow(newrow)


def AuthAndGetDataUser():
    onemonthago = int(datetime.datetime.now().timestamp() - month_seconds)
    url2 = rawurl2 + str(onemonthago)
    print(url2)
    # Do the HTTP get request
    response = requests.get(url2, auth=(API_USER,TOKEN_KEY))
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    newrow = ValueList2
    with open(str(datetime.datetime.now().date())+"_Users.csv", 'w', newline='') as csvw:
        writer = csv.writer(csvw)
        writer.writerow(newrow)
        newrow=[]
        for i in data['users']:
            newrow=[]
            for k in ValueList2:
                newrow.append(i[k])
            writer.writerow(newrow)
            



#INPUT YES OR NO
def startornotstart():
    YorN = input("Extract? Y or N \n")
    if YorN.upper()== "Y":
        AuthAndGetData()
        AuthAndGetDataUser()
        while True:
            print("next run is: " + str(int(schedule.idle_seconds())))
            schedule.run_pending()
            time.sleep(1)
    elif YorN.upper() == "N":
        print("Nothing done")
    else:
        print("incorrect input")


# Schedule both jobs
schedule.every(30).days.do(AuthAndGetData)
schedule.every(30).days.do(AuthAndGetDataUser)
startornotstart()



#if today time - previous time > x then start api call to save calls





