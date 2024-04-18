<div align="center">

# **Bitcoin-inspired Bittensor Subnet** <!-- omit in toc -->


</div>

---
- [Introduction](#introduction)
- [Installation](#installation)
- [Wallets](#wallets)

---

## Introduction

The customized subnet mimics the Bitcoin blockchain mechanism in a simplified fashion to avoid unnecessary complexity 
for the sake of this exercise. Validators relay the current state of the network, while miners engage in computing a 
new hash value by integrating a random nonce integer with a combination of new block information and the hash of the 
previous block. The difficulty integer value represents the number of zeros the new hash must start with.

A couple of things to notice are that this subnet does not support concurrency and only one miner can be created.

---

## Installation

- **Running locally**: The subnet was created based on the instructions from [Running Subnet Locally](./docs/running_on_staging.md).
- **Build the blockchain server**: From the project root folder run `docker-compose build` followed by `docker-compose up` in
order to build the image and run the container
- **Set up Subnet/Miner/Validador**: Once the container is up and running, execute the following steps:
  - `docker exec -it bittensor_subnet bash` from a terminal to access to the running container
  - `cd ..` to go back to the `/app` folder
  - `cd bittensor-subnet-rafael`
  - `chmod +x create_subnet.sh`
  - `./create_subnet.sh`

This process will run for several minutes. All commands from `create_subnet.sh` are set to have no prompt, but the
command to stake the validator will ask `Stake all Tao from account: 'validator'? [y/n]:` where `y` should be selected.
Following that, there will be an attempt to boost the subnet which will fail. For that to work, the command
`btcli root boost --netuid 1 --increase 1 --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt`
needs to be reapplied after the blockchain is running for some time (over 90 minutes).

Once that the blockchain is up and running, the following commands need to be executed to initiate the subnet miner and 
validator. 
- Open two terminals and execute `docker exec -it bittensor_subnet bash` in each
- Run the following commands, one in each terminal:
  - `python3 neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --wallet.name miner --wallet.hotkey default --logging.debug`
  - `python3 neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --wallet.name validator --wallet.hotkey default --logging.debug`

Now that the setup is complete the miners will start to calculate the hashes and, after validation, they will be stored
in the `rafacoin_ledger.txt` file, which acts like the ledger book for all the hashes of the blocks created

The miner/validator logic can be found in this repo under:
- Miner: `neurons/miner/py`
- Validator: `template/validator/forward.py`

---

## Wallets

As of the time of this writing, nearly 72,000 blocks have been mined. Below are the Miner and Validator wallets.

**Miner**    
```                                            
Subnet: 1                                                                                                                                                                            
COLDKEY  HOTKEY   UID  ACTIVE    STAKE(τ)     RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS   EMISSION(ρ)   VTRUST  VPERMIT  UPDATED  AXON                HOTKEY_SS58               
miner    default  0      True   195.57109  1.00000  1.00000    1.00000    1.00000    0.00000   410_002_288  0.00000        *     1116  187.65.224.80:8091  5CUrAqDRg2Lgf6CfShSNLH2tc…
1        1        1            τ195.57109  1.00000  1.00000    1.00000    1.00000    0.00000  ρ410_002_288  0.00000                                                                  
                                                                               Wallet balance: τ299.0                                                                                
```

**Validator**  
```

Subnet: 0                                                                                                                                                                            
COLDKEY    HOTKEY   UID  ACTIVE   STAKE(τ)     RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS  EMISSION(ρ)   VTRUST  VPERMIT  UPDATED  AXON  HOTKEY_SS58                             
validator  default  0      True  494.57109  0.00000  0.00000    0.00000    0.00000    0.00000            0  0.00000               659  none  5CUxnA3XcyPKKXk5XL17Wh2cf6dssGLTr752YKd…
                    1                       0.00000  0.00000    0.00000    0.00000    0.00000           ρ0  0.00000                                                                  
Subnet: 1                                                                                                                                                                            
COLDKEY    HOTKEY   UID  ACTIVE    STAKE(τ)     RANK    TRUST  CONSENSUS  INCENTIVE  DIVIDENDS   EMISSION(ρ)   VTRUST  VPERMIT  UPDATED  AXON                HOTKEY_SS58             
validator  default  1      True   494.57109  0.00000  0.00000    0.00000    0.00000    1.00000   410_002_288  1.00000        *       64  187.65.224.80:8091  5CUxnA3XcyPKKXk5XL17Wh2…
2          2        2            τ494.57109  0.00000  0.00000    0.00000    0.00000    1.00000  ρ410_002_288  1.00000                                                                
                                                                               Wallet balance: τ1e-06
```




---

