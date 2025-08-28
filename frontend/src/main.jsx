import React, { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';
import { createBrowserRouter, RouterProvider } from 'react-router';
import WelcomePage from './pages/WelcomePage';

const router = createBrowserRouter([
  { path: "/", element: <App /> },
  { path: "/welcome", element: <WelcomePage /> },
]);

const rootElement = document.getElementById('root');
const root = createRoot(rootElement);

root.render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
