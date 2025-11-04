// frontend/src/pages/WeekPlanPage.jsx
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { API } from '../api/endpoints';
import { ROUTES } from '../constants/routes';
import MealCard from '../components/MealCard';

function WeekPlanPage() {
    const [planSemana, setPlanSemana] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const diasOrdenados = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"];

    useEffect(() => {
        const fetchWeeklyPlan = async () => {
            try {
                const response = await fetch(API.getWeeklyPlanUrl());
                const data = await response.json();
                setPlanSemana(data);
            } catch (error) {
                console.error("Error al obtener el plan semanal:", error);
            } finally {
                setIsLoading(false);
            }
        };
        fetchWeeklyPlan();
    }, []);

    return (
        <div className="container-fluid mt-5">
            <h1 className="text-center mb-4">Plan Semanal</h1>

            {isLoading ? (
                <p className="text-center">Cargando...</p>
            ) : (
                <div className="d-flex flex-row flex-nowrap overflow-auto pb-3">
                    {diasOrdenados.map(dia => (
                        <div className="col-11 col-md-4 col-lg-3" key={dia} style={{ minWidth: "300px" }}>
                            <div className="card" style={{ marginRight: '15px' }}>
                                <div className="card-header text-center text-capitalize">
                                    <strong>{dia}</strong>
                                </div>
                                <div className="card-body">
                                    {planSemana[dia] && planSemana[dia].length > 0 ? (
                                        <div className="row row-cols-1 g-3">
                                            {planSemana[dia].map(comida => (
                                                <div className="col" key={comida.id}>
                                                    <MealCard comida={comida} />
                                                </div>

                                            ))}
                                        </div>

                                    ) : (
                                        <p className="text-muted">Día libre</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div className="text-center mt-4">
                <Link to={ROUTES.HOME} className="btn btn-secondary">Volver a Inicio</Link>
            </div>
            <br />

            
            
        </div>
    );
}

export default WeekPlanPage;