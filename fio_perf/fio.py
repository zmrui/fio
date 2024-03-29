import os

def mydir(name):
    path="/home/fioresult/"+name
    try:
        if(not os.path.exists(path)):
            os.makedirs(path)
        return path
    except:
        print("mkdir error")
        return None

if __name__ == "__main__":
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
                        print("now: "+arg)
                        os.system(cmd)
                    except:
                        print(arg)
    cmd1="lscpu > /home/fioresult/lscpu"
    cmd2="uname -a > /home/fioresult/uname"
    cmd3="sysctl -a > /home/fioresult/sysctl"
    cmd4="cat /boot/con* > /home/fioresult/bootinfo"
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
