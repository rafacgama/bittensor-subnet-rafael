# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Rafael Gama
# Copyright © 2023 <your name>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import torch
import bittensor as bt
from typing import List
import template
import hashlib
from template.validator.rafacoin import add_rafacoin_hash


def hash_validation(values: template.protocol.Dummy, response: int) -> float:
    hash_data = (str(values.block_number) + values.transactions + values.previous_hash + str(response))
    hash = hashlib.sha256(hash_data.encode()).hexdigest()

    if (hash.startswith("0" * values.dificulty)) and (
            not values.previous_hash or int(hash, 16) < int(values.previous_hash, 16)):

        bt.logging(f'New hash: {hash} was validated and added to rafacoin ledger')
        add_rafacoin_hash(hash)
        return 1
    return 0


def get_rewards(
    self,
    values: int,
    responses: List[float],
) -> torch.FloatTensor:
    """
    Returns a tensor of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[float]): A list of responses from the miner.

    Returns:
    - torch.FloatTensor: A tensor of rewards for the given query and responses.
    """
    # Get all the reward results by iteratively calling your reward() function.
    weights = []
    for response in responses:
        weight = 0
        if response.dendrite.status_code == 200:
            weight = hash_validation(values, response)
        weights.append(weight)

    # Get all the reward results by iteratively calling your reward() function.
    return torch.FloatTensor(weights).to(self.device)
