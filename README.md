# HD-Wallet-Address-Derivation-System-Py
HD Wallet address derivation system for extracting addresses from Master Public Keys (xpub, ypub, zpub).



## How to Use

(requires)  -  xpub
(requires)  -  num_addresses
(requires)  -  account_index
(requires)  -  change_index
(optional)  -  type (manually define xpub, ypub, zpub)

*type: this is automatially interpreted based in prefix of 'xpub' input. Use type to manually define this.


application/json
```
{
"xpub":"zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
"num_addresses":"50",
"account_index":"0",
"change_index":"0"
}
```




## Requirements
Tested working on Ubuntu 22.04

**Local use:**
python3
python pip

**Docker use:**
Docker-Compose
Docker





## Setup
```
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
           "xpub": "zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
           "num_addresses": "21",
           "account_index": "0",
           "change_index": "0"
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
           "xpub": "zpub6mZc2YsabjXCoPD421fUTnWMDL6GkidmnW2AAcdGp5NL8zKFUtYfuT45NzyXp1GTRhGDyX4NWQQjCbt6TvzboTvFWQHKbXuV6VqkCCo33YC",
           "num_addresses": "21",
           "account_index": "0",
           "change_index": "0"
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
"num_addresses":"21",
"account_index":"0",
"change_index":"0"
}
```

