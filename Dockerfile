FROM ubuntu

WORKDIR /root

COPY . .

RUN if ! [[ "16.04 18.04 20.04 22.04" == *"$(lsb_release -rs)"* ]]; \
then \
    echo "Ubuntu $(lsb_release -rs) is not currently supported."; \
    exit;  \
fi  \
curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc  &&\
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list  &&\
apt update  &&\
ACCEPT_EULA=Y apt install -y msodbcsql17  &&\
# optional: for bcp and sqlcmd
ACCEPT_EULA=Y apt install -y mssql-tools  &&\
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc  &&\
source ~/.bashrc  &&\
# optional: for unixODBC development headers
apt install -y unixodbc-dev

RUN apt update &&\
apt install -y python3 &&\
apt install -y python3-pip &&\
python3-pip install --no-cache-dir -r requirements.txt &&\
apt remove python3-pip

CMD ["python", "./focus.io.py"]