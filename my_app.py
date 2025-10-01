from app import create_app
import os
from flask_migrate import upgrade


app = create_app(os.getenv("FLASK_CONFIG") or "default")
print("fff")
print(os.getenv("FLASK_CONFIG"))


@app.cli.command("deploy")
def deploy():
    #Migrar base de datos a la ultima versión
    upgrade()


if __name__=="__main__":
    print("jojojo")
    app.run(
        use_debugger = False, use_reloader = False, passthrough_errors = True, host='0.0.0.0', port = 5000
        )