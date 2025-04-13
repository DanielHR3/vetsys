"""Modelo de base de datos para el módulo de inventario en VetSys."""

from database.db_connection import conectar


def agregar_articulo(
    nombre,
    marca,
    submarca,
    sku,
    codigo_barras,
    unidad,
    precio,
    categoria,
    subcategoria,
    descripcion,
    imagen,
):
    """Agrega un artículo nuevo al inventario."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        INSERT INTO inventario
        (nombre, marca, submarca, sku, codigo_barras, unidad, precio, categoria, subcategoria, descripcion, imagen)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            nombre,
            marca,
            submarca,
            sku,
            codigo_barras,
            unidad,
            precio,
            categoria,
            subcategoria,
            descripcion,
            imagen,
        ),
    )
    con.commit()
    con.close()


def obtener_inventario():
    """Obtiene todos los artículos del inventario."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        SELECT id, nombre, marca, submarca, sku, codigo_barras, unidad, precio, categoria, subcategoria, imagen
        FROM inventario
        ORDER BY nombre ASC
    """
    )
    resultados = cur.fetchall()
    con.close()
    return resultados


def actualizar_articulo(
    id_articulo,
    nombre,
    marca,
    submarca,
    sku,
    codigo_barras,
    unidad,
    precio,
    categoria,
    subcategoria,
    descripcion,
    imagen,
):
    """Actualiza un artículo existente en el inventario."""
    con = conectar()
    cur = con.cursor()
    cur.execute(
        """
        UPDATE inventario SET
        nombre = ?, marca = ?, submarca = ?, sku = ?, codigo_barras = ?, unidad = ?,
        precio = ?, categoria = ?, subcategoria = ?, descripcion = ?, imagen = ?
        WHERE id = ?
    """,
        (
            nombre,
            marca,
            submarca,
            sku,
            codigo_barras,
            unidad,
            precio,
            categoria,
            subcategoria,
            descripcion,
            imagen,
            id_articulo,
        ),
    )
    con.commit()
    con.close()


def eliminar_articulo(id_articulo):
    """Elimina un artículo del inventario por su ID."""
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM inventario WHERE id = ?", (id_articulo,))
    con.commit()
    con.close()
