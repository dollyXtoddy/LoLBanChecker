import requests, ssl, re, json

class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)
    
class macro:
	def __init__(self):
		self.session = requests.session()
		self.session.mount('https://', TLSAdapter())
	def check(self, username, password):
		self.session.post("https://auth.riotgames.com/api/v1/authorization", headers={"User-agent": "RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)"}, json={"acr_values": "","claims": "","client_id": "riot-client","code_challenge": "","code_challenge_method": "","nonce": "HDewORkVWVNXvZJLwvQlzA","redirect_uri": "http://localhost/redirect","response_type": "token id_token","scope": "openid link ban lol_region"})
		response = self.session.put("https://auth.riotgames.com/api/v1/authorization", headers={"User-agent": "RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)"}, json={"language":"en_US","password":password,"region":None,"remember":False,"type":"auth","username":username})
		if "auth_failure" not in response.text:
			bearer = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)').findall(response.json()['response']['parameters']['uri'])[0][0]
			r3 = self.session.post("https://auth.riotgames.com/userinfo",headers={"Authorization":f"Bearer {bearer}"},json={}).json()
			if str(r3['ban']['exp']) != 'None':
				print(f"[#] Account banned")
				print(json.dumps(r3['ban'], indent=4, sort_keys=True))
			else:
				print('[!] Account not banned.')
		else:
			print('[!] Invalid credentials.')

if __name__ == '__main__':
    macro().check(input('Username: '), input('Password: '))
