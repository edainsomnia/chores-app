# generate_keys.py
from pywebpush import webpush

try:
    # Versuche die Keys zu generieren
    private_key = webpush.generate_vapid_private_key()
    public_key = webpush.generate_vapid_public_key(private_key)

    print("-" * 30)
    print("DEINE VAPID KEYS:")
    print("-" * 30)
    print(f"VAPID_PRIVATE_KEY = '{private_key}'")
    print(f"VAPID_PUBLIC_KEY = '{public_key}'")
    print("-" * 30)
    print("\nKopiere diese Keys jetzt in deine app.py und index.html!")

except AttributeError:
    # Falls die obige Methode in deiner Version nicht existiert, 
    # nutzen wir einen alternativen Weg über die Cryptography-Bibliothek:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    import base64

    private_key_obj = ec.generate_private_key(ec.SECP256R1())
    public_key_obj = private_key_obj.public_key()

    # Formatiere die Keys für Web-Push
    private_key = base64.urlsafe_b64encode(
        private_key_obj.private_numbers().private_value.to_bytes(32, byteorder='big')
    ).decode('utf-8').strip('=')
    
    public_key = base64.urlsafe_b64encode(
        public_key_obj.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
    ).decode('utf-8').strip('=')

    print("-" * 30)
    print("VAPID_PRIVATE_KEY = '" + private_key + "'")
    print("VAPID_PUBLIC_KEY = '" + public_key + "'")
    print("-" * 30)