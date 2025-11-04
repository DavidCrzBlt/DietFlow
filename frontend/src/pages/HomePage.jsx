import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; 
import { ROUTES } from '../constants/routes';
import { API } from '../api/endpoints';

import DailyPlan from '../components/DailyPlan';
import ShoppingListForm from '../components/ShoppingListForm';

function HomePage() {
    const navigate = useNavigate(); // Hook para controlar la navegación
    const [planDelDia, setPlanDelDia] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isSendingPlan, setIsSendingPlan] = useState(false);

    useEffect(() => {
        const fetchPlan = async () => {
            try {
                const response = await fetch(API.getDailyPlanUrl());
                const data = await response.json();
                setPlanDelDia(data);
            } catch (error) {
                console.error("Error al obtener el plan del día:", error);
            }
        };
        fetchPlan();
    }, []); // El [] vacío asegura que solo se ejecute una vez
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

    const handleSendPlanToTasks = async () => {
        setIsSendingPlan(true);
        try {
            const response = await fetch(API.sendPlanToTasks(), {
                method: 'POST',
            });
            const data = await response.json();
            alert(data.message);
        } catch (error) {
            console.error("Error al enviar el plan a Tasks:", error);
            alert("Error al enviar el plan.");
        } finally {
            setIsSendingPlan(false);
        }
    };
    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-lg-10">
                    <ShoppingListForm onGenerate={handleGenerateList} isLoading={isLoading} />
                    <div className="text-center my-4">
                        <Link to={ROUTES.WEEK_PLAN} className="btn btn-outline-primary btn-lg">
                            Ver Plan Semanal Completo
                        </Link>
                    </div>
                    <hr className="my-5" />
                    <div className="card mt-4">
                        <div className="card-body text-center">
                            <h5 className="card-title">Plan semanal en Google Tasks</h5>
                            <p className="card-text">Envía las comidas de toda la semana a tus listas de tareas con recordatorios.</p>
                            <button
                                className="btn btn-primary text-white"
                                onClick={handleSendPlanToTasks}
                                disabled={isSendingPlan}
                            >
                                {isSendingPlan ? "Enviando..." : "Enviar Plan Semanal a Tasks"}
                            </button>
                        </div>
                    </div>
                    <hr className="my-5" />
                    <DailyPlan plan={planDelDia} />
                </div>
            </div>
        </div>
    );
}

export default HomePage;