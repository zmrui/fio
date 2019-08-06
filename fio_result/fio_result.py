import back_
import os
import re
import csv

def get_nvr_list():
    path="/home/kg/"+back_.get_hostname()
    dirs=os.listdir(path)
    dirs.sort()
    return dirs

def get_result_dir():
    path="/home/kg/"+back_.get_hostname()+"/result/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def test_result(basepath,test):
    filepath=basepath+"fioresult/"+test+"/result"
    print(filepath)
    try:
        fileobj=open(filepath,"r")
    except:
        return 0.0
    filecontent=fileobj.read()
    print(filecontent)
    res=re.search('((BW=\d*\.\d*)|(BW=\d*))(M|K)(iB/s)',filecontent)
    (start,end)=res.span()
    result=filecontent[int(start)+3:int(end)]

    
    if re.match(".*KiB/s",result):
        numstr=result[:-5]
        num=float(numstr)
    elif re.match(".*MiB/s",result):
        numstr=result[:-5]
        num=float(numstr)*1024.0
    else:
        return 0.0
    return num

def compare(nvr_list,base,target):
    test_list=[]
    rw_list=['read', 'write', 'randread', 'randwrite', 'randrw']
    bs_list=['4k', '16k', '64k', '256k']
    iodepth_list=['1','8','64']
    for rw in rw_list:
            for bs in bs_list:
                for iod in iodepth_list:
                    arg=str(rw)+"_"+str(bs)+"_"+str(iod)
                    test_list.append(arg)
    
    filepath=get_result_dir()+nvr_list[base]+"-"+nvr_list[target]+".csv"
    result=[]
    temp_head=[]
    temp_head.append(" ")
    temp_head.append(nvr_list[base])
    temp_head.append(nvr_list[target])
    temp_head.append(nvr_list[target]+"->"+nvr_list[target])
    result.append(temp_head)
    for test in test_list:
        base_path="/home/kg/"+back_.get_hostname()+"/"+nvr_list[base]+"/"
        target_path="/home/kg/"+back_.get_hostname()+"/"+nvr_list[target]+"/"
        base_result=test_result(base_path,test)
        target_result=test_result(target_path,test)
        if target_result==0.0:
            continue
        compare_result=(target_result-base_result)/base_result*100
        compare_result_txt=str(compare_result)+"%"
        temp_item=[]
        temp_item.append(test)
        temp_item.append(base_result)
        temp_item.append(target_result)
        temp_item.append(compare_result_txt)
        result.append(temp_item)
    
    f = open(filepath,"w")
    writer=csv.writer(f)
    writer.writerows(result)
    f.close()

def process():
    back_.mountNFS()
    nvr_list=get_nvr_list()
    if "result" in nvr_list:
        nvr_list.remove("result")
    length=len(nvr_list)
    for i in range(0,length):
        for j in range(i+1,length):
            compare(nvr_list,i,j)
            
    back_.unmountNFS()


if __name__ == "__main__":
    process()
