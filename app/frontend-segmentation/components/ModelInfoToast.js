"use client";

import React, { useEffect, useState } from 'react';

const ModelInfoToast = () => {

  const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1/segmentation';

  const [health, setHealth] = useState(null);
  const [info, setInfo] = useState(null);
  const [show, setShow] = useState(true);

  // Poll /health every 10s
  useEffect(() => {
    let interval;
    const fetchHealth = async () => {
      try {
        const res = await fetch(`${apiBaseUrl}/health`);
        const data = await res.json();
        setHealth(data);
      } catch {
        setHealth({ status: 'unreachable', model_loaded: false });
      }
    };
    fetchHealth();
    interval = setInterval(fetchHealth, 10000);
    return () => clearInterval(interval);
  }, [apiBaseUrl]);

  // Fetch /model/info once
  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const res = await fetch(`${apiBaseUrl}/model/info`);
        const data = await res.json();
        setInfo(data);
      } catch {
        setInfo(null);
      }
    };
    fetchInfo();
  }, [apiBaseUrl]);

const apiStatus =
  health?.status === 'healthy'
    ? '🟢 API connectée'
    : '🔴 API inaccessible';

  const modelStatus =
    health?.model_loaded === true
      ? '🟢 Modèle chargé'
      : '🔴 Modèle non chargé';

  const headerClass =
    health?.status === 'healthy'
      ? 'toast-header bg-success text-white'
      : 'toast-header bg-danger text-white';

  return (
    show && (
      <div
        className="toast show position-fixed"
        style={{
          bottom: 20,
          right: 20,
          maxWidth: 220,
          zIndex: 1055,
          pointerEvents: 'auto',
        }}
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
      >
        <div className={headerClass}>
          <strong className="me-auto">État du serveur</strong>
          <button
            type="button"
            className="btn-close"
            aria-label="Fermer"
            onClick={() => setShow(false)}
          ></button>
        </div>
        <div className="toast-body">
          <div>{apiStatus}</div>
          <div>{modelStatus}</div>
          {info && (
            <div className="mt-2 small">
              <div>
                <strong>Modèle :</strong> {info.model_name}
              </div>
              <div>
                <strong>TensorFlow :</strong> {info.tensorflow_version}
              </div>
              <div>
                <strong>Keras :</strong> {info.keras_version}
              </div>
            </div>
          )}
        </div>
      </div>
    )
  );
};

export default ModelInfoToast;