import { Link, NavLink, useNavigate } from 'react-router-dom'
import './NavBar.css'
import { useAuth } from '../context/AuthContext'

export default function NavBar() {
  const { user, logout } = useAuth()
  const nav = useNavigate()

  const onLogout = () => {
    logout()
    nav('/login')
  }

  return (
    <nav className="nav">
      <Link className="brand" to="/">Data-Hub</Link>
      <div className="links">
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/upload">Upload</NavLink>
        <NavLink to="/collections">Collections</NavLink>
        {user ? (
          <>
            <span style={{ marginLeft: 12, opacity: 0.8 }}>Hi, {user.username}</span>
            <button style={{ marginLeft: 12 }} onClick={onLogout}>Logout</button>
          </>
        ) : (
          <>
            <NavLink to="/login">Login</NavLink>
            <NavLink to="/register">Register</NavLink>
          </>
        )}
      </div>
    </nav>
  )
}
