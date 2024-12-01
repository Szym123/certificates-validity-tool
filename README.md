# A simple tool to monitor the validity of certificates - local and remote

This tool checks at set intervals how much time is left until the expiry of the certificates stored in its list. And if this time is less than a set threshold, it displays this information in the web terminal.

## Configuration for Docker

Requirements:
* Docker version 24.0.7
* Docker Compose version v2.29.2-desktop.2

Start of configuration:

```bash
git clone https://github.com/Szym123/certificates-validity-tool.git
```

```bash
cd ./cd certificates-validity-tool/
```

```bash
docker build -t all:1.5 .
```

> [!IMPORTANT]
> If you need to change the image name and id, do the same in **docker-compose.yml**.

Followed by the this command:

```bash
docker-compose up
```

## Structure

```bash
.
├── Dockerfile
├── README.md
├── data
│   ├── cron.txt
│   ├── final.html
│   └── list.txt
├── docker-compose.yml
├── main.py
├── server.py
└── start.sh
```

## Working principle

The main components of this tool are two python scripts: **main.py** and **server.py**. Where the first is responsible for checking the lifetime of certificates and selecting those about to expire. While the second is responsible for displaying this information in the form of a simple web page.



### Main.py

The operation of the **main.py** script is based on the use of two fuctionalities from the openssl programme: 

* one checking local certificates:
```bash
echo -n Q | openssl x509 -noout -dates < FILE 
```

* the second to check remote certificates:
```bash
echo -n Q | openssl s_client -servername ADRESS -connect ADRESS:PORT | openssl x509 -noout -dates
```

The parameters of this script can be modified using **Config**, which is located at the beginning of the script:

```python
Config={
    "InputFile":"list.txt",
    "OutputFile":"final.html",
    "TimeStamp":[60,2]
}
```

List of options:
* **InputFile** - path to the file with the list of certificates to be checked, this must be a TEXT file
* **OutputFile** - path of the file to which the results of the program are returned, this must be an HTML file
* **TimeStamp** - a list containing the time after which the programme will inform that the certificate is about to expire, **[Weeks,Days]**

> [!WARNING]
> The **OutputFile** of the main.py script is also the **InputFile** for server.py.

### Server.py

This part of the tool provides data on certificates and error parts on the selected port. The parameters of this script can be modified using **Config**, which is located at the beginning of the script:

```python
Config={
    "InputFile":"/root/final.html",
    "Address":"0.0.0.0",
    "Port":8080
}
```

List of options:
* **InputFile** - path to the file with the list of certificates to be checked, this must be an HTMLfile
* **Address** - the ip address at which the service will be issued, given as a **string**
* **Port** - the port at which the service will be issued, in the form of an int

## Structure of the input file

```
en.wikipedia.org:443
my.crt:0
```

In order for the programme to work correctly, the input data must follow a certain pattern. On each line, we record the domain name or address together with the port on which the remote certificates are issued: ``ADREESS:PORT``. In the case of local certificates, on the other hand, the path to the certificate is entered inline and 0 is entered instead of the port number: ``FILE:0``.

## Containerisation

The container has been written in such a way that all resources placed in it are easily modifiable. Therefore, files are added using **docekr-compose**. The exception is the start.sh file, which is necessary for both scripts to run correctly at the same time.

```docker-compose
services:

  openssl:
    image: all:1.5
    container_name: all
    volumes:
      - ./data/list.txt:/root/list.txt
      - ./data/final.html:/root/final.html
      - ./data/cron.txt:/root/cron.txt
      - ./main.py:/root/main.py
      - ./server.py:/root/server.py
    ports:
      - 8080:8080
```

To modify the frequency of certificate checks, edit the contents of the file **cron.txt**:

```
* * * * * python3 $HOME/main.py
```
