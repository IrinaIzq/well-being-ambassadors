from flask import Flask

from app.config import Config


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    @app.route("/")
    def index():
        return """
        <html>

        <head>

        <title>Wellbeing Quest</title>

        <style>

        body{

            background:#08111F;

            color:white;

            display:flex;

            justify-content:center;

            align-items:center;

            height:100vh;

            font-family:Arial;

            flex-direction:column;

        }

        h1{

            font-size:58px;

            margin-bottom:10px;

        }

        p{

            color:#94A3B8;

            font-size:20px;

        }

        </style>

        </head>

        <body>

        <h1>🌱 Wellbeing Quest</h1>

        <p>Well-being Ambassadors Programme</p>

        </body>

        </html>
        """

    return app