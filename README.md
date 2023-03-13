# port scan

## usage
```python
python3 port_scan.py 127.0.0.1,192.168.1.1
```

results are saved in txt files with ip addresses 
ex.  
127.0.0.1.txt  
192.168.1.1.txt

example:
```bash
complete scan 127.0.0.1 port range 1:65534 test timeouts: [0.5, 1]
send open ports [(3306, b'o\x00\x00\x00\n5.5.5-10.9.4-MariaDB-1:10.9.4+maria~ubu2204\x00\x18\x00\x00\x00[)VX6B-V\x00\xfe\xf7-\x02\x00\xff\x81\x15\x00\x00\x00\x00\x00\x00\x1d\x00\x00\x00L[aXt`aI*5j8\x00mysql_native_password\x00'), (52663, b'\x01\x00\x00\x00')]
recv open ports [3306, 6379, 6942]
send possible ports [(58016, '[Errno 22] Invalid argument')]
recv possible ports []
```