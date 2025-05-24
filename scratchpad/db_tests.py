@app.route('/testdb')
def test_db():
    try:
        db.create_all()  # Ensures tables are created
        return "Database connection successful!", 200
    except Exception as e:
        return str(e), 500