from app import app
from raven.contrib.flask import Sentry
sentry = Sentry(app, dsn='https://e7efa4e39f6d4d69956fb1577d6b5fda:8d9feb63cc0840169c42fc01e7d25d20@sentry.io/235185')
#app.run(host='0.0.0.0', port=5000)
app.run(debug=True,port=5007)