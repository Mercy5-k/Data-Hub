import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { useNavigate, Link } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'

const LoginSchema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  password: Yup.string().required('Password is required'),
})

export default function Login() {
  const { login } = useAuth()
  const nav = useNavigate()
  const [error, setError] = useState('')

  return (
    <div className="page">
      <div className="card">
        <h3>Login</h3>
        {error && <div className="error">{error}</div>}
        <Formik
          initialValues={{ username: '', password: '' }}
          validationSchema={LoginSchema}
          onSubmit={async (values, { setSubmitting }) => {
            setError('')
            try {
              await login(values.username, values.password)
              nav('/')
            } catch (e) {
              setError(e.message)
            } finally {
              setSubmitting(false)
            }
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <label>
                Username
                <Field name="username" />
                <ErrorMessage className="error" component="div" name="username" />
              </label>
              <label>
                Password
                <Field name="password" type="password" />
                <ErrorMessage className="error" component="div" name="password" />
              </label>
              <button type="submit" disabled={isSubmitting}>Login</button>
            </Form>
          )}
        </Formik>
        <p style={{ marginTop: 12 }}>
          No account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
  )
}
