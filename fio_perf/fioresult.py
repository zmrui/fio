import re
import os

def progress(path):
    filepath=path+"/result"
    #print(filepath)
    fileobj=open(filepath,"r")
    filecontent=fileobj.read()
    #print(filecontent)
    res=re.search('((BW=\d*\.\d*)|(BW=\d*))',filecontent)
    (start,end)=res.span()
    result=filecontent[int(start):int(end)]
    #print(result,end="")

    num=result[3:]
    return float(num)
    

def func(arc):
    print("++++++++++++++++++++++++arch:"+arc+"node++++++++++++++++++++")
    print("rw_bs_iodep,(8-7.6)/7.6,(8-alt)/alt,(alt-7.6)/7.6,BW7,BWalt,BW8")
    rw_list=['read', 'write', 'randread', 'randwrite', 'randrw']
    bs_list=['4k', '16k', '64k', '256k']
    iodepth_list=['1','8','64']
    for rw in rw_list:
            for bs in bs_list:
                for iod in iodepth_list:
                    arg=str(rw)+"_"+str(bs)+"_"+str(iod)
                    path8="/home/mizhang/fioresult/"+arc+"/8.0/fio/"+str(arg)
                    path7="/home/mizhang/fioresult/"+arc+"/7.6/fio/"+str(arg)
                    path7alt="/home/mizhang/fioresult/"+arc+"/alt76/fio/"+str(arg)
                    print(arg+",",end="")
                    speed7=progress(path7)
                    speed8=progress(path8)
                    speed7alt=progress(path7alt)

                    result1=(speed8-speed7)*100/speed7
                    if result1>0:
                        print("+",end="")
                    print((("%.2f"%result1+"%"))+",",end="")

                    result2=(speed8-speed7alt)*100/speed7alt
                    if result2>0:
                        print("+",end="")
                    print((("%.2f"%result2+"%"))+",",end="")
                    
                    result3=(speed7alt-speed7)*100/speed7
                    
                    if result3>0:
                        print("+",end="")
                    print((("%.2f"%result3+"%"))+",",end="")

                    print(str(speed7)+","+str(speed7alt)+","+str(speed8))
                    
if __name__ == "__main__":
    arcs=['x862d']
    for arc in arcs:
        func(str(arc))
