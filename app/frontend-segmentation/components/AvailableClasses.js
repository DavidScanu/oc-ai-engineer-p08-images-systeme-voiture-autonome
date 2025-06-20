import React, { useEffect, useState } from 'react';

const AvailableClasses = ({ apiUrl }) => {
  const [classNames, setClassNames] = useState([]);
  const [classColors, setClassColors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`Erreur API: ${response.status}`);
        }
        const data = await response.json();
        setClassNames(data.class_names || []);
        setClassColors(data.class_colors || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchClasses();
  }, [apiUrl]);

  if (loading) return <div>Chargement des classes...</div>;
  if (error) return <div className="alert alert-warning">Erreur: {error}</div>;
  if (!classNames.length) return <div>Aucune classe disponible.</div>;

  return (
    <div className="mb-3">
      <strong>Classes disponibles :</strong>
      <ul className="list-inline mb-0">
        {classNames.map((className, idx) => {
          const color = classColors[idx]
            ? `rgb(${classColors[idx].join(',')})`
            : '#6c757d'; // fallback Bootstrap secondary
          const textColor =
            classColors[idx] && (classColors[idx][0]*0.299 + classColors[idx][1]*0.587 + classColors[idx][2]*0.114) < 186
              ? '#fff'
              : '#000';
          return (
            <li
              key={idx}
              className="list-inline-item badge me-1"
              style={{
                backgroundColor: color,
                color: textColor,
                fontWeight: 500,
                fontSize: '1em',
              }}
            >
              {className}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default AvailableClasses;