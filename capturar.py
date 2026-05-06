import feedparser
import requests
import os

WEBHOOK_URL = os.environ['WEBHOOK_URL']
RSS_URL     = os.environ['RSS_URL']
ANON_KEY    = os.environ['SUPABASE_ANON_KEY']

headers = {
    'Content-Type': 'application/json',
    'apikey': ANON_KEY
}

feed = feedparser.parse(RSS_URL)

if not feed.entries:
    print("No se pudo leer el feed o está vacío.")
else:
    for entry in feed.entries:
        # Extraer el ID del tweet desde la URL
        tweet_id = entry.link.split('/')[-1].split('#')[0]

        # Enviar al webhook
        try:
            response = requests.post(WEBHOOK_URL, json={
                'tweet_id':          tweet_id,
                'origen':            'B',
                'fecha_publicacion': entry.get('published', '')
            }, headers=headers, timeout=30)

            result = response.json()

            if result.get('status') == 'captured':
                print(f"Nuevo tweet guardado: {tweet_id}")
            elif result.get('status') == 'already_captured':
                print(f"Ya existía, ignorado: {tweet_id}")
            else:
                print(f"Respuesta inesperada en {tweet_id}: {result}")

        except Exception as e:
            print(f"Error procesando {tweet_id}: {e}")
