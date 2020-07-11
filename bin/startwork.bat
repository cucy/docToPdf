set path=%path%;%cd%\python3;%cd%\python3\Scripts

cd bin
celery -A task worker --loglevel=info >>../logs/worker.log