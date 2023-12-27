from app import SSApp

if __name__ == "__main__":
    app = SSApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print()
        exit()
