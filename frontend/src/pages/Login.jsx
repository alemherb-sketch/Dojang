import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await api.post('/api/token/', {
        username,
        password
      });
      localStorage.setItem('token', response.data.access);
      navigate('/dashboard');
    } catch (err) {
      setError('Usuario o contraseña incorrectos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      {/* Animated background elements */}
      <div style={styles.bgOrb1}></div>
      <div style={styles.bgOrb2}></div>
      <div style={styles.bgOrb3}></div>

      <div style={styles.container}>
        {/* Logo Card */}
        <div style={styles.logoSection}>
          <div style={styles.logoIcon}>🥋</div>
          <h1 style={styles.title}>Dojang Taekwondo</h1>
          <h2 style={styles.subtitle}>Segma</h2>
          <p style={styles.tagline}>Portal de Estudiantes y Padres</p>
        </div>

        {/* Login Card */}
        <div style={styles.card}>
          {/* Accent bar on top */}
          <div style={styles.accentBar}></div>

          {error && (
            <div style={styles.errorBox}>
              <span style={styles.errorIcon}>⚠️</span>
              {error}
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div style={styles.formGroup}>
              <label style={styles.label}>Usuario</label>
              <div style={styles.inputWrapper}>
                <svg style={styles.inputIcon} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.5 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.5-1.632Z" />
                </svg>
                <input
                  type="text"
                  placeholder="Ingresa tu usuario"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  style={styles.input}
                  required
                  autoFocus
                />
              </div>
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Contraseña</label>
              <div style={styles.inputWrapper}>
                <svg style={styles.inputIcon} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
                </svg>
                <input
                  type="password"
                  placeholder="Ingresa tu contraseña"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  style={styles.input}
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              style={{
                ...styles.submitBtn,
                opacity: loading ? 0.7 : 1,
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
              disabled={loading}
            >
              {loading ? (
                <span style={styles.spinner}></span>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>

          <div style={styles.footer}>
            <p style={styles.footerText}>© 2026 Academia Dojang Taekwondo Segma</p>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes float1 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.05); }
          66% { transform: translate(-20px, 20px) scale(0.95); }
        }
        @keyframes float2 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(-40px, 30px) scale(1.1); }
          66% { transform: translate(30px, -20px) scale(0.9); }
        }
        @keyframes float3 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(20px, 40px) scale(1.15); }
        }
        @keyframes slideUp {
          0% { opacity: 0; transform: translateY(30px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeIn {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
          50% { box-shadow: 0 0 0 15px rgba(59, 130, 246, 0); }
        }
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
        input:focus {
          border-color: #3b82f6 !important;
          background-color: #fff !important;
          box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12) !important;
          outline: none;
        }
        button[type="submit"]:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 28px -6px rgba(30, 58, 138, 0.5) !important;
        }
        button[type="submit"]:active {
          transform: translateY(0);
        }
      `}</style>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 40%, #0c1a3a 70%, #0f172a 100%)',
    position: 'relative',
    overflow: 'hidden',
    padding: '20px',
  },
  bgOrb1: {
    position: 'absolute',
    width: '500px',
    height: '500px',
    borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%)',
    top: '-15%',
    right: '-10%',
    animation: 'float1 15s ease-in-out infinite',
    pointerEvents: 'none',
  },
  bgOrb2: {
    position: 'absolute',
    width: '400px',
    height: '400px',
    borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(245,158,11,0.08) 0%, transparent 70%)',
    bottom: '-10%',
    left: '-10%',
    animation: 'float2 12s ease-in-out infinite',
    pointerEvents: 'none',
  },
  bgOrb3: {
    position: 'absolute',
    width: '300px',
    height: '300px',
    borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(239,68,68,0.06) 0%, transparent 70%)',
    top: '40%',
    left: '30%',
    animation: 'float3 18s ease-in-out infinite',
    pointerEvents: 'none',
  },
  container: {
    position: 'relative',
    zIndex: 10,
    width: '100%',
    maxWidth: '420px',
    animation: 'slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1)',
  },
  logoSection: {
    textAlign: 'center',
    marginBottom: '32px',
    animation: 'fadeIn 0.8s ease-out',
  },
  logoIcon: {
    width: '88px',
    height: '88px',
    background: 'linear-gradient(135deg, #1e3a8a, #3b82f6)',
    borderRadius: '22px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '0 auto 20px auto',
    fontSize: '44px',
    boxShadow: '0 15px 35px -5px rgba(30, 58, 138, 0.5)',
    animation: 'pulse 3s ease-in-out infinite',
  },
  title: {
    fontSize: '28px',
    fontWeight: '800',
    color: '#ffffff',
    letterSpacing: '-0.5px',
    lineHeight: '1.1',
    margin: 0,
    textShadow: '0 2px 10px rgba(0,0,0,0.3)',
  },
  subtitle: {
    fontSize: '24px',
    fontWeight: '300',
    color: '#93c5fd',
    letterSpacing: '6px',
    textTransform: 'uppercase',
    margin: '4px 0 0 0',
  },
  tagline: {
    fontSize: '14px',
    color: 'rgba(148, 163, 184, 0.8)',
    marginTop: '12px',
    fontWeight: '400',
  },
  card: {
    background: 'rgba(255, 255, 255, 0.97)',
    backdropFilter: 'blur(20px)',
    borderRadius: '20px',
    padding: '40px 36px',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.05)',
    position: 'relative',
    overflow: 'hidden',
  },
  accentBar: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: 'linear-gradient(90deg, #ef4444, #f59e0b, #1e3a8a, #3b82f6)',
    backgroundSize: '200% 100%',
    animation: 'shimmer 3s linear infinite',
  },
  errorBox: {
    background: 'linear-gradient(135deg, #fef2f2, #fee2e2)',
    color: '#991b1b',
    border: '1px solid #fca5a5',
    borderRadius: '12px',
    padding: '14px 18px',
    fontSize: '14px',
    marginBottom: '24px',
    textAlign: 'center',
    fontWeight: '500',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  },
  errorIcon: {
    fontSize: '16px',
  },
  formGroup: {
    marginBottom: '22px',
  },
  label: {
    display: 'block',
    fontSize: '13px',
    fontWeight: '600',
    color: '#334155',
    marginBottom: '8px',
    letterSpacing: '0.5px',
    textTransform: 'uppercase',
  },
  inputWrapper: {
    position: 'relative',
  },
  inputIcon: {
    position: 'absolute',
    left: '16px',
    top: '50%',
    transform: 'translateY(-50%)',
    width: '20px',
    height: '20px',
    color: '#94a3b8',
    pointerEvents: 'none',
  },
  input: {
    width: '100%',
    padding: '15px 16px 15px 48px',
    border: '2px solid #e2e8f0',
    borderRadius: '12px',
    fontSize: '15px',
    fontFamily: "'Inter', sans-serif",
    color: '#0f172a',
    background: '#f8fafc',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    outline: 'none',
    boxSizing: 'border-box',
  },
  submitBtn: {
    width: '100%',
    padding: '16px',
    background: 'linear-gradient(135deg, #1e3a8a, #2563eb)',
    color: 'white',
    border: 'none',
    borderRadius: '12px',
    fontSize: '16px',
    fontWeight: '700',
    fontFamily: "'Inter', sans-serif",
    letterSpacing: '0.5px',
    textTransform: 'uppercase',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    marginTop: '8px',
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
  },
  spinner: {
    width: '22px',
    height: '22px',
    border: '3px solid rgba(255,255,255,0.3)',
    borderTopColor: '#ffffff',
    borderRadius: '50%',
    display: 'inline-block',
    animation: 'spin 0.6s linear infinite',
  },
  footer: {
    textAlign: 'center',
    marginTop: '28px',
    paddingTop: '20px',
    borderTop: '1px solid #e2e8f0',
  },
  footerText: {
    fontSize: '12px',
    color: '#94a3b8',
    fontWeight: '400',
    margin: 0,
  },
};
