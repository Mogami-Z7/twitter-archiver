import os
import requests
import feedparser

# Recuperamos los secrets que configuraste en GitHub
webhook_url = os.environ.get('WEBHOOK_URL')
rss_url = os.environ.get('RSS_URL')
supabase_key = os.environ.get('SUPABASE_ANON_KEY')  # ← NUEVA LÍNEA

def check_rss():
    print(f"Consultando RSS...")
    feed = feedparser.parse(rss_url)
    
    if not feed.entries:
        print("El feed está vacío o falló la conexión a RSSHub.")
        return
    
    # Extraemos el ID del tuit más reciente desde el enlace
    latest_entry = feed.entries[0]
    tweet_id = latest_entry.link.split('/')[-1]
    
    print(f"Último Tweet ID detectado: {tweet_id}")
    
    # Preparamos el paquete para la Edge Function
    payload = {
        "tweet_id": tweet_id,
        "origen": "Via B (GitHub Actions)"
    }
    
    # ← AGREGAMOS LOS HEADERS DE AUTENTICACIÓN
    headers = {
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "apikey": supabase_key  # Supabase también espera este header
    }
    
    # Disparamos el Webhook CON AUTENTICACIÓN
    response = requests.post(webhook_url, json=payload, headers=headers)
    
    print(f"Estado HTTP de Supabase: {response.status_code}")
    print(f"Respuesta del servidor: {response.text}")

if __name__ == "__main__":
    check_rss()
