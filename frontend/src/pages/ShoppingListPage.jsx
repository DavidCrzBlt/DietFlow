// frontend/src/pages/ShoppingListPage.jsx
import { useLocation, Link } from 'react-router-dom';
import { ROUTES } from '../constants/routes';

function ShoppingListPage() {
    const location = useLocation();
    const { items = [], startDate = '', endDate = '' } = location.state || {};
    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-lg-8">
                    <div className="card text-center mb-4">
                        <div className="card-body">
                            <h5 className="card-title">Rango de Fechas Seleccionado</h5>
                            <p className="card-text fs-5">
                                Desde el <strong>{startDate}</strong> hasta el <strong>{endDate}</strong>
                            </p>
                        </div>
                    </div>
                    <div className="card">
                        <div className="card-header">
                            <strong>Lista de Compras Generada</strong>
                        </div>
                        <ul className="list-group list-group-flush">
                            {items.length > 0 ? (
                                items.map((item) => (
                                    <li key={item.nombre} className="list-group-item d-flex justify-content-between align-items-center">
                                        {item.nombre}
                                        <span className="badge bg-primary rounded-pill">
                                            {item.cantidad} {item.unidad}
                                        </span>
                                    </li>
                                ))
                            ) : (
                                <li className="list-group-item">No se encontraron ingredientes.</li>
                            )}
                        </ul>
                    </div>
                    <div className="text-center mt-4">
                        <Link to={ROUTES.HOME} className="btn btn-secondary">Volver</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ShoppingListPage;