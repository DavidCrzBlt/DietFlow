import { useState, useEffect } from 'react';

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

export default ShoppingListForm;