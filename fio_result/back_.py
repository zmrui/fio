import os

def get_nvr():
    cmd_nvr="uname -r"
    nvr_obj=os.popen(cmd_nvr)
    nvr=(nvr_obj.readlines())[0]
    nvr=nvr[:-1]
    return nvr

def get_hostname():
    cmd_hn="hostname"
    hn_obj=os.popen(cmd_hn)
    hn=(hn_obj.readlines())[0]
    hn=hn[:-1]
    return hn

def mountNFS():
    if not os.path.exists("/home/kg"):
        os.makedirs("/home/kg")
    cmd="mount -t nfs vmcore.usersys.redhat.com:/data/kgqe/scheduler/fio/ /home/kg/"
    try:
        os.system(cmd)
        return "/home/kg/"
    except:
        return None


def unmountNFS():
    cmd="umount -f -l /home/kg"
    try:
        os.system(cmd)
    except:
        return ""


if __name__ == "__main__":
    print(current_dir())