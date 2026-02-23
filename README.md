# HD-Wallet-Address-Derivation-System-Py
HD Wallet address derivation system for extracting addresses from Master Public Keys (xpub, ypub, zpub).



## How to Use

(requires)  -  xpub

(requires)  -  num_addresses                                    -     (default: 20)

(requires)  -  account_index                                    -     (default: 0)

(requires)  -  derivation_index                                 -     (default: 0)

(optional)  -  type (manually define xpub, ypub, zpub)          -     (default: zpub)

* *type: this is automatially interpreted based on the prefix of the master public key (xpub variable). Use type to manually define this.* *




application/json
```
{
"xpub":"zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
"num_addresses":"20",
"derivation_index":"0",
"account_index":"0",
"type":"zpub"
}
```




## Requirements


Tested working on Ubuntu 22.04


**Local use:**

sudo apt install python3 python3-pip -y

pip install -r requirements.txt

* *if you have trouble with pip accessing the internet to install requirements.txt - create a directory called 'packages' in the same directory as the main.py script. Then manually download the pip packages to to the newly created packages directory and use the following command:* *
pip install --no-index --find-links=/app/packages fastapi uvicorn bitcoinlib python-dotenv

* *run the script with:* *
python3 main.py


**Docker use:**

Docker-Compose

Docker





## Setup
```
mkdir ~/GIT
cd ~/GIT
mkdir HD-Wallet-Address-Derivation-System-Py
cd HD-Wallet-Address-Derivation-System-Py/
git clone https://github.com/BasketCase808/HD-Wallet-Address-Derivation-System-Py
docker-compose up -d --build
echo "Testing .."
sleep 2
curl -X POST http://localhost:8000/derive-addresses \
     -H "Content-Type: application/json" \
     -d '{
          "xpub":"zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
          "num_addresses":"20",
          "derivation_index":"0",
          "account_index":"0",
          "type":"zpub"
         }'
sleep 1
echo "If you get a list of raw addresses, it worked!"
```




## Application Use

**Terminal**
```
curl -X POST http://localhost:8000/derive-addresses \
     -H "Content-Type: application/json" \
     -d '{
          "xpub":"zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
          "num_addresses":"20",
          "derivation_index":"0",
          "account_index":"0",
          "type":"zpub"
         }'

```

**GUI**
Download Poracora or Postman.
1. create New HTTP Request.
2. Set: POST
3. set URL: http://localhost:8000/derive-addresses
4. leave headers empty - select body tab -
5. Set type: Raw - application/json
6. Set Body:
```
{
"xpub":"zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
"num_addresses":"20",
"derivation_index":"0",
"account_index":"0",
"type":"zpub"
}
```

First address should show:
bc1qc3zpt8ptn35q33qlya4c337f8v7m89394j9dvs
