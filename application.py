from mend import application

# Version - 1.0.0
# Date - 12/13/20

def start_ngrok():
    from pyngrok import ngrok

    url = ngrok.connect(5000)
    print("\n * Tunnel URL:", url)

if __name__ == "__main__":
    #start_ngrok()
    application.run()
