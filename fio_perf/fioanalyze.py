import re
import requests
import csv

def fetch_result(filecontent):
    listretuen=[]
    res=re.search("{start_fio_result.*end_fio_result}",filecontent)
    (start,end)=res.span()
    result=filecontent[int(start):int(end)]
    mylist=result.split("; ")
    mylist.remove("end_fio_result}")
    mylist.remove("{start_fio_result")
    for item in mylist:
        pairs=str(item).split(",")
        key=pairs[0]
        value=pairs[1]
        temp_item={'test':key,
                   'result':value}
        listretuen.append(temp_item)
    return listretuen


def request_log(url):
    response=requests.get(url)
    return fetch_result(response.text)

def request_log_test(text):
    return fetch_result(text)

def fetch_tests(result_list):
    tests=[]
    temp_list=result_list[0]['tests_list']
    for item in temp_list:
        tests.append(str(item['test']))#('test':key,'result':value)
    return tests

def fetch_distros(result_list):
    distros=[]
    for item in result_list:
        distro=item['distro']
        distros.append(distro)
    return distros

def result_at(result_list,distro_name,test_name):
    for item in result_list:
        if item['distro']==distro_name:
            for itemm in item['tests_list']:
                if itemm['test']==test_name:
                    return str(itemm['result'])

def analyze(result_list):
    tests=fetch_tests(result_list)
    distros=fetch_distros(result_list)
    dic=[]
    temp_item=[]
    temp_item.append(" ")
    for distro in distros:
        temp_item.append(str(distro))
    dic.append(temp_item)
    for test in tests:
        row=[]
        row.append(str(test))
        for distro in distros:
            temp_str=result_at(result_list,str(distro),str(test))
            row.append(str(temp_str))
        dic.append(row)

    with open("1.csv","w",newline="") as f:
        writer=csv.writer(f)
        writer.writerows(dic)

        

if __name__ == "__main__":
    distrolog=[]
    while True:
        distro=input("input system distro (nvr asc):")
        if distro=="ok":
            break
        log_url=input("input result log url:")
        temp_item={'distro':distro,
                    'log_url':log_url}
        distrolog.append(temp_item)

    data=[]
    for item in distrolog:
        distro=str(item['distro'])
        url=str(item['log_url'])
        if True:
            temp_list=request_log(url)
        else:
            temp_list=request_log_test('''''')
        temp_item={
            'distro':distro,
            'tests_list':temp_list}
        data.append(temp_item)

    analyze(data)
