import React from 'react';
import { Activity } from 'lucide-react';
import ComplaintForm from './ComplaintForm';
import AIPanel from './AIPanel';

const Layout = () => {
  return (
    <>
      <nav className="app-navbar">
        <div className="app-logo">
          <Activity size={24} />
          ComplaiNet
        </div>
      </nav>
      
      <main className="app-container">
        <section className="panel">
          <header className="panel-header">
            <h2>Log Customer Complaint</h2>
          </header>
          <div className="form-container">
            <ComplaintForm />
          </div>
        </section>
        
        <section className="panel">
          <header className="panel-header">
            <h2>AI Assistant</h2>
          </header>
          <AIPanel />
        </section>
      </main>
    </>
  );
};

export default Layout;
