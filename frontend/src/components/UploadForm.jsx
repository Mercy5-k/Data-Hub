import { useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import api from '../api'
import { useAuth } from '../context/AuthContext'

const UploadSchema = Yup.object().shape({
  filename: Yup.string().required('Filename is required'),
  file: Yup.mixed().test('fileRequired', 'File is required', function (value) {
    const { parent } = this
    // Allow either file upload or rely on filename-only for MVP
    if (parent?.file instanceof File) return true
    return !!parent.filename
  }),
  user_id: Yup.number().typeError('user_id must be a number').required('user_id required'),
})

export default function UploadForm({ onSuccess }) {
  const [error, setError] = useState('')
  const { user } = useAuth()

  return (
    <Formik
      initialValues={{ filename: '', description: '', tags: '', user_id: user?.id || 1, file: null }}
      validationSchema={UploadSchema}
      onSubmit={async (values, { setSubmitting, resetForm }) => {
        setError('')
        try {
          const form = new FormData()
          form.append('user_id', values.user_id)
          form.append('description', values.description)
          form.append('tags', values.tags)
          form.append('filename', values.filename)
          if (values.file) form.append('file', values.file)

          await api.post('/files', form, true)
          resetForm()
          onSuccess?.()
        } catch (e) {
          setError(e.message)
        } finally {
          setSubmitting(false)
        }
      }}
    >
      {({ isSubmitting, setFieldValue, values }) => (
        <Form className="card">
          <h3>Upload File</h3>
          {error && <div className="error">{error}</div>}
          <label>
            Filename
            <Field name="filename" placeholder="report.pdf" />
            <ErrorMessage className="error" component="div" name="filename" />
          </label>

          <label>
            Description
            <Field name="description" as="textarea" placeholder="Short description" />
          </label>

          <label>
            Tags (comma separated)
            <Field name="tags" placeholder="finance, q3" />
          </label>

          <label>
            User ID
            <Field name="user_id" />
            <ErrorMessage className="error" component="div" name="user_id" />
          </label>

          <label>
            File
            <input
              name="file"
              type="file"
              onChange={(e) => setFieldValue('file', e.currentTarget.files?.[0] || null)}
            />
            <ErrorMessage className="error" component="div" name="file" />
          </label>

          <button type="submit" disabled={isSubmitting}>Upload</button>
        </Form>
      )}
    </Formik>
  )
}
