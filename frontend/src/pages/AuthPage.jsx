import { useState } from 'react'
import RegisterForm from '../components/RegisterForm'
import LoginForm from '../components/LoginForm'

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true)

  return (
    <main className="auth_page">
      {isLogin ? <LoginForm /> : <RegisterForm />}

      <div className="auth_toggle">
        {isLogin ? (
          <p>
            Don’t have an account?{' '}
            <button
              type="button"
              className="auth_toggle__btn"
              onClick={() => setIsLogin(false)}
            >
              Sign up
            </button>
          </p>
        ) : (
          <p>
            Already have an account?{' '}
            <button
              type="button"
              className="auth_toggle__btn"
              onClick={() => setIsLogin(true)}
            >
              Log in
            </button>
          </p>
        )}
      </div>
    </main>
  )
}
