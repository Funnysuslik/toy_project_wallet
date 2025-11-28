import { useState } from 'react'
import { useNavigate } from 'react-router'
import './AuthForms.css'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()

    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    try {
      const response = await fetch("/api/v1/users/login/access-token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        credentials: "include",
        body: formData.toString(),
      })

      if (!response.ok) {
        throw new Error("Login failed")
      }

      setError("")
      navigate("/welcome")
    } catch (err) {
      setError("Invalid email or password")
    }
  }

  function handleGoogleLogin() {
    const redirectUri = `${window.location.origin}/api/v1/users/login/google/callback`

    const googleUrl =
      `https://accounts.google.com/o/oauth2/v2/auth?` +
      `client_id=797302245130-52rns8fdfr66p2flan3id62p59c8v362.apps.googleusercontent.com` +
      `&redirect_uri=${redirectUri}` +
      `&response_type=code` +
      `&scope=openid%20email%20profile` +
      `&prompt=select_account` +
      `&access_type=offline`

    window.location.href = googleUrl
  }

  return (
    <section className="login_wrapper">
      <div className="login_form">
        <h1 className="login_heading">Welcome!</h1>
        <form className="form" aria-label="Log in form" onSubmit={handleSubmit}>
          <label className="form__label">
            <span>E-mail</span>
            <input
              type="email"
              name="email"
              className="form__input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </label>
          <label className="form__label">
            <span>Password</span>
            <input
              type="password"
              name="password"
              className="form__input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </label>

          <button type="submit" className="form__submit">
            Log In
          </button>

          <button type="button" className="google_btn" onClick={handleGoogleLogin}>
            Continue with Google
          </button>

          {error && (
            <p className="form__error" role="alert">
              {error}
            </p>
          )}
        </form>
      </div>
    </section>
  )
}
