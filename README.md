# alice-simulator
A standalone simulator for alice that behaves like a hardware robot.

## Run

(First install dependencies see below)

Clone the repository.
```bash
git clone git@github.com:penguinmenac3/alice-simulator.git
```

### Linux
In the bash go to the directory where you cloned alice-simulator.
```bash
./simulate_with_vis.sh
```

### Windows

In the bash inside the folder where you cloned alice-simulator run the bat script.
```bash
simulate_with_vis.bat
```

## Install Dependencies (Ubuntu)

Update and upgrade your system.

```bash
sudo apt-get update
sudo apt-get upgrade
```

Install git, python, pip and python-dev.

```bash
sudo apt-get install git python python-pip python-dev libopencv-dev python-opencv
pip install pillow
```

## Install Dependencies (Windows)

Download and install the most recent version of anaconda python for windows. (Python2.7 and Python3.x should both be fine)

https://www.continuum.io/downloads#windows

Download and install git.

https://git-scm.com/

Download and install opencv for python.
(32-bit)
http://www.lfd.uci.edu/~gohlke/pythonlibs/ru4fxw3r/opencv_python-3.1.0-cp27-cp27m-win32.whl

(64-bit)
http://www.lfd.uci.edu/~gohlke/pythonlibs/ru4fxw3r/opencv_python-3.1.0-cp27-cp27m-win_amd64.whl

Install pillow
```bash
pip install pillow
```
