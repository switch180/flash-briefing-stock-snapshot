from itsdangerous import URLSafeSerializer
from getpass import getpass
from chalicelib import config

private_path = config.private_path

password = getpass("Enter your encryption password:\n")
dangerous_world = URLSafeSerializer(password)
signature = dangerous_world.dumps(private_path)
print("The secret is:\n{}".format(signature))
print("Use as [rest endpoint]/api/{}/{}".format(private_path, signature))

#TODO SM too
