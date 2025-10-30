// frontend/src/pages/HomePage.jsx
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ROUTES } from '../constants/routes';
import { API } from '../api/endpoints';


function ShoppingListForm({ onGenerate, isLoading }) {

    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();

        onGenerate(startDate, endDate);
    };


    return (
        <div className="card mb-5">
            <div className="card-header">
                <strong>Generar Lista de Compras</strong>
            </div>
            <div className="card-body">
                <form className="row g-3 align-items-center" onSubmit={handleSubmit}>
                    <div className="col-md-5">
                        <label htmlFor="dia_inicio" className="form-label">Fecha de Inicio:</label>
                        <input type="date" id="dia_inicio" className="form-control" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                    </div>
                    <div className="col-md-5">
                        <label htmlFor="dia_fin" className="form-label">Fecha de Fin:</label>
                        <input type="date" id="dia_fin" className="form-control" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
                    </div>
                    <div className="col-md-2 d-grid align-self-end">
                        <button type="submit" className="btn btn-primary">Generar</button>
                    </div>
                </form>
            </div>
        </div>
    );
}


function DailyPlan() {
    return (
        <div>
            <h1 className="text-center mb-4">Plan de Hoy</h1>
            <div className="row">
                {/* Tarjeta de Desayuno (datos "quemados") */}
                <div className="col-md-6 col-lg-4 mb-4">
                    <div className="card h-100">
                        <div className="card-header bg-primary text-white">Desayuno</div>
                        <div className="card-body">
                            <h5 className="card-title">OMELETE (L/J)</h5>
                        </div>
                    </div>
                </div>

                {/* Tarjeta de Refrigerio (datos "quemados") */}
                <div className="col-md-6 col-lg-4 mb-4">
                    <div className="card h-100">
                        <div className="card-header bg-primary text-white">Refrigerio</div>
                        <div className="card-body">
                            <h5 className="card-title">REFRIGERIO (L/J)</h5>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}


function HomePage() {
    const navigate = useNavigate(); // Hook para controlar la navegación
    const [planDelDia, setPlanDelDia] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerateList = async (startDate, endDate) => {
        setIsLoading(true);
        const apiUrl = API.getShoppingListUrl(startDate, endDate);
        try {
            const response = await fetch(apiUrl);
            const data = await response.json();
            // En lugar de guardar en el estado, navegamos a la nueva ruta pasándole los datos
            navigate(ROUTES.SHOPPING_LIST, { 
                state: { 
                    items: data,
                    startDate: startDate,
                    endDate: endDate
                } 
            });
        } catch (error) {
            console.error("Error al generar la lista:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-lg-10">
                    <ShoppingListForm onGenerate={handleGenerateList} isLoading={isLoading} />
                    <hr className="my-5" />
                    <DailyPlan plan={planDelDia} /> 
                </div>
            </div>
        </div>
    );
}

export default HomePage;