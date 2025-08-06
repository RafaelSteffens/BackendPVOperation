from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, processes=True)
    # app.run(debug=False, use_reloader=False)
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, threaded=True, processes=True)