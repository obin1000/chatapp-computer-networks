# Chatapp computer networks

## How to use
Create and config file called 'server_info.ini' which looks like this:
```ini
[DEFAULT]
ip = 127.0.0.1
port = 9999
```

The following command will start a chat commandline client.
```shell script
python chat_app --client
```
Start a start a chat server
```shell script
python chat_app --server
```
List online users;
```shell script
!who
```
Send message
```shell script
@username message
```
Exit
```shell script
quit
```

