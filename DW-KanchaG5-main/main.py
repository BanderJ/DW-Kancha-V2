from flask import Flask,render_template,request,jsonify
from controlador_productos import insertProduct,listarProductos,updateProducto,deleteProducto

app = Flask(__name__)

@app.get('/')
def inicio():
    return render_template("index.html")

@app.get('/productos')
def seccionProductos():
    return render_template("SeccionProductos.html")

if __name__ == "__main__":
    app.run(debug=True)