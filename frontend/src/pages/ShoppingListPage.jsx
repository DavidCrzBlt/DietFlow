// frontend/src/pages/ShoppingListPage.jsx
import { useState, useEffect } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import ShoppingList from '../components/ShoppingList';
import { ROUTES } from '../constants/routes';
import { API } from '../api/endpoints';

function ShoppingListPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { items = [], startDate = '', endDate = '' } = location.state || {};

    // Estado para los checkboxes. Inicializamos todos como marcados.
    const [checkedItems, setCheckedItems] = useState({});
    const [isSending, setIsSending] = useState(false);

    useEffect(() => {
        // Cuando los items se cargan, creamos un objeto donde cada item está 'true' (marcado)
        const initialCheckedState = items.reduce((acc, item) => {
            acc[item.nombre] = true;
            return acc;
        }, {});
        setCheckedItems(initialCheckedState);
    }, [items]); // Este efecto se ejecuta si 'items' cambia

    const handleItemToggle = (itemName) => {
        setCheckedItems(prev => ({
            ...prev,
            [itemName]: !prev[itemName]
        }));
    };

    const handleSendToTasks = async () => {
        setIsSending(true);

        // 1. Filtramos los items que están marcados
        const selectedItems = items.filter(item => checkedItems[item.nombre]);

        // 2. Creamos un objeto FormData para enviar los datos como un formulario
        const formData = new FormData();
        selectedItems.forEach(item => {
            const itemString = `${item.nombre}|${item.cantidad}|${item.unidad}`;
            formData.append('ingredientes', itemString);
        });

        try {
            // El endpoint del backend espera un POST con datos de formulario
            const response = await fetch(API.sendToTasksUrl(), {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                alert('¡Lista enviada a Google Tasks con éxito!');
                navigate(ROUTES.HOME); // Redirigimos al inicio
            } else {
                throw new Error('Falló el envío de la lista.');
            }
        } catch (error) {
            console.error("Error al enviar a Google Tasks:", error);
            alert('Hubo un problema al enviar la lista. Inténtalo de nuevo.');
        } finally {
            setIsSending(false);
        }
    };

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
                    <ShoppingList
                        items={items}
                        checkedItems={checkedItems}
                        onItemToggle={handleItemToggle}
                    />
                    <div className="d-grid gap-2 mt-4">
                        <button
                            className="btn btn-info btn-lg text-white"
                            onClick={handleSendToTasks}
                            disabled={isSending || items.length === 0}
                        >
                            {isSending ? 'Enviando...' : 'Enviar a Google Tasks'}
                        </button>
                        <Link to={ROUTES.HOME} className="btn btn-secondary">Cancelar</Link>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ShoppingListPage;