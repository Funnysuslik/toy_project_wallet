import { useState } from 'react'
import './AuthForms.css'

export default function RegisterForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()

    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        throw new Error("Registration failed")
      }

      setError("")
      console.log("Registration successful")
    } catch (error) {
      setError("Email is already in use")
    }
  }

  return (
    <section className="signup_wrapper">
      <div className="signup_form">
        <h1 className="signup_heading">Create your account</h1>
        <form className="form" aria-label="Sign up form" onSubmit={handleSubmit}>
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
            Sign Up
          </button>
          {error && (
            <p className="form__error" role="alert">
              {error}
            </p>
          )}
        </form>
      </div>
    </section>
  );
}
