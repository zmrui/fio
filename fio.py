import os
import back
import csv
import re
import time

def mydir(name):
    '''mkdir for test result'''
    path="/home/fioresult/"+name
    try:
        if(not os.path.exists(path)):
            os.makedirs(path)
        return path
    except:
        print("mkdir error")
        return None

def run_all_test():
    '''run all 5*4*3=60 tests'''
    rw_list=['read', 'write', 'randread', 'randwrite', 'randrw']
    bs_list=['4k', '16k', '64k', '256k']
    iodepth_list=['1','8','64']
    for rw in rw_list:
        for bs in bs_list:
            for iod in iodepth_list:
                arg=str(rw)+"_"+str(bs)+"_"+str(iod)
                dir=mydir(arg)
                if dir:
                    cmdbase='fio --rw=%s --bs=%s --iodepth=%s --runtime=1m --direct=1 --filename=/mnt/read_64k_8 --name=job1 --ioengine=libaio --thread --group_reporting --numjobs=16 --size=512MB --time_based --output=%s '
                    result_output_path=dir+"/result"
                    cmd=cmdbase%(rw,bs,iod,result_output_path)
                    try:
                        beakerlog("Running:"+cmd)
                        os.system(cmd)
                        while not os.path.exists(result_output_path):
                            time.sleep(61)
                            print("waiting for fio exec end")
                        cmd6="echo -e '\n~~~~~~~~~~~~~~~~~"+arg+"~~~~~~~~~~~~~~~~~\n' >> /home/fioresult/output.log "
                        cmd5="cat "+result_output_path+" >> /home/fioresult/output.log"
                        os.system(cmd6)
                        os.system(cmd5)
                    except:
                        print("test error:"+arg)
    cmd1="lscpu > /home/fioresult/lscpu"
    cmd2="uname -a > /home/fioresult/uname"
    cmd3="sysctl -a > /home/fioresult/sysctl"
    cmd4="cat /boot/con* > /home/fioresult/bootinfo"
    cmd5="cat /proc/meminfo > /home/fioresult/meminfo"
    cmd6="tuned-adm active > /home/fioresult/tuned"
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)

def get_result_dir():
    '''make or return folder to place result'''
    path="/home/kg/"+back.get_hostname()+"/result/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_test_result(basepath,test):
    '''fetch bandwigth result from output file'''
    filepath=basepath+"fioresult/"+test+"/result"
    try:
        fileobj=open(filepath,"r")
    except:
        return 0.0
    filecontent=fileobj.read()
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
    '''compare two test result, generate a csv report'''
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
    temp_head.append(base+" (KiB/S)")
    temp_head.append(target+" (KiB/S)")
    temp_head.append(base+"->"+target)
    result.append(temp_head)
    for test in test_list:
        base_path="/home/kg/"+back.get_hostname()+"/"+base+"/"
        target_path="/home/kg/"+back.get_hostname()+"/"+target+"/"
        base_result=get_test_result(base_path,test)
        target_result=get_test_result(target_path,test)
        if target_result==0.0:
            continue
        compare_result=round((target_result-base_result)/base_result*100,2)
        compare_result_txt=str(compare_result)+"%"
        temp_item=[]
        temp_item.append(test)
        temp_item.append(base_result)
        temp_item.append(target_result)
        temp_item.append(compare_result_txt)
        result.append(temp_item)

    with open(filepath,"w") as f:
        beakerlog("open:"+filepath)
        writer=csv.writer(f)
        writer.writerows(result)
        f.close()
        beakersubmitfile(filepath,base+"->"+target+".csv")


def get_enviroment():
    '''get enviroment varibles'''
    baseline=str(os.environ['BASELINE'])
    target=str(os.environ['TARGET'])
    return(baseline,target)

def exist(arg):
    '''check if result exist'''
    mainfolder=back.main_dir()
    path=mainfolder+arg
    return os.path.exists(path)

def beakerlog(string):
    cmd=''' . /usr/bin/rhts-environment.sh
            . /usr/share/beakerlib/beakerlib.sh
            rlLogInfo "%s"  '''%(string)
    os.system(cmd)

def beakereport(name,result):
    cmd=''' . /usr/bin/rhts-environment.sh
            . /usr/share/beakerlib/beakerlib.sh
            rlReport "%s" "%s" '''%(name,result)
    os.system(cmd)

def beakersubmitfile(path,name):
    cmd=''' . /usr/bin/rhts-environment.sh
            . /usr/share/beakerlib/beakerlib.sh
            rlFileSubmit "%s" "%s" '''%(path,name)
    os.system(cmd)

def main():
    (BASELINE,TARGET)=get_enviroment()
    CURRENT=back.get_nvr()
    back.mountNFS()

    if TARGET==BASELINE:
        run_all_test()
        back.copy_to_NFS()
        back.unmountNFS()
        beakereport("Run test:"+CURRENT,"PASS")
        exit(0)
    elif (CURRENT != TARGET) and (CURRENT != BASELINE):
        if exist(TARGET) and exist(BASELINE):
            compare(BASELINE,TARGET)
            back.unmountNFS()
            beakereport("Compare:"+BASELINE+"->"+TARGET,"PASS")
            exit(0)
        else:
            beakerlog("nothing to compare")
            back.unmountNFS()
            exit(4)
    elif (CURRENT == TARGET) and (CURRENT != BASELINE) and (exist(BASELINE)):
        run_all_test()
        back.copy_to_NFS()
        compare(BASELINE,TARGET)
        back.unmountNFS()
        beakereport("Run test:"+CURRENT,"PASS")
        beakereport("Compare:"+BASELINE+"->"+TARGET,"PASS")
        exit(0)
    elif (CURRENT == TARGET) and (CURRENT != BASELINE) and  (not exist(BASELINE)):
        run_all_test()
        back.copy_to_NFS()
        back.mountNFS()
        beakereport("baseline result not exist","FAIL")
        exit(2)
    elif (CURRENT != TARGET) and (CURRENT == BASELINE) and (exist(TARGET)):
        run_all_test()
        back.copy_to_NFS()
        compare(BASELINE,TARGET)
        back.unmountNFS()
        beakereport("Run test:"+CURRENT,"PASS")
        beakereport("Compare:"+BASELINE+"->"+TARGET,"PASS")
        exit(0)
    elif (CURRENT != TARGET) and (CURRENT == BASELINE) and (not  exist(TARGET)):
        run_all_test()
        back.copy_to_NFS()
        back.unmountNFS()
        beakereport("target result not exist","FAIL")
        exit(3)
    else:
        beakereport("undefined arguments","FAIL")
        back.unmountNFS()
        exit(5)

if __name__ == "__main__":
    main()
