// frontend/src/components/ShoppingList.jsx

function ShoppingList({ items, checkedItems, onItemToggle }) {
    return (
        <div className="card">
            <div className="card-header">
                <strong>Lista de Compras Generada</strong>
            </div>
            <ul className="list-group list-group-flush">
                {items.length > 0 ? ( // Usamos .map para transformar cada item en un elemento de la lista
                    items.map((item, index) => (
                        <li key={item.nombre} className="list-group-item fs-5">
                            <div className="form-check">
                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    id={`item-${index}`}
                                    checked={checkedItems[item.nombre] || false}
                                    onChange={() => onItemToggle(item.nombre)}
                                />
                                <label className="form-check-label d-flex justify-content-between w-100" htmlFor={`item-${index}`}>
                                    {item.nombre}
                                    <span className="badge bg-primary rounded-pill">{item.cantidad} {item.unidad}</span>
                                </label>
                            </div>
                        </li>
                    ))
                ) : (
                    <li className="list-group-item">No se encontraron ingredientes.</li>
                )}
            </ul>
        </div>
    );
}

export default ShoppingList;