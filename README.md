Welcome to the "homelab montioring and provisioning tool". 

What this tool is designed to do, is use a web browser (currently ran on the local interface (127.0.0.1:5000), but will be moved to an http:///{some_IP_address} at some point), that allows the user to monitor the status of their Hosts and VMs, while allowing them to use python to spin up new VMs for testing {or whateve}.

Prerequisites:
admin privilages on the system that will be hosting the server
flask
nmap
proxmoxer (that is the hypervisor used in buidling/testing this)
DNS configuration (I used PFsense in building this)


Program Hierarcy:
Root Directory
|______Templates
       |__index.html
|__ app.py
|_hosts.csv

Once the struture is built, it should like something like this:
C:\path\to\monitoring_tools (root directory)
app.py
hosts.csv
C:\path\to\monitoring_tools\Template\index.html

Logic of the program:

The nmap scan passes the following arguments to NMAP: -R (to resolve the hostname), -v (for verbose data in the terminal :)), and -sn (for a clean simple scan).
It will take the normal range of inputs like: 192.168.103.1, or ranges like: 192.168.103.1-20 an it can scan entire subnets like 192.168.103.0/24.
It will display the output like:
FQDN | IP | Status (up or down)

The provsioning section allows you select a host (pulled from hosts.csv{modify file as needed. one host per line)) to add the VM to. There is a dropdown that will allow you to look at the OS's currently available on that host. You can tweak all the normal setings during creation. Make sure you have root prviilages to your Proxmox instance too.

Once the VM has been created, the program will interact the PFsesne API to create a resolvable DNS reservation for the newly created VM.

Have fun. Feel free to tweak as needed!

-Andrew (AnCo!)
