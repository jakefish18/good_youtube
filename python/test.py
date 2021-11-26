import keyring

f = keyring.get_password('good_tube', 'insaf')

print(f)