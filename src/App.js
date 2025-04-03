import React from 'react';
import './App.css';
import D90calculator from './components/D90calculator';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>D90 Value Calculator</h1>
        <D90calculator />
      </header>
    </div>
  );
}

export default App;
