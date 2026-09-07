import app 
@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    