// Composant loader
const LoadingOverlay = ({ message }) => (
  <div className="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
       style={{ backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 9999 }}>
    <div className="card p-4 text-center">
        <div className="d-flex justify-content-center">
            <div className="spinner-border text-primary mb-3 d-flex" role="status" style={{ width: '3rem', height: '3rem' }}>
                <span className="visually-hidden">Chargement...</span>
            </div>
        </div>
      <h5 className="card-title">Analyse en cours</h5>
      <p className="card-text mb-0">{message}</p>
      <div className="progress mt-1">
        <div className="progress-bar progress-bar-striped progress-bar-animated" 
             role="progressbar" style={{ width: '100%' }}></div>
      </div>
    </div>
  </div>
);

export default LoadingOverlay;