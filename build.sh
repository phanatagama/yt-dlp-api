echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python -m venv venv

# activate the virtual environment
source venv/bin/activate

# install all deps in the venv
pip install --user pipenv

pipenv install
# pip install -r requirements.txt

# collect static files using the Python interpreter from venv
# python manage.py collectstatic --noinput

echo "BUILD END"

# [optional] Start the application here 
pipenv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app 