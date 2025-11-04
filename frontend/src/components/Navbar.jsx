import { Link } from 'react-router-dom';
import { ROUTES } from '../constants/routes';

function Navbar() {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <div className="container-fluid">

                <Link className="navbar-brand d-flex align-items-center" to={ROUTES.HOME}>
                    {/* Vite buscará automáticamente esta imagen en la carpeta 'public' 
            que crearemos en el siguiente paso.
          */}
                    <img
                        src="/vite.svg"
                        alt="DietFlow Logo"
                        width="30"
                        height="30"
                        className="d-inline-block align-text-top me-2"
                    />
                    DietFlow
                </Link>

                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to={ROUTES.HOME}>Inicio</Link>
                        </li>
                        <li className="nav-item">
                            <Link className="nav-link" to={ROUTES.WEEK_PLAN}>Plan Semanal</Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;