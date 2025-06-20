import React, { useEffect, useState } from 'react';

const ModelInfo = ({ apiUrl }) => {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInfo = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`Erreur API: ${response.status}`);
        }
        const data = await response.json();
        setInfo(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInfo();
  }, [apiUrl]);

  if (loading) return <div>Chargement des infos du modèle...</div>;
  if (error) return <div className="alert alert-warning">Erreur: {error}</div>;
  if (!info) return null;

  return (
    <div className="mb-3">
      <strong>Modèle :</strong> {info.model_name}<br />
      <strong>TensorFlow :</strong> {info.tensorflow_version}<br />
      <strong>Keras :</strong> {info.keras_version}
    </div>
  );
};

export default ModelInfo;