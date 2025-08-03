
import React, { useState, useEffect } from 'react';
import './App.css';

const ReadingView = ({ session, onNavigate, progress }) => {
  if (!session) {
    return <div className="container text-center mt-5">Carregando...</div>;
  }

  return (
    <div className="container mt-4">
      <div className="card shadow-sm">
        <div className="card-header text-center bg-primary text-white">
          <h3>{session.title}</h3>
        </div>
        <div className="card-body" style={{ maxHeight: '60vh', overflowY: 'auto' }}>
          {session.content.map((item, index) => {
            if (item.type === 'p') {
              return <p key={index} className="lead">{item.content}</p>;
            }
            return null;
          })}
        </div>
        <div className="card-footer d-flex justify-content-between align-items-center">
          <button className="btn btn-secondary" onClick={() => onNavigate('prev')}>Anterior</button>
          <span className="text-muted">{progress}</span>
          <button className="btn btn-secondary" onClick={() => onNavigate('next')}>Próximo</button>
        </div>
      </div>
    </div>
  );
};

const App = () => {
  const [sessions, setSessions] = useState([]);
  const [currentSessionIndex, setCurrentSessionIndex] = useState(0);
  const [language, setLanguage] = useState('pt-BR'); // pt-BR ou en

  useEffect(() => {
    fetch(`/data/livro_${language}.json`)
      .then(response => response.json())
      .then(data => {
        const allParagraphs = data.flatMap(part => 
          part.chapters.flatMap(chapter => 
            chapter.content.filter(item => item.type === 'p').map(p => ({...p, chapterTitle: chapter.chapter_title, partTitle: part.part_title}))
          )
        );

        const readingSessions = [];
        let currentSession = { title: '', content: [] };
        let wordCount = 0;

        allParagraphs.forEach(p => {
          if (wordCount > 250 || !currentSession.title) {
            if(currentSession.content.length > 0) readingSessions.push(currentSession);
            currentSession = { title: `${p.partTitle} - ${p.chapterTitle}`, content: [p] };
            wordCount = p.word_count;
          } else {
            currentSession.content.push(p);
            wordCount += p.word_count;
          }
        });
        if(currentSession.content.length > 0) readingSessions.push(currentSession);
        
        setSessions(readingSessions);
        setCurrentSessionIndex(0); // Reseta para o início ao mudar o idioma
      }).catch(error => console.error("Failed to load book data:", error));
  }, [language]);

  const handleNavigate = (direction) => {
    if (direction === 'next' && currentSessionIndex < sessions.length - 1) {
      setCurrentSessionIndex(currentSessionIndex + 1);
    } else if (direction === 'prev' && currentSessionIndex > 0) {
      setCurrentSessionIndex(currentSessionIndex - 1);
    }
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'ArrowLeft') {
        handleNavigate('prev');
      } else if (event.key === 'ArrowRight') {
        handleNavigate('next');
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [currentSessionIndex, sessions.length]);

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  }

  return (
    <div className="App bg-light min-vh-100">
      <nav className="navbar navbar-dark bg-dark">
        <div className="container-fluid">
          <span className="navbar-brand mb-0 h1">Leitura Devota</span>
          <select className="form-select w-auto" value={language} onChange={handleLanguageChange}>
            <option value="pt-BR">Português (BR)</option>
            <option value="en">English (US)</option>
          </select>
        </div>
      </nav>
      <ReadingView 
        session={sessions[currentSessionIndex]} 
        onNavigate={handleNavigate} 
        progress={`Dia ${currentSessionIndex + 1} de ${sessions.length}`}
      />
    </div>
  );
}

export default App;
