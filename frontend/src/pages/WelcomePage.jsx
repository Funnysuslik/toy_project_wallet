import { useNavigate } from 'react-router'
import './WelcomePage.css'

export default function WelcomePage() {
  const navigate = useNavigate()

  function handleLogout() {
    navigate('/')
  }

  return (
    <div className="welcome-page">
      <nav className="welcome-page__navbar navbar">
        <div className="navbar__logo">Wallet</div>
        <ul className="navbar__tabs tabs">
          <li className="tabs__tab">Overview</li>
          <li className="tabs__tab">Accounts</li>
          <li className="tabs__tab">Analytics</li>
        </ul>
        <button className="navbar__logout-btn" onClick={handleLogout}>
          Log Out
        </button>
      </nav>

      <main className="welcome-page__content content">
        <div className="content__card card">
          <h2 className="card__title">Your Accounts</h2>
          <p className="card__text">Here will be a card with balance and transactions</p>
          <button className="card__button button">Add</button>
        </div>
      </main>
    </div>
  )
}
