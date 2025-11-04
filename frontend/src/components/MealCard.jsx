function MealCard({ comida }) {
  if (!comida) return null;

  return (
    <div className="card">
      <div className="card-header bg-primary text-white">
        {comida.momento_comida.charAt(0).toUpperCase() + comida.momento_comida.slice(1)}
      </div>
      <div className="card-body">
        <h5 className="card-title">{comida.receta.nombre}</h5>
        <ul className="list-group list-group-flush">
          {comida.receta.ingredientes.map((item) => (
            <li key={item.ingrediente.id} className="list-group-item d-flex justify-content-between align-items-center">
              {item.ingrediente.nombre}
              <span className="badge bg-secondary rounded-pill">
                {item.cantidad} {item.ingrediente.unidad}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default MealCard;