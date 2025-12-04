import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import './WelcomePage.css'

export default function WelcomePage() {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchUser() {
      try {
        const response = await fetch("/api/v1/users/me", {
          credentials: "include",
        })

        if (!response.ok) throw new Error("Not authenticated")

        const data = await response.json()
        setUser(data)
      } catch {
        navigate("/")
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [navigate])

  function handleLogout() {
    fetch("/api/v1/users/logout", { credentials: "include" })
      .finally(() => navigate("/"))
  }

  if (loading) return <p>Loading...</p>

  return (
    <div className="welcome-page">
      <nav className="welcome-page__navbar navbar">
        <div className="navbar__logo">Wallet</div>

        <ul className="navbar__tabs tabs">
          <li className="tabs__tab">Overview</li>
          <li className="tabs__tab">Wallets</li>
          <li className="tabs__tab">Analytics</li>
        </ul>

        <div className="navbar__user-info">
          <span className="navbar__user-name">
            {user?.name || "User"}
          </span>

          <button className="navbar__logout-btn" onClick={handleLogout}>
            Log Out
          </button>
        </div>
      </nav>

      <main className="welcome-page__content content">
        <div className="content__card card">
          <h2 className="card__title">Your Wallets</h2>
          <p className="card__text">
            Here will be a card with balance and transactions
          </p>

          <button className="card__button button">Add</button>
        </div>
      </main>
    </div>
  )
}
