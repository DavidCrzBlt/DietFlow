function DailyPlan({ plan }) {
  if (!plan || plan.length === 0) {
    return (
      <div className="text-center">
        <p>Cargando el plan del día...</p>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-center mb-4">Plan de Hoy</h1>
      <div className="row">
        {plan.map((comida) => (
          // **IMPORTANTE**: Cada elemento en un .map() necesita un prop "key" único.
          // React lo usa internamente para optimizar el renderizado.
          // Piensa en ello como una "matrícula" para cada tarjeta.
          <div key={comida.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-header bg-primary text-white">
                {comida.momento_comida.charAt(0).toUpperCase() + comida.momento_comida.slice(1)}
              </div>
              <div className="card-body">
                <h5 className="card-title">{comida.receta.nombre}</h5>
                <ul className="list-group list-group-flush">
                  {/* ¡Podemos anidar .map() sin problemas! */}
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
          </div>
        ))}
      </div>
    </div>
  );
}

export default DailyPlan;