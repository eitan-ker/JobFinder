import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl,sys
from sql2 import DataBase #sys is needed only if you are converting program to #software
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
from decimal import Decimal
SLEEP_TIME = 7200

def main():

    print("\nWelcome to the Linkedin Job Finder console.\n"
          "All you need to do is to write the Job Title and Country you want to look for, I'll do the rest.\n"
          "Job Finder will search for new jobs posted in every time period you specify.\n\n")
    firstSearch = True

    db = DataBase()
    db.tableExist()

    while(True):
        # just in case of a bad input
        if (firstSearch == True):

            print("Please write the Job Title you want to look for:")
            job_title = input('>> ')
            job_title = generateURLFormat(job_title)

            # job_title = 'junior%20developer'

            print("Please write the Location you want to look for:")
            location = input('>> ')
            location = generateURLFormat(location)

            # location = 'Israel'

        print()
        print("Searching for jobs...")
        print()
        url = 'https://www.linkedin.com/jobs/search?keywords=' + job_title + '&location=' + location + '&locationId=&geoId=&f_TPR=r86400&position=1&pageNum=0'
        # job page search
        try:
            html_text = urlopen(url, context=ctx).read()
            html_text = html_text.decode("utf-8")
        except Exception as e:
            print("get URL")
            print(e)
            time.sleep(SLEEP_TIME)
            exit(1)

        # find all jobs
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            jobs = soup.find_all('div',
                                 class_='base-card base-card--link base-search-card base-search-card--link job-search-card')
            if len(jobs) != 0:
                firstSearch = False
            else:
                print("No jobs were found.")
        except Exception as e:
            print("find_all")
            print(e)
            time.sleep(SLEEP_TIME)
            exit(1)


        try:
            # dbData list obj.
            dbData = db.readData()
            # if dbData is empty continue.
            # else map it by job_id and check for duplicats - append only new jobs.
            dbListById = []
            if dbData: 
                # list is not empty
                for job in dbData:
                    #  need only for keays
                    dbListById.append(cleanText(job[2]))
            



            for index, job in enumerate(jobs):
                job_details = []
                try:
                    job_id = job['data-entity-urn'].split(':')[3]

                    # if dbMapByID is not empty check if id already saved in map, if already saved - continue to next iteration.
                    if len(dbListById) != 0:
                        if job_id in dbListById:
                            continue

                    companyInfo = job.find('a', class_='hidden-nested-link')
                    company_name = companyInfo.text.replace('\n', '')
                    company_name = cleanText(company_name)
                    company_link = companyInfo['href']
                except Exception as e:
                    company_name = ""
                    company_link = ""
                try:
                    job_title = cleanText(job.find('span', class_='screen-reader-text').text)
                except:
                    job_title = ""
                try:
                    post_date = job.find('time', class_='job-search-card__listdate--new')['datetime']
                except Exception as e:
                    post_date = ""

                try:
                    job_link = job.a['href']
                except Exception as e:
                    job_link = ""

                try:
                    company_location = job.find('span', class_='job-search-card__location').text
                    company_location = cleanText(company_location)

                except Exception as e:
                    company_location = ""
 
                job_details.append(("job_title", job_title))
                job_details.append(("job_id", job_id))
                job_details.append(("company_name", company_name))
                job_details.append(("company_link", company_link))
                job_details.append(("job_post_date", post_date))
                job_details.append(("job_link", job_link))
                job_details.append(("company_location", company_location))

                db.insertData(job_details)


                


                #    
                # -------------- write to files --------------
                # 
                # try:
                #     file_name = job_title +"-"+ company_name+".txt"
                #     file  = open(file_name, "w+")
                #     for i in range(len(job_details)):
                #         file.write(job_details[i][0])
                #         file.write(": ")
                #         try:
                #             file.write(job_details[i][1])
                #         except Exception as e:
                #             firstBadIndex = e.args[2]
                #             file.write(job_details[i][1][0:firstBadIndex])
                #         file.write("\n")
                #     file.close()


                # except Exception as e:
                #     print(e)
                #     error = e.args
                
                # print(f'{index + 1}.')
                # print(f'job_title: {job_title}')
                # print(f'job_id: {job_id}')
                # print(f'company_name: {company_name}')
                # print(f'company_link: {company_link}') # to look for HR
                # print(f'post_date: {post_date}')
                # print(f'job_link: {job_link}')
                # print(f'company_location: {company_location}')
                # print()

        except Exception as e:
            print("parsing")
            print(e)
            time.sleep(SLEEP_TIME)
            exit(1)
        print(f'Going to sleep for 2 hours')
        db.closeConn()
        time.sleep(SLEEP_TIME)

def cleanText(unCleanedStr):
    firstIndex = 0
    lastIndex = 0
    strReadingFlag = False
    if (type(unCleanedStr) is str):
        splitStr = unCleanedStr.split(' ')
        for index, elem in enumerate(splitStr):
            if strReadingFlag == False:
                if elem != '' and elem != '\n':
                    firstIndex = index
                    lastIndex = index
                    strReadingFlag = True
            else:
                # last index ++ as long as i see  elem != ''
                if elem != '' and elem != '\n':
                    lastIndex = index
        cleanedstr = splitStr[firstIndex:lastIndex + 1]
        cleanedstr = ' '.join(cleanedstr)
        lastChar = cleanedstr[len(cleanedstr)-1]
        if lastChar == '\n':
            cleanedstr = cleanedstr[0:len(cleanedstr)-1]
        return cleanedstr


def generateURLFormat(job_title):
    split_jobTile = job_title.split(" ")
    if len(split_jobTile) > 1:
        jobTitleURL = "%20".join(split_jobTile)
    else:
        jobTitleURL = split_jobTile[0]
    return jobTitleURL


if __name__ == '__main__':
    main()
