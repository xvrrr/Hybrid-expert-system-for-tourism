'''from BeautifulSoup import BeautifulSoup'''
from bs4 import BeautifulSoup  
import logging
from difflib import *
import zipfile, io, re, csv, sys
import requests

output_string =''
def select():

    print("\nWelcome to our Expert System!")
    print("\t1. List the countries.")
    print("\t2. Search about the geographic details of any country. (KNOWLEDGE BASED SYSTEM)")
    print("\t3. Seek recommendations from our Expert system on living, working, or traveling in various countries. (RULE BASED EXPERT SYSTEM)\n\t4. Exit\n")

    choice = input()
    recordchoice = choice

    if choice == '1':
        list_country()
    elif choice == '2':
        main()
    elif choice == '3':
        expertSystem()

    elif choice == '4':
        exit()
    else:
        print("Invalid Input! Please try again")


def list_country():
    file = open("countryList.txt", "r")
    count = 0
    print("The countries you can search about are: ")
    for line in file:
        con = line[3:]
        count += 1
        print(str(count) + '.', con.upper(),)
    select()

def main():
    while True:
        country = input("Enter a Country:\n(Type 'BACK' to go back to menu or 'EXIT' to exit)\n").lower()
        if country=='back':
            select()
            break

        if country=='exit':
            exit()

        country = country[0].upper() + country[1:].lower()
        for i in range(len(country)-3):
            if country[i] == " ":
                country = country[:i + 1] + country[i + 1].upper() + country[(i + 2):]



        try:
            file = open("countryList.txt", "r")
            for line in file:
                if country in line:
                    page = line[:2] + ".html" #finds name of the country's file
                    break
            print(page)
        except UnboundLocalError:
            print('Invalid Input! Please try again')
            exit()

        keyWord = getQuery() #raw_input("What would you like to know?")


        countrySearch(country, keyWord)

def getQuery():
    userInput = input("What would you like to know?  \n(eg. location, area, climate, population, nationality, ethnic group, languages, birth rate, death rate, economy, industries, etc)\n").lower()

    wordsToRemove = ["how", "what", "the", "a", "an", "which", "of", "in", ",", ":", ".", "?", "is"]

    words = []
    for word in userInput.split():
        if word not in wordsToRemove:
            words.append(word)

    userInput = " ".join(words)

    #print userInput

    return userInput

def countrySearch(country, key):

    try:
        file = open("countryList.txt", "r")
        for line in file:
            if country in line:
                page = line[:2] + ".html" #finds name of the country's file
                break
        #print page
    except UnboundLocalError:
        print('Invalid Input! Please try again')
        return

    archive = zipfile.ZipFile("countries.zip", "r") #access a zip archive
    file2 = archive.open(page, "r")


    possibilities = parseHtml(file2)


    if key == ";lst":
        for key in possibilities.keys():
            print(key + "," + possibilities[key])
        return


    if key == ";keys":
        for key in possibilities.keys():
            print(key)
        return
    
    results = get_close_matches(key, possibilities.keys())

    if key == ";matches":
        for result in results:
            print(result)
        return


    if len(results) == 0: 
        print("Sorry, there is no relevant information.")
    else:
      for result in results:
            print(result + ": ")
            print(possibilities[result])

def parseHtml(htmlFile):
  soup = BeautifulSoup(htmlFile)

  possibilities = dict()

  for attr in soup.findAll("div", "category"):
    aTag = attr.find("a")
    if aTag:
      trTag = attr.parent.parent.findNextSibling("tr")

      if len(trTag) > 1:
        contents = []
        for div in trTag.findAll("div", "category"):
          if len(div.contents) > 0:
            contents.append(div.contents[0].strip())
            for span in div.find("span"):
              contents.append(span.string.strip())

        for div in trTag.findAll("div", "category_data"):
          if div.string:
            contents.append(div.string)

        data = "\r\n".join(contents)
      elif trTag.find("td"):
        data = trTag.find("td").find("div", "category_data").string
        print(data)
      else:
        data = trTag.find("div", "category_data").string

      #alot of the titles contain extra info after a " - " which is throwing off the search
      title = formatKey(aTag.string)

      if title in possibilities:
        data = possibilities[title] + "\r\n" + data

      possibilities[title] = data

  return possibilities

def formatKey(key):
  words = key.split()

  temp = []
  for word in words:
    if word == "-":
      break
    else:
      temp.append(word)

  return " ".join(temp)

def liveSuggestion(countryDetails):
    l = []
    c = []

    print("What kind of Population Desnity do you prefer?\n1.High\n2.Low\n")
    b = int(input())

    if(b == 1):
        l.append("high")
    elif(b == 2):
        l.append("low")
    else:
        print("Invalid selection")
        exit()

    print("What kind of Climate do you prefer?\n1.Cold\n2.Moderate\n3.Hot\n")
    c = int(input())

    if(c == 1):
        l.append("cold")
    elif(c == 2):
        l.append("moderate")
    elif(c ==3):
        l.append("hot")
    else:
        print("Invalid selection")
        exit()

    print("What kind of Government do you prefer?\n1.Democracy\n2.Communist\n3.Monarchy\n4.Republic\n5.Federal")
    g = int(input())

    if(g == 1):
        l.append("democracy")
    elif(g == 2):
        l.append("communist")
    elif(g ==3):
        l.append("monarchy")
    elif(g == 4):
        l.append("republic")
    elif(g ==5):
        l.append("federal")
    else:
        print("Invalid selection")
        exit()

    print("What is your religion?\n1.Christianity\n2.Buddhism\n3.Hinduism\n4.Islam\n5.Atheist")
    r = int(input())

    if(r == 1):
        l.append("christianity")
    elif(r == 2):
        l.append("buddhism")
    elif(r ==3):
        l.append("hinduism")
    elif(r == 4):
        l.append("islam")
    elif(r ==5):
        l.append("atheist")
    else:
        print("Invalid selection")
        exit()

    possibleCountry = []
    for item in countryDetails:
        if countryDetails[item]["average weather"] == l[1] and countryDetails[item]["type of government"] == l[2] and countryDetails[item]["major religion"] == l[3]:
            possibleCountry.append(item)

    if possibleCountry != []:
        print("Your possible choices are: ")
        for item in possibleCountry:
            print(item.upper())
    else:
        print("The one you describe does not exist among the top 40 rich countries in the world.")

    output_string = f"I'm looking for a country to settle in, Population Density I prefer is {l[0]}, Climate I prefer is {l[1]}, Government I prefer is {l[2]}, My religion is {l[3]}, Recommend some cities for me."
    print(output_string)

def workSuggestion(countryDetails):
    global output_string
    x = int(input('What is your work preference?:\n1. Business\n2. Job\n'))
    wp = False; #Work preference F: Business T: Job
    ie = False; #F: Import  T: Export
    fdomain = 0;
    jobtype = 0;    # 1: Startup 2: Local business 3: MNC
    l = []

    p = ['Business']
    k = ['Job']
    if x == 1:



        wp = False;
        xa = int(input('Choose the type of trade:\n1.Imports\n2.Exports\n'))

        if xa == 1:
            l.append("import")
            p.append("import")


        elif xa == 2:
            l.append("export")
            p.append("export")


        else:
            print("Invalid selection")

        print("Your field:")
        fdomain = int(input('1. Technology\n2. Manufacturing\n3. Tourism\n4. Infrastructure\n'))
        if fdomain == 1:
            l.append("technology")
            p.append("technology")



        elif fdomain == 2:
            l.append("manufacturing")
            p.append("manufacturing")



        elif fdomain == 3:
            l.append("tourism")
            p.append("tourism")


        elif fdomain == 4:
            l.append("infrastructure")
            p.append("infrastructure")


        else:
            print("Invalid selection")
            exit()

        possibleCountry = []
        for item in countryDetails:
            # print l[0], l[1]
            if countryDetails[item]["trade type"] == l[0] and countryDetails[item]["field domain"] == l[1]:

                possibleCountry.append(item)

        if possibleCountry != []:
            print("Your possible choices are: ")
            for item in possibleCountry:
                print(item.upper())
        else:
            print("The one you describe does not exist among the top 40 rich countries in the world.")
        # break;
        output_string = f"I want to work in another countries, work preference is {p[0]}, type of trade is {p[1]}, field is {p[2]}, recommend some cities for me."
        print(output_string)


    elif x == 2:

        wp = True;
        print("Your field:")
        fdomain = int(input('1. Technology\n2. Manufacturing\n3. Tourism\n4. Infrastructure\n'))

        # jobtype = int(raw_input('What type of company would you work for 1: Startup,  2: Local businesses,  3: MNC'))
        if fdomain == 1:
            l.append("technology")
            k.append("technology")

        elif fdomain == 2:
            l.append("manufacturing")
            k.append("manufacturing")

        elif fdomain == 3:
            l.append("tourism")
            k.append("tourism")

        elif fdomain == 4:
            l.append("infrastructure")
            k.append("infrastructure")

        else:
            print("Wrong input")
            exit()

        possibleCountry = []
        for item in countryDetails:
            # print l[0], l[1]
            if countryDetails[item]["field domain"] == l[0]:

                possibleCountry.append(item)

        if possibleCountry != []:
            print("Your possible choices are: ")
            for item in possibleCountry:
                print(item.upper())
        else:
            print("The one you describe does not exist among the top 40 rich countries in the world.")
        output_string = f"I want to work in another countries, work preference is {k[0]}, field is {k[1]}, recommend some cities for me."
        print(output_string)

    else:
        print("Invalid selection")
        exit()




def tourismSuggestion():
    global output_string
    tourism = {}
    placeList = []
    f = open("Tourism.csv")
    try:
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].lower()
            placeList.append(row)
    finally:
        f.close()

    l = len(placeList)
    for i in range(1, l):
        tourism[placeList[i][0]] = {}

    for i in range(1, l):
        for j in range(len(placeList[0])):
            if placeList[0][j] != "" and placeList[i][j] != "":
                tourism[placeList[i][0]][placeList[0][j]] = placeList[i][j]

    l = []
    k = []

    print("What is your total budget (per person) ?\n1. Under 10000 HKD\n2. Between 10000 and 20000 HKD\n3. Above 20000 HKD\n")

    c = int(input())
    if(c == 1):
        l.append(0.5)
        k.append(5000)
    elif(c == 2):
        l.append(1.5)
        k.append(15000)
    elif(c ==3):
        l.append(2.5)
        k.append(25000)
    else:
        print("Invalid selection")
        exit()

    print("What type of view would you like to go?\n1. Historical Place\n2. Mountain scenery\n3. Desert scenery\n4. Seaside scenery\n")

    p = int(input())

    if(p == 1):
        l.append("Historical Place")
        k.append("Historical Place")
    elif(p == 2):
        l.append("Mountain scenery")
        k.append("Mountain scenery")
    elif(p ==3):
        l.append("Desert scenery")
        k.append("Desert scenery")
    elif(p == 4):
        l.append("Seaside scenery")
        k.append("Seaside scenery")
    else:
      print("Invalid selection")
      exit()

    # print l
    # possiblePlaces = []
    print("Suggested attractions you can visit are： ")
    for item in tourism:
        # print item, '-----'
        # if tourism[item]["population density"] == l[0] and
        # print type(tourism[item]["budget"]), type(l[0])#, tourism[item]["type of place"], l[1]

        if float(tourism[item]["budget"]) == l[0] and tourism[item]["type of place"] == l[1]:
            print(item.upper() + ",", tourism[item]["country"].upper())
    output_string = f"I want to travel to some countries, my total budget (per person) is {k[0]} HKD, view I would like to go is {k[1]}, recommend some cities for me."
    print(output_string)


def askQuestion(countryDetails):

    print("Which of the following questions would you like to ask?")
    print("\t1. I'm looking for a country to settle in, where is the best place for me?")
    print("\t2. I want to work in another country, where I can make the most profit?")
    print("\t3. I want to travel to some countries, can you give me some recommendations?")
    print("\t4. Go Back!\n")

    a = int(input())



    if(a == 1):
        liveSuggestion(countryDetails)

    elif(a == 2):
        workSuggestion(countryDetails)

    elif(a ==3):

        tourismSuggestion()

    elif(a==4):
        select()
        exit()

    else:
        print("Invalid selection")

def expertSystem():


    countryDetails = {}
    countryList = []
    f = open("countries.csv")
    try:
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].lower()
            countryList.append(row)
    finally:
        f.close()

    l = len(countryList)
    for i in range(1, l):
        countryDetails[countryList[i][0]] = {}

    for i in range(1, l):
        for j in range(len(countryList[0])):
            if countryList[0][j] != "" and countryList[i][j] != "":
                countryDetails[countryList[i][0]][countryList[0][j]] = countryList[i][j]

    askQuestion(countryDetails)






# Replace LLM API Key and Secret Key
import requests
import json

API_KEY = ""
SECRET_KEY = ""





def modeloutput():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": output_string
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    select()
    # Example usage
    token = get_access_token()
    print("LLM's answer:")
    modeloutput()
