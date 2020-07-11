set path=%path%;%cd%\python3;%cd%\python3\Scripts

cd bin
python web.py 8080 >>../logs/web1.log