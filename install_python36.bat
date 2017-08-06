@echo off

:ask_anaconda
echo Download and install anaconda for Python 3.
echo https://www.continuum.io/downloads#windows
echo Did you install anaconda for Python 3? [y/n]
set INPUT=
set /P INPUT=Type input: %=%
if %INPUT%==y goto anaconda
if %INPUT%==Y goto anaconda
if %INPUT%==N goto no_anaconda
if %INPUT%==n goto no_anaconda
echo Invalid Input
goto ask_anaconda

:no_anaconda
echo Install anaconda for Python 3 first and then rerun the install.bat
goto exit

:anaconda
call conda create -n alice36 python=3.6
call activate alice36
call conda install mkl
call conda install numpy
call conda install scipy
pip install pillow

:ask_opencv
echo Download and copy opencv next to the install script:
echo http://www.lfd.uci.edu/~gohlke/pythonlibs/tuft5p8b/opencv_python-3.3.0+contrib-cp36-cp36m-win_amd64.whl
echo If the link is broken search on that site for opencv_python-3.3.0+contrib-cp36-cp36m-win_amd64
echo Did you download and copy the opencv file next to the install.bat? [y/n]
set INPUT=
set /P INPUT=Type input: %=%

if %INPUT%==y goto opencv
if %INPUT%==Y goto opencv
if %INPUT%==N goto no_opencv
if %INPUT%==n goto no_opencv
echo Invalid Input
goto ask_opencv

:no_opencv
echo Download the file first and then rerun the install.bat

:opencv
pip install "opencv_python-3.3.0+contrib-cp36-cp36m-win_amd64.whl"

echo Done. Everything should be installed if there were no errors.
echo Try running the simulator with simulate_with_vis.bat next.
pause

