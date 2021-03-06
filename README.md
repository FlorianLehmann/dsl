This project uses Python 3. This project require pip and pipenv to manage its python dependencies and environment. To install pipenv, run (with pip installed) :

```shell
pip install pipenv
```

Then, at the root of the project, run this command to install dependencies :

```shell
pipenv install
```

When this is done, you can go into the pipenv virtual environment with : 

```shell
pipenv shell
```

Inside the pipenv virtual environment, run the following command to run the scenario simple_led.arduinoml and write it into simple_led.ino :

```shell
python -m pyArduinoML.antlr.main pyArduinoML/resources/led_button_and_time.arduinoml > simple_led.ino
```

Still the pipenv virtual environment, run the following command to start a web server on `http://127.0.0.1:8050/` for the debugging visualization.

```shell
python -m pyArduinoML.visualization.visualization
```

If you're having trouble connecting to the arduino board with the visualization, try to alter the permissions on /dev/ttyACM0 (or whatever your serial port is) through this command : 

```shell
sudo chmod 666 /dev/ttyACM0
```
