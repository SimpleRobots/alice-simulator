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
sudo apt-get install git python python-pip python-dev
```

Install dependencies by running the install_deps.py in the commandline.
```bash
python install_deps.py
```

## Install Dependencies (Windows)

Download and install the most recent version of anaconda python for windows. (Python2.7 and Python3.x should both be fine)

https://www.continuum.io/downloads#windows

Download and install git.

https://git-scm.com/

Install dependencies by running the install_deps.py in the commandline.
```bash
python install_deps.py
```
