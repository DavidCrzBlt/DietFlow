// frontend/src/components/DailyPlan.jsx
import MealCard from './MealCard'; // <-- Importamos nuestro nuevo componente

function DailyPlan({ plan, showTitle = true }) {
  if (!plan || plan.length === 0) {
    return (
      <div className="text-center">
        {showTitle && <p>Cargando el plan del día...</p>}
      </div>
    );
  }

  return (
    <div>
      {showTitle && <h1 className="text-center mb-4">Plan de Hoy</h1>}
      <div className="row">
        {plan.map((comida) => (
          <div key={comida.id} className="col-md-6 col-lg-4 mb-4">
            <MealCard comida={comida} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default DailyPlan;