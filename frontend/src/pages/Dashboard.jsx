import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import QRCode from 'react-qr-code';

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [activities, setActivities] = useState([]);
  const [attendances, setAttendances] = useState([]);
  const [activeTab, setActiveTab] = useState('qr');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) { navigate('/'); return; }

    const fetchData = async () => {
      try {
        const config = { headers: { Authorization: `Bearer ${token}` } };
        const userRes = await api.get('/api/profile/', config);
        setProfile(userRes.data);
        if (userRes.data.role !== 'STUDENT' && activeTab === 'qr') {
          setActiveTab('activities');
        }
        
        const actRes = await api.get('/api/activities/', config);
        setActivities(actRes.data);
        
        const attRes = await api.get('/api/dashboard/attendance/', config);
        setAttendances(attRes.data);
      } catch (err) {
        localStorage.removeItem('token');
        navigate('/');
      }
    };
    fetchData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (!profile) {
    return (
      <div style={styles.loadingPage}>
        <div style={styles.loadingSpinner}></div>
        <p style={styles.loadingText}>Cargando...</p>
        <style>{`
          @keyframes spin { to { transform: rotate(360deg); } }
        `}</style>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <div style={styles.headerLeft}>
            <span style={styles.headerIcon}>🥋</span>
            <div>
              <h1 style={styles.headerTitle}>Dojang Segma</h1>
              <p style={styles.headerSub}>Panel del Estudiante</p>
            </div>
          </div>
          <button onClick={handleLogout} style={styles.logoutBtn}>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
            </svg>
            Salir
          </button>
        </div>
      </header>

      <main style={styles.main}>
        {/* Welcome Card */}
        <div style={styles.welcomeCard}>
          <div style={styles.welcomeGradient}></div>
          <div style={styles.welcomeContent}>
            <div style={styles.avatar}>
              {(profile.first_name || profile.username)[0].toUpperCase()}
            </div>
            <div>
              <h2 style={styles.welcomeName}>
                ¡Hola, {profile.first_name || profile.username}!
              </h2>
              <span style={styles.roleBadge}>{profile.role}</span>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div style={styles.tabBar}>
          {[
            ...(profile.role === 'STUDENT' ? [{ id: 'qr', label: '📱 Mi QR' }] : []),
            { id: 'activities', label: '📢 Actividades' },
            { id: 'attendance', label: '✅ Asistencias' },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                ...styles.tabBtn,
                ...(activeTab === tab.id ? styles.tabBtnActive : {}),
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* QR Section */}
        {activeTab === 'qr' && profile.role === 'STUDENT' && (
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>Tu Código de Asistencia</h3>
            <p style={styles.cardDesc}>Muestra este código al instructor al ingresar a clase.</p>
            <div style={styles.qrContainer}>
              <div style={styles.qrWrapper}>
                <QRCode
                  value={profile.qr_code || profile.username}
                  size={180}
                  bgColor="#ffffff"
                  fgColor="#0f172a"
                  level="H"
                />
              </div>
              <p style={styles.qrName}>{profile.first_name} {profile.last_name}</p>
              <p style={styles.qrId}>ID: {profile.qr_code || profile.username}</p>
            </div>
          </div>
        )}

        {/* Activities Section */}
        {activeTab === 'activities' && (
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>📢 Tablón de Actividades</h3>
            <div style={styles.activitiesList}>
              {activities.length > 0 ? (
                activities.map(act => (
                  <div key={act.id} style={styles.activityItem}>
                    <div style={styles.activityAccent}></div>
                    <div style={styles.activityContent}>
                      <h4 style={styles.activityTitle}>{act.title}</h4>
                      <p style={styles.activityDate}>
                        {new Date(act.date_posted).toLocaleDateString('es-PE', {
                          day: 'numeric', month: 'long', year: 'numeric'
                        })}
                      </p>
                      <p style={styles.activityText}>{act.content}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div style={styles.emptyState}>
                  <span style={{ fontSize: '48px' }}>📋</span>
                  <p style={styles.emptyText}>No hay actividades recientes</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Attendance Section */}
        {activeTab === 'attendance' && (
          <div style={styles.card}>
            <h3 style={styles.cardTitle}>✅ Registro de Asistencias</h3>
            <div style={styles.activitiesList}>
              {attendances.length > 0 ? (
                attendances.map(att => (
                  <div key={att.id} style={styles.activityItem}>
                    <div style={{ ...styles.activityAccent, background: 'linear-gradient(180deg, #10b981, #059669)' }}></div>
                    <div style={styles.activityContent}>
                      <h4 style={styles.activityTitle}>{att.student_name}</h4>
                      <p style={styles.activityDate}>
                        {new Date(`${att.date}T${att.time}`).toLocaleString('es-PE', {
                          day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit'
                        })}
                      </p>
                      <p style={styles.activityText}>
                        Estado: <strong style={{color: att.status === 'P' ? '#10b981' : (att.status === 'L' ? '#f59e0b' : '#ef4444')}}>
                          {att.status === 'P' ? 'Presente' : (att.status === 'L' ? 'Tarde' : 'Ausente')}
                        </strong> | Grupo: {att.section_name}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <div style={styles.emptyState}>
                  <span style={{ fontSize: '48px' }}>📅</span>
                  <p style={styles.emptyText}>No hay asistencias recientes</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      <style>{`
        @keyframes slideDown {
          0% { opacity: 0; transform: translateY(-20px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
          0% { opacity: 0; transform: translateY(20px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        button:hover { opacity: 0.9; }
      `}</style>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    background: 'linear-gradient(180deg, #0f172a 0%, #1e293b 100%)',
    fontFamily: "'Inter', sans-serif",
  },
  loadingPage: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    background: '#0f172a',
    gap: '16px',
  },
  loadingSpinner: {
    width: '40px',
    height: '40px',
    border: '4px solid rgba(59,130,246,0.2)',
    borderTopColor: '#3b82f6',
    borderRadius: '50%',
    animation: 'spin 0.6s linear infinite',
  },
  loadingText: {
    color: '#94a3b8',
    fontSize: '14px',
    fontFamily: "'Inter', sans-serif",
  },
  header: {
    background: 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)',
    padding: '0',
    boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
    animation: 'slideDown 0.5s ease-out',
  },
  headerContent: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '16px 20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  headerIcon: {
    fontSize: '32px',
    filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))',
  },
  headerTitle: {
    fontSize: '18px',
    fontWeight: '800',
    color: '#ffffff',
    margin: 0,
    letterSpacing: '-0.3px',
  },
  headerSub: {
    fontSize: '12px',
    color: 'rgba(191,219,254,0.8)',
    margin: 0,
    fontWeight: '400',
  },
  logoutBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
    background: 'rgba(255,255,255,0.15)',
    border: '1px solid rgba(255,255,255,0.2)',
    color: 'white',
    padding: '8px 16px',
    borderRadius: '10px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
    fontFamily: "'Inter', sans-serif",
    backdropFilter: 'blur(10px)',
  },
  main: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    animation: 'fadeInUp 0.6s ease-out',
  },
  welcomeCard: {
    background: 'rgba(255,255,255,0.06)',
    borderRadius: '18px',
    overflow: 'hidden',
    position: 'relative',
    border: '1px solid rgba(255,255,255,0.08)',
  },
  welcomeGradient: {
    height: '4px',
    background: 'linear-gradient(90deg, #ef4444, #f59e0b, #3b82f6)',
  },
  welcomeContent: {
    padding: '24px',
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  avatar: {
    width: '52px',
    height: '52px',
    borderRadius: '14px',
    background: 'linear-gradient(135deg, #3b82f6, #1e3a8a)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '22px',
    fontWeight: '800',
    color: 'white',
    boxShadow: '0 4px 12px rgba(59,130,246,0.3)',
    flexShrink: 0,
  },
  welcomeName: {
    fontSize: '20px',
    fontWeight: '700',
    color: '#ffffff',
    margin: '0 0 6px 0',
  },
  roleBadge: {
    display: 'inline-block',
    background: 'rgba(59,130,246,0.15)',
    color: '#93c5fd',
    padding: '4px 12px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    border: '1px solid rgba(59,130,246,0.2)',
  },
  tabBar: {
    display: 'flex',
    gap: '8px',
    background: 'rgba(255,255,255,0.04)',
    borderRadius: '14px',
    padding: '6px',
    border: '1px solid rgba(255,255,255,0.06)',
  },
  tabBtn: {
    flex: 1,
    padding: '12px',
    border: 'none',
    borderRadius: '10px',
    background: 'transparent',
    color: '#94a3b8',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
    fontFamily: "'Inter', sans-serif",
  },
  tabBtnActive: {
    background: 'rgba(59,130,246,0.15)',
    color: '#ffffff',
    boxShadow: '0 2px 8px rgba(59,130,246,0.2)',
  },
  card: {
    background: 'rgba(255,255,255,0.06)',
    borderRadius: '18px',
    padding: '28px 24px',
    border: '1px solid rgba(255,255,255,0.08)',
    backdropFilter: 'blur(10px)',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: '700',
    color: '#ffffff',
    margin: '0 0 8px 0',
  },
  cardDesc: {
    fontSize: '14px',
    color: '#94a3b8',
    margin: '0 0 24px 0',
  },
  qrContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '16px',
  },
  qrWrapper: {
    background: '#ffffff',
    padding: '20px',
    borderRadius: '16px',
    boxShadow: '0 8px 25px rgba(0,0,0,0.2)',
  },
  qrName: {
    fontSize: '16px',
    fontWeight: '700',
    color: '#ffffff',
    margin: 0,
  },
  qrId: {
    fontSize: '13px',
    color: '#64748b',
    margin: 0,
    fontFamily: 'monospace',
  },
  activitiesList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '14px',
    marginTop: '16px',
  },
  activityItem: {
    display: 'flex',
    background: 'rgba(255,255,255,0.04)',
    borderRadius: '14px',
    overflow: 'hidden',
    border: '1px solid rgba(255,255,255,0.06)',
    transition: 'all 0.2s',
  },
  activityAccent: {
    width: '4px',
    background: 'linear-gradient(180deg, #f59e0b, #ef4444)',
    flexShrink: 0,
  },
  activityContent: {
    padding: '16px 18px',
    flex: 1,
  },
  activityTitle: {
    fontSize: '15px',
    fontWeight: '700',
    color: '#ffffff',
    margin: '0 0 4px 0',
  },
  activityDate: {
    fontSize: '12px',
    color: '#64748b',
    margin: '0 0 8px 0',
  },
  activityText: {
    fontSize: '14px',
    color: '#cbd5e1',
    margin: 0,
    lineHeight: '1.5',
  },
  emptyState: {
    textAlign: 'center',
    padding: '40px 20px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '12px',
  },
  emptyText: {
    color: '#64748b',
    fontSize: '14px',
    margin: 0,
  },
};
