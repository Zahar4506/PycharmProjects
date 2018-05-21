import vk
session = vk.Session(access_token='5468a153fce3fde17f358bbcbe410c2eb08aa53f7d1bcb7d959e0ec0e44c621ae14909f1d33b814778e6b')
vk_api = vk.API(session)
profiles = vk_api.users.get(user_id=197181811, fields='online, last_seen')
print(profiles)
