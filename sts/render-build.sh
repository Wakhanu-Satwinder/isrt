apt-get update && apt-get install -y build-essential
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env


set -o errexit
apt-get update && apt-get install -y libjpeg-dev zlib1g-dev
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput