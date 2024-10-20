import json
import requests
import time

token = 'sometokenhere'
chat_ids = set()
notified = set()

def time_stamp():

    with open('timestamp.txt', 'r') as file:
        last_run = float(file.read())
        
    current_time = time.time()
    thirty_days = 2592000

    if (current_time - last_run) >= thirty_days:
        get_token()
        
        with open('timestamp.txt', 'w') as file:
            file.write(str(current_time))

def write_data():    
    with open('datalist.txt', 'w') as file:
        
        for id in chat_ids:
            file.write(str(id) + '\n')           

def write_notif():
    with open('notified.txt', 'w') as file:
        
        for id in notified:
            file.write(str(id) + '\n')

def retrieve_data():
    with open('datalist.txt', 'r') as file:
        lines = file.readlines()
        
        if lines:
            
            for line in lines:
                id = line.strip()
        
                try:
                    id = int(id)
                except ValueError:
                    pass
        
            chat_ids.add(id)
            
    with open('notified.txt', 'r') as file:
        lines = file.readlines()
        
        if lines:
            
            for line in lines:
                id = line.strip()
        
                try:
                    id = int(id)
                except ValueError:
                    pass
        
            notified.add(id)

def get_token():

    url = 'https://id.twitch.tv/oauth2/token'
    par = {
        'client_id': 'someclientIDhere',
        'client_secret': 'someclientsecrethere',
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, json=par)
    json_dic = json.loads(response.text)
    token = json_dic['access_token']

    with open('access.txt', 'w') as file:
        file.write(str(token))

def check_live():
    
    with open('access.txt', 'r') as file:
        token = file.read()
    
    url = 'https://api.twitch.tv/helix/streams'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Client-Id': 'someclientIDhere'
    }
    par = {
        'user_login': 'cuscitoergosum'
    }
    response = requests.get(url, headers=headers, params=par)
    is_online = json.loads(response.text)

    if is_online['data']:
        if is_online['data'][0]['user_login']:
            if is_online['data'][0]['user_login'] == 'cuscitoergosum':
                new_viewers = chat_ids - notified
        
                for id in new_viewers:
                    send_message(id, '&#127881 Il dottor Cùscito è in diretta!\n\nVisita il canale:\n\nhttps://twitch.tv/cuscitoergosum')
            
                notified.update(new_viewers)
                write_notif()
    else:
        notified.clear()
        write_notif()

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    param = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(url, json = param)
    
def send_message_nothumb(chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    param = {
        'chat_id': chat_id,
        'text': text,
        'disable_web_page_preview': True,
        'parse_mode': 'HTML'
    }
    requests.post(url, json = param)

def start_comm(update):
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        
        if 'text' in message:
            text = message['text']
    
            if '/start' in text and chat_id not in chat_ids:
                chat_ids.add(chat_id)
                write_data()
                send_message_nothumb(chat_id, 'Ciao e grazie per avermi attivato! &#10024\n\nSono un semplice bot che ti manderà un messaggio qui su Telegram ogni volta che il dottor Cùscito andrà in diretta sul <a href="https://twitch.tv/cuscitoergosum">suo canale Twitch</a>. Tu non devi far assolutamente nulla a parte rilassarti, ti arriverà una notifica al momento giusto. Se hai bisogno di più informazioni, puoi usare il comando /help.\n\nBene, per ora ti saluto e torno a girare dietro le quinte... &#128064')   
        
            elif '/start' in text and chat_id in chat_ids:
                send_message_nothumb(chat_id, 'Mi hai già attivato in precedenza! Non preoccuparti, sto lavorando nell\'ombra per te! &#128077')

def help_comm(update):
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        
        if 'text' in message:
            text = message['text']
        
            if '/help' in text:
                send_message_nothumb(chat_id, '<b>Descrizione</b> &#129302\n\nMi presento: sono un bot con l\'unica funzione di notificare i miei utenti con un messaggio su Telegram ogni volta che il dottor Cùscito va in diretta sul <a href="https://twitch.tv/cuscitoergosum">suo canale Twitch</a>, così che tu non possa perderti nemmeno una live.\n\n<b>Comandi</b> &#127918\n\n/start - Attiva il bot\n/help - Informazioni utili\n/stop - Disattiva il bot\n\n<b>Privacy</b> &#128373\n\nQuesto bot non conserva nessun dato personale, ad eccezione del codice ID della chat in cui è attivo, e comunque solo temporaneamente. Attivando il bot, si dà il proprio assenso alla conservazione temporanea di questo dato solo ed esclusivamente al fine di poter far funzionare correttamente il bot. Se un utente arresta il bot tramite il comando specifico o anche tramite l\'opzione offerta dall\'applicazione Telegram, il codice verrà automaticamente e permanentemente cancellato. In ogni caso questi dati non verranno mai condivisi con terze parti, né per fini analitici, né tantomeno commerciali.\n\n<b>Contatti</b> &#9997\n\nPer qualsiasi ulteriore informazione, suggerimenti, segnalazioni ed altro, scrivere a: cuscitoergobot@proton.me')

def stop_comm(update):
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        
        if 'text' in message:
            text = message['text']
        
            if '/stop' in text and chat_id in chat_ids:
                send_message_nothumb(chat_id, '&#9888 Stai procedendo con la disattivazione del bot.\n\nNon ti manderà più notifiche fino a nuova riattivazione, ma potrai comunque sempre lanciare il comando /help per informazioni.\n\n&#9989 /conferma')

def conf_comm(update):
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        
        if 'text' in message:
            text = message['text']
        
            if '/conferma' in text and chat_id in chat_ids: 
                send_message_nothumb(chat_id, 'Bot disattivato.\nTutti i dati sono stati cancellati.\n\nAlla prossima! &#128075')
                chat_ids.discard(chat_id)
                write_data()
                notified.discard(chat_id)
                write_notif()
                                 
def get_updates():
    last_update = None
    
    while True:
        time_stamp()
        url = f'https://api.telegram.org/bot{token}/getUpdates'
    
        if last_update:
            url += f'?offset={last_update + 1}'
    
        response = requests.get(url)
        json_dic = response.json()
    
        if json_dic['result']:
            
            for update in json_dic['result']:
                
                if 'my_chat_member' in update:
                    chat_member = update['my_chat_member']
                    
                    if 'new_chat_member' in chat_member and chat_member['new_chat_member']['status'] == 'kicked':
                        chat_ids.discard(chat_member['chat']['id'])
                        write_data()
                        notified.discard(chat_member['chat']['id'])
                        write_notif()
                
                stop_comm(update)
                conf_comm(update)
                help_comm(update)
                start_comm(update)
                last_update = update['update_id']
                            
        check_live()
        time.sleep(1.5)

retrieve_data()        
get_updates()