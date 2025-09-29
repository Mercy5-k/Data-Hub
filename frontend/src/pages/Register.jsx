import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { useNavigate, Link } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '../context/AuthContext'

const RegisterSchema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  password: Yup.string().min(4, 'Min 4 characters').required('Password is required'),
})

export default function Register() {
  const { register } = useAuth()
  const nav = useNavigate()
  const [error, setError] = useState('')

  return (
    <div className="page">
      <div className="card">
        <h3>Register</h3>
        {error && <div className="error">{error}</div>}
        <Formik
          initialValues={{ username: '', password: '' }}
          validationSchema={RegisterSchema}
          onSubmit={async (values, { setSubmitting }) => {
            setError('')
            try {
              await register(values.username, values.password)
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
              <button type="submit" disabled={isSubmitting}>Create account</button>
            </Form>
          )}
        </Formik>
        <p style={{ marginTop: 12 }}>
          Have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  )
}
