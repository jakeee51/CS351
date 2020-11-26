from mend import application

# Version - 0.0.2
# Date - 11/25/20

def start_ngrok():
    from pyngrok import ngrok

    url = ngrok.connect(5000)
    print("\n * Tunnel URL:", url)

if __name__ == "__main__":
    #start_ngrok()
    application.run()
