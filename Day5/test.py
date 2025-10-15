# from werkzeug.security import generate_password_hash as gph
# from werkzeug.security import check_password_hash as cph

# password = "hritik"

# # Generating
# hash_password = gph(password)
# print(hash_password) # scrypt:32768:8:1$p34425F4fMX11LJA....

# # Check
# login_pass = 'hritik'
# print(cph(hash_password, login_pass))


import matplotlib
import matplotlib.pyplot as plt

x = ['User', 'Creators', "Admin"]
y = [10, 5, 1]

plt.bar(x,y)
plt.savefig('test.png')