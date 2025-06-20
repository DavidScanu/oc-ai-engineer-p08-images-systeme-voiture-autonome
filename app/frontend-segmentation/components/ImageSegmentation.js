"use client";

import React, { useState, useRef } from 'react';


// Composant loader
const LoadingOverlay = ({ message }) => (
  <div className="position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center" 
       style={{ backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 9999 }}>
    <div className="card p-4 text-center">
      <div className="spinner-border text-primary mb-3" role="status" style={{ width: '3rem', height: '3rem' }}>
        <span className="visually-hidden">Chargement...</span>
      </div>
      <h5 className="card-title">Analyse en cours</h5>
      <p className="card-text">{message}</p>
      <div className="progress mt-2">
        <div className="progress-bar progress-bar-striped progress-bar-animated" 
             role="progressbar" style={{ width: '100%' }}></div>
      </div>
    </div>
  </div>
);

const ImageSegmentation = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);
  const [loadingProgress, setLoadingProgress] = useState('');

  // URL de votre API FastAPI (à adapter selon votre déploiement)
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1/segmentation';

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!selectedFile) {
      setError('Veuillez sélectionner une image');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingProgress('Préparation de l\'image...');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      setLoadingProgress('Envoi vers le serveur...');
      
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }

      setLoadingProgress('Traitement de la réponse...');
      const data = await response.json();
      
      setLoadingProgress('Finalisation...');
      setResult(data);
      
    } catch (err) {
      setError(`Erreur lors de la prédiction: ${err.message}`);
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
      setLoadingProgress('');
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setLoadingProgress(''); // Ajoutez cette ligne
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="container-fluid py-4">
      {loading && <LoadingOverlay message={loadingProgress} />}
      <div className="row">
        <div className="col-12">
          <h1 className="text-center mb-4">Segmentation Sémantique d'Images</h1>
          
          {/* Formulaire d'upload */}
          <div className="card mb-4">
            <div className="card-header">
              <h3 className="card-title mb-0">Sélectionnez une image</h3>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <input
                    ref={fileInputRef}
                    type="file"
                    className="form-control"
                    accept="image/*"
                    onChange={handleFileSelect}
                  />
                  <div className="form-text">
                    Formats supportés: JPEG, PNG, GIF (max 4096x4096px)
                  </div>
                </div>
                
                <div className="d-flex gap-2">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={!selectedFile || loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Analyse en cours...
                      </>
                    ) : (
                      'Analyser l\'image'
                    )}
                  </button>
                  
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={resetForm}
                  >
                    Réinitialiser
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Prévisualisation de l'image sélectionnée */}
          {previewUrl && !result && (
            <div className="card mb-4">
              <div className="card-header">
                <h4 className="card-title mb-0">Image sélectionnée</h4>
              </div>
              <div className="card-body text-center">
                <img
                  src={previewUrl}
                  alt="Aperçu"
                  className="img-fluid"
                  style={{ maxHeight: '400px' }}
                />
              </div>
            </div>
          )}

          {/* Affichage des erreurs */}
          {error && (
            <div className="alert alert-danger" role="alert">
              <i className="bi bi-exclamation-triangle-fill me-2"></i>
              {error}
            </div>
          )}

          {/* Résultats de la segmentation */}
          {result && (
            <div className="row">
              {/* Visualisation overlay */}
              <div className="col-lg-8 mb-4">
                <div className="card">
                  <div className="card-header">
                    <h4 className="card-title mb-0">Résultat de la segmentation</h4>
                  </div>
                  <div className="card-body text-center">
                    <img
                      src={result.images.overlay}
                      alt="Segmentation overlay"
                      className="img-fluid"
                      style={{ maxWidth: '100%', height: 'auto' }}
                    />
                  </div>
                </div>
              </div>

              {/* Statistiques */}
              <div className="col-lg-4 mb-4">
                <div className="card">
                  <div className="card-header">
                    <h4 className="card-title mb-0">Statistiques</h4>
                  </div>
                  <div className="card-body">
                    <div className="mb-3">
                      <strong>Classe dominante:</strong><br />
                      <span className="badge bg-primary fs-6">
                        {result.dominant_class} ({result.dominant_class_percentage.toFixed(1)}%)
                      </span>
                    </div>
                    
                    <div className="mb-3">
                      <strong>Taille de l'image:</strong><br />
                      {result.image_size[0]} × {result.image_size[1]} pixels
                    </div>

                    <div>
                      <strong>Distribution des classes:</strong>
                      <div className="mt-2">
                        {result.class_statistics.slice(0, 5).map((stat, index) => (
                          <div key={stat.class_id} className="d-flex justify-content-between mb-1">
                            <span className="text-truncate me-2">{stat.class_name}:</span>
                            <span className="fw-bold">{stat.percentage.toFixed(1)}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Comparaison côte à côte */}
              <div className="col-12 mb-4">
                <div className="card">
                  <div className="card-header">
                    <h4 className="card-title mb-0">Comparaison détaillée</h4>
                  </div>
                  <div className="card-body text-center">
                    <img
                      src={result.images.side_by_side}
                      alt="Comparaison originale vs prédiction"
                      className="img-fluid"
                      style={{ maxWidth: '100%', height: 'auto' }}
                    />
                  </div>
                </div>
              </div>

              {/* Images individuelles */}
              <div className="col-12">
                <div className="card">
                  <div className="card-header">
                    <h4 className="card-title mb-0">Images individuelles</h4>
                  </div>
                  <div className="card-body">
                    <div className="row">
                      <div className="col-md-4 mb-3">
                        <h6 className="text-center">Image originale</h6>
                        <img
                          src={result.images.original}
                          alt="Image originale"
                          className="img-fluid border"
                        />
                      </div>
                      <div className="col-md-4 mb-3">
                        <h6 className="text-center">Masque de segmentation</h6>
                        <img
                          src={result.images.prediction_mask}
                          alt="Masque de prédiction"
                          className="img-fluid border"
                        />
                      </div>
                      <div className="col-md-4 mb-3">
                        <h6 className="text-center">Superposition</h6>
                        <img
                          src={result.images.overlay}
                          alt="Superposition"
                          className="img-fluid border"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageSegmentation;