"""
Run app
"""

if __name__ == '__main__':
    from cloudproxygateway.views import app
    app.run(host='127.0.0.1', port=5000)
