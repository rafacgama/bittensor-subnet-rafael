#!/bin/sh

echo "creating owner wallet..."
btcli wallet new_coldkey --no_password --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating miner wallet..."
btcli wallet new_coldkey --no_password --wallet.name miner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet new_hotkey --no_password --wallet.name miner --wallet.hotkey default --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating validator wallet..."
btcli wallet new_coldkey --no_password --wallet.name validator --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
btcli wallet new_hotkey --no_password --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "minting tokens for owner..."
# Run a loop to create enough owner coins to create a subnet
for i in 1 2 3 4
do
  echo "started minting owner token interation: $i"
  btcli wallet faucet --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt
  echo "finished minting owner token interation: $i"
done

echo "minting tokens for miner..."
btcli wallet faucet --wallet.name miner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "minting tokens for validator..."
btcli wallet faucet --wallet.name validator --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "creating subnet..."
btcli subnet create --wallet.name owner --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "registering miner in subnet..."
btcli subnet register --wallet.name miner --wallet.hotkey default --netuid 1 --subtensor.chain_endpoint ws://0.0.0.0:9946 --subtensor.network local --no_prompt

echo "registering validator in subnet..."
btcli subnet register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "Staking validator ..."
btcli stake add --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "registering validator in the root subnet..."
btcli root register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt

echo "boosting subnet..."
btcli root boost --netuid 1 --increase 1 --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --subtensor.network local --no_prompt
