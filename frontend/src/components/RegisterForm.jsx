import { useState } from 'react'
import { useNavigate } from 'react-router'
import './AuthForms.css'

export default function RegisterForm() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [passwordCheck, setPasswordCheck] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()

    if (password !== passwordCheck) {
      setError("Passwords do not match")
      return
    }

    try {
      const response = await fetch("/api/v1/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          full_name: name,
          email,
          password,
          password_check: passwordCheck,
        }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || "Registration failed")
      }

      setError("")
      console.log("Registration successful")
      navigate("/welcome")
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <section className="signup_wrapper">
      <div className="signup_form">
        <h1 className="signup_heading">Create your account</h1>
        <form className="form" aria-label="Sign up form" onSubmit={handleSubmit}>
          <label className="form__label">
            <span>Name</span>
            <input
              type="text"
              name="name"
              className="form__input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoComplete="name"
              required
            />
          </label>
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
              autoComplete="new-password"
              required
            />
          </label>
          <label className="form__label">
            <span>Confirm Password</span>
            <input
              type="password"
              name="passwordCheck"
              className="form__input"
              value={passwordCheck}
              onChange={(e) => setPasswordCheck(e.target.value)}
              autoComplete="new-password"
              required
            />
          </label>
          <button type="submit" className="form__submit">
            Sign Up
          </button>
          <button type="button" className="google_btn">
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
