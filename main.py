import requests
import json

def retrieve_and_save_messages(channel_id, num_messages=10):
    num = 0
    limit = min(num_messages, 100)  # Discord API limit for message retrieval

    headers = {
        'authorization': 'Your token here user token'
    }

    last_message_id = None
    scammer_data = []

    while num < num_messages:
        query_parameters = f'limit={limit}'
        if last_message_id is not None:
            query_parameters += f'&before={last_message_id}'

        r = requests.get(
            f'https://discord.com/api/v9/channels/{channel_id}/messages?{query_parameters}', headers=headers
        )
        json_data = json.loads(r.text)
        if len(json_data) == 0:
            break

        for message in json_data:
            user_id_start = message['content'].find(':') + 2
            user_id_end = message['content'].find('(', user_id_start)
            user_id = message['content'][user_id_start:user_id_end].strip()
            reason_start = user_id_end + 1
            reason_end = message['content'].find(')', reason_start)
            reason = message['content'][reason_start:reason_end]
            scammer_entry = {'user_id': user_id, 'reason': reason}
            print('Scammer Data:', scammer_entry)
            scammer_data.append(scammer_entry)
            last_message_id = message['id']
            num += 1
            if num >= num_messages:
                break

    print('Number of messages collected:', num)

    with open('parsed.json', 'w') as f:
        json.dump(scammer_data, f, indent=4)

retrieve_and_save_messages('channel to parse data', num_messages=no of messages you want to parse in int)
