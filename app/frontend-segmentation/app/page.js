// pages/index.js
import Head from 'next/head';
import ImageSegmentation from '@/components/ImageSegmentation';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@/styles/globals.css';

export default function Home() {
  return (
    <div className ="container">
      <Head>
        <title>Segmentation d'Images - Future Vision Transport</title>
        <meta name="description" content="Application de segmentation sémantique d'images pour véhicules autonomes" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <ImageSegmentation />
      </main>
      <footer className="text-center mt-5">
        <p>&copy; {new Date().getFullYear()} Future Vision Transport. Tous droits réservés.</p>
        <p className="small">
          Projet développé par <a href="https://www.linkedin.com/in/davidscanu14/" target="_blank" rel="noopener noreferrer">David Scanu</a> dans le cadre du parcours <a href="https://openclassrooms.com/fr/paths/795-ai-engineer" target="_blank" rel="noopener noreferrer">AI Engineer</a> d'OpenClassrooms : <strong>Projet 8 - Traitez les images pour le système embarqué d'une voiture autonome</strong>.
        </p>
      </footer>
    </div>
  );
}