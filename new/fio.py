
import os
import back_
import csv
import re

def mydir(name):
    path="/home/fioresult/"+name
    try:
        if(not os.path.exists(path)):
            os.makedirs(path)
        return path
    except:
        print("mkdir error")
        return None

def run_all_test():
    
#    rw_list=['read', 'write', 'randread', 'randwrite', 'randrw']
#    bs_list=['4k', '16k', '64k', '256k']
#    iodepth_list=['1','8','64']
    rw_list=['read']
    bs_list=['4k', '16k', '64k']
    iodepth_list=['1']
    for rw in rw_list:
        for bs in bs_list:
            for iod in iodepth_list:
                arg=str(rw)+"_"+str(bs)+"_"+str(iod)
                dir=mydir(arg)
                if dir:
                    cmdbase='fio --rw=%s --bs=%s --iodepth=%s --runtime=1m --direct=1 --filename=/mnt/read_64k_8 --name=job1 --ioengine=libaio --thread --group_reporting --numjobs=16 --size=512MB --time_based --output=%s '
                    cmd=cmdbase%(rw,bs,iod,dir+"/result")
                    try:
                        print("test now: "+arg)
                        os.system(cmd)
                    except:
                        print("test error:"+arg)
    cmd1="lscpu > /home/fioresult/lscpu"
    cmd2="uname -a > /home/fioresult/uname"
    cmd3="sysctl -a > /home/fioresult/sysctl"
    cmd4="cat /boot/con* > /home/fioresult/bootinfo"
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)

def get_result_dir():
    path="/home/kg/"+back_.get_hostname()+"/result/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_test_result(basepath,test):
    filepath=basepath+"fioresult/"+test+"/result"
    #print(filepath)
    try:
        fileobj=open(filepath,"r")
    except:
        return 0.0
    filecontent=fileobj.read()
    #print(filecontent)
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

def compare(base,target):
    test_list=[]
    rw_list=['read', 'write', 'randread', 'randwrite', 'randrw']
    bs_list=['4k', '16k', '64k', '256k']
    iodepth_list=['1','8','64']
    for rw in rw_list:
            for bs in bs_list:
                for iod in iodepth_list:
                    arg=str(rw)+"_"+str(bs)+"_"+str(iod)
                    test_list.append(arg)
    
    filepath=get_result_dir()+base+"->"+target+".csv"
    result=[]
    temp_head=[]
    temp_head.append(" ")
    temp_head.append(base)
    temp_head.append(target)
    temp_head.append(base+"->"+target)
    result.append(temp_head)
    for test in test_list:
        base_path="/home/kg/"+back_.get_hostname()+"/"+base+"/"
        target_path="/home/kg/"+back_.get_hostname()+"/"+target+"/"
        base_result=get_test_result(base_path,test)
        target_result=get_test_result(target_path,test)
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
    
    with open(filepath,"w") as f:
        print("open:"+filepath)
        writer=csv.writer(f)
        writer.writerows(result)
        f.close()


def get_enviroment():
    return(os.environ['BASELINE'],os.environ['TARGET'])

def exist(arg):
    mainfolder=back_.main_dir()
    path=mainfolder+arg
    return os.path.exists(path)



def main():
    (BASELINE,TARGET)=get_enviroment()
    CURRENT=back_.get_nvr()
    back_.mountNFS()
    print("BASELINE="+BASELINE+",TARGENT="+TARGET)

    if TARGET==BASELINE:
        run_all_test()
        back_.copy_to_NFS()
        #back_.unmountNFS()
        print("run test:"+CURRENT)
        exit(0)
    elif (CURRENT != TARGET) and (CURRENT != BASELINE):
        if exist(TARGET) and exist(BASELINE):
            compare(BASELINE,TARGET)
            #back_.unmountNFS()
            print("compare:"+BASELINE+"->"+TARGET)
            exit(0)
        else:
            print("nothing to compare")
            #back_.unmountNFS()
            exit(4)
    elif (CURRENT == TARGET) and (CURRENT != BASELINE) and (exist(BASELINE)):
        run_all_test()
        back_.copy_to_NFS()
        compare(BASELINE,TARGET)
        #back_.unmountNFS()
        print("run test:"+CURRENT+";compare:"+BASELINE+"->"+TARGET)
        exit(0)
    elif (CURRENT == TARGET) and (CURRENT != BASELINE) and  (not exist(BASELINE)):
        run_all_test()
        back_.copy_to_NFS()
        back_.mountNFS()
        print("baseline result not exist")
        exit(2)
    elif (CURRENT != TARGET) and (CURRENT == BASELINE) and (exist(TARGET)):
        run_all_test()
        back_.copy_to_NFS()
        compare(BASELINE,TARGET)
        #back_.unmountNFS()
        print("run test:"+CURRENT+";compare:"+BASELINE+"->"+TARGET)
        exit(0)
    elif (CURRENT != TARGET) and (CURRENT == BASELINE) and (not  exist(TARGET)):
        run_all_test()
        back_.copy_to_NFS()
        #back_.unmountNFS()
        print("target result not exist")
        exit(3)

    else:
        print("undefined arguments")
        #back_.unmountNFS()
        exit(5)
    

if __name__ == "__main__":
    main()
