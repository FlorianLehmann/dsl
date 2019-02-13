If you're having trouble connecting to the arduino board with the visualization, try to alter the permissions on /dev/ttyACM0 (or whatever your serial port is) through this command : 

```shell
sudo chmod 666 /dev/ttyACM0
```