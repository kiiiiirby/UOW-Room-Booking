# Python script at the top-level that defines the Flask application instance

from app import app

# run in debug
if __name__ == "__main__":
    app.run(debug=True)
    # os.chdir(r'C:\Users\T\OneDrive - SIM - Singapore Institute of Management\Dev material\Python\Projects\flask')
