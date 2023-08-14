from utils.RedisInterface import RedisInterface

with RedisInterface() as redis_interface:
    value = redis_interface.get_fetched_email_ids('lamorim7657@outlook.com')
    uids = {1223, 342, 34234}
    key = 'lamorim7657@outlook.com'
    result = redis_interface.put_fetched_email_ids(key, uids)
    print(result)
    print(value)
