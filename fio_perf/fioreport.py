import re
import os

def progress(path):
    filepath=path+"/result"
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
    

def func():
    temp_str="{start_fio_result;"
    rw_list=['read', 'write', 'randread', 'randwrite', 'randrw']
    bs_list=['4k', '16k', '64k', '256k']
    iodepth_list=['1','8','64']
    for rw in rw_list:
            for bs in bs_list:
                for iod in iodepth_list:
                    arg=str(rw)+"_"+str(bs)+"_"+str(iod)
                    path="/home/fioresult/"+arg
                    speed=progress(path)
                    temp_str=temp_str+arg+","+str(speed)+";"
    print(temp_str)
                    
                    
if __name__ == "__main__":
    func()
