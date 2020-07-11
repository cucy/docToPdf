set path=%path%;%cd%\python3;%cd%\python3\Scripts

cd bin
python web.py 8081 >>../logs/web2.log