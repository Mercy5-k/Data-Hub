import { useEffect, useState } from 'react'
import api from '../api'

export default function Dashboard() {
  const [files, setFiles] = useState([])
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState({ filename: '', description: '', tags: '' })

  const load = async () => {
    try {
      setError('')
      const data = await api.get('/files')
      setFiles(data)
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const remove = async (id) => {
    try {
      await api.delete(`/files/${id}`)
      setFiles((prev) => prev.filter((f) => f.id !== id))
    } catch (e) {
      setError(e.message)
    }
  }

  const startEdit = (f) => {
    setEditing(f.id)
    setForm({
      filename: f.filename || '',
      description: f.description || '',
      tags: f.tags?.map((t) => t.name).join(', ') || '',
    })
  }

  const cancelEdit = () => {
    setEditing(null)
    setForm({ filename: '', description: '', tags: '' })
  }

  const save = async (id) => {
    try {
      const payload = {
        filename: form.filename,
        description: form.description,
        tags: form.tags
          .split(',')
          .map((t) => t.trim())
          .filter(Boolean),
      }
      const updated = await api.patch(`/files/${id}`, payload)
      setFiles((prev) => prev.map((f) => (f.id === id ? updated : f)))
      cancelEdit()
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="page">
      <h2>Files</h2>
      {error && <div className="error">{error}</div>}
      <button onClick={load}>Refresh</button>
      <ul className="list">
        {files.map((f) => (
          <li key={f.id} className="list-item">
            {editing === f.id ? (
              <div style={{ width: '100%' }}>
                <div className="card" style={{ margin: 0 }}>
                  <label>
                    Filename
                    <input value={form.filename} onChange={(e) => setForm({ ...form, filename: e.target.value })} />
                  </label>
                  <label>
                    Description
                    <input value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
                  </label>
                  <label>
                    Tags (comma separated)
                    <input value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} />
                  </label>
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button onClick={() => save(f.id)}>Save</button>
                    <button type="button" className="danger" onClick={cancelEdit}>Cancel</button>
                  </div>
                </div>
              </div>
            ) : (
              <>
                <div>
                  <strong>{f.filename}</strong>
                  {f.description ? <span> — {f.description}</span> : null}
                  {f.tags?.length ? (
                    <small> [Tags: {f.tags.map((t) => t.name).join(', ')}]</small>
                  ) : null}
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <button onClick={() => startEdit(f)}>Edit</button>
                  <button className="danger" onClick={() => remove(f.id)}>Delete</button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
