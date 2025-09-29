import { useEffect, useState } from 'react'
import api from '../api'
import { useAuth } from '../context/AuthContext'

export default function Collections() {
  const [collections, setCollections] = useState([])
  const [name, setName] = useState('')
  const { user } = useAuth()
  const [userId, setUserId] = useState(user?.id || 1)
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState({ name: '', file_ids: '' })

  const load = async () => {
    try {
      setError('')
      const data = await api.get('/collections')
      setCollections(data)
    } catch (e) {
      setError(e.message)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const create = async (e) => {
    e.preventDefault()
    try {
      await api.post('/collections', { name, user_id: Number(userId), file_ids: [] })
      setName('')
      load()
    } catch (e) {
      setError(e.message)
    }
  }

  const startEdit = (c) => {
    setEditing(c.id)
    setForm({
      name: c.name || '',
      file_ids: (c.files || []).map((f) => f.id).join(', '),
    })
  }

  const cancelEdit = () => {
    setEditing(null)
    setForm({ name: '', file_ids: '' })
  }

  const save = async (id) => {
    try {
      const file_ids = form.file_ids
        .split(',')
        .map((x) => Number(String(x).trim()))
        .filter((n) => Number.isFinite(n))
      const updated = await api.patch(`/collections/${id}`, { name: form.name, file_ids })
      setCollections((prev) => prev.map((c) => (c.id === id ? updated : c)))
      cancelEdit()
    } catch (e) {
      setError(e.message)
    }
  }

  const remove = async (id) => {
    try {
      await api.delete(`/collections/${id}`)
      setCollections((prev) => prev.filter((c) => c.id !== id))
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <div className="page">
      <h2>Collections</h2>
      {error && <div className="error">{error}</div>}
      {!user && <div className="card" style={{ marginBottom: 12 }}>Tip: Login to auto-fill your user id.</div>}
      <form className="card" onSubmit={create}>
        <label>
          Name
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Team Docs" />
        </label>
        <label>
          User ID
          <input value={userId} onChange={(e) => setUserId(e.target.value)} />
        </label>
        <button type="submit">Create</button>
      </form>
      <ul className="list">
        {collections.map((c) => (
          <li key={c.id} className="list-item">
            {editing === c.id ? (
              <div style={{ width: '100%' }}>
                <div className="card" style={{ margin: 0 }}>
                  <label>
                    Name
                    <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
                  </label>
                  <label>
                    File IDs (comma separated)
                    <input value={form.file_ids} onChange={(e) => setForm({ ...form, file_ids: e.target.value })} />
                  </label>
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button onClick={() => save(c.id)}>Save</button>
                    <button type="button" className="danger" onClick={cancelEdit}>Cancel</button>
                  </div>
                </div>
              </div>
            ) : (
              <>
                <div>
                  <strong>{c.name}</strong>
                  <small> — {c.files?.length || 0} files</small>
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <button onClick={() => startEdit(c)}>Edit</button>
                  <button className="danger" onClick={() => remove(c.id)}>Delete</button>
                </div>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
