import os

RAFACOIN_LEDGER = 'rafacoin_ledger.txt'  # Example file path


def get_last_rafacoin_hash() -> str:
    """
    Retrieves the last line from a file efficiently, intended to be used to fetch the last block hash in a blockchain ledger file.
    """
    with open(RAFACOIN_LEDGER, 'rb') as f:
        f.seek(0, os.SEEK_END)  # Go to the end of the file
        file_size = f.tell()
        if file_size == 0:
            return ""  # Return an empty string if the file is empty

        f.seek(max(-1024, -file_size), os.SEEK_END)  # Seek the last 1024 bytes or the whole file if it's smaller
        lines = f.readlines()  # Read to the end of the file
        if lines:
            last_line = lines[-1].decode().strip()
        else:
            last_line = ""
        return last_line


def add_rafacoin_hash(line: str) -> None:
    """
    Appends a new line to the ledger file, typically used to add a new block hash.
    """
    with open(RAFACOIN_LEDGER, 'a') as f:  # Open file in append mode
        f.write(line + '\n')
