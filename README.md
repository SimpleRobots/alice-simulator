# alice-simulator
A standalone simulator for alice that behaves like a hardware robot.

## Run

**First install dependencies see below**

Clone the repository.
```bash
git clone https://github.com/penguinmenac3/alice-simulator.git
```

### Linux
In the bash go to the directory where you cloned alice-simulator.
```bash
./simulate_with_vis.sh
```

### Windows

Run the simulate_with_vis_python36.bat (for example by double clicking it).
```bash
simulate_with_vis_python36.bat
```

Or if you chose to install python27...
```bash
simulate_with_vis_python27.bat
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
```

```bash
pip install pillow scipy
```

If the pip install fails you may need to rerun it using sudo.

## Install Dependencies (Windows)

Download and install the most recent version of anaconda python37 for windows. (Python27 works too.)

https://www.continuum.io/downloads#windows

Download and install git.

https://git-scm.com/

Download opencv for python and copy the whl into the home folder.

(python27) http://www.lfd.uci.edu/~gohlke/pythonlibs/tuft5p8b/opencv_python-3.1.0-cp27-cp27m-win_amd64.whl

(python36) http://www.lfd.uci.edu/~gohlke/pythonlibs/tuft5p8b/opencv_python-3.3.0+contrib-cp36-cp36m-win_amd64.whl

Now install all the dependencies automatically.
```bash
install_python36.bat
```

If you want to stick with python27 for some reason use this instead.
```bash
install_python27.bat
```
