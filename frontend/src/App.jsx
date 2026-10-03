import { useEffect, useState } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import axios from 'axios';

const API = 'http://localhost:8001';

const serviceCategories = [
  'Company formation',
  'Legal compliance',
  'Contracts',
  'Disputes',
  'Property',
  'IP & Brand',
  'Startup advisory',
  'Documentation',
  'Quick consults',
];

function formatMoney(value) {
  return `₹${Number(value).toLocaleString('en-IN')}`;
}

function HomePage() {
  const [services, setServices] = useState([]);
  const [booking, setBooking] = useState({
    name: '',
    email: '',
    phone: '',
    city: '',
    service: 'Private Limited Company',
    consultation_type: 'Video Call',
    budget: '₹1,000 - ₹5,000',
    urgency: 'This week',
    message: '',
  });
  const [success, setSuccess] = useState('');

  useEffect(() => {
    axios.get(`${API}/api/services`).then((res) => setServices(res.data.items || [])).catch(() => setServices([]));
  }, []);

  function handleChange(e) {
    setBooking((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const result = await axios.post(`${API}/api/bookings`, booking);
      setSuccess(`Consultation request submitted successfully. Reference: ${result.data.booking.id}`);
      setBooking({
        name: '',
        email: '',
        phone: '',
        city: '',
        service: services[0]?.name || 'Private Limited Company',
        consultation_type: 'Video Call',
        budget: '₹1,000 - ₹5,000',
        urgency: 'This week',
        message: '',
      });
    } catch (err) {
      setSuccess('Unable to submit the request right now. Please try again.');
    }
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div className="brand-wrap">
          <div className="brand-mark">SP</div>
          <div>
            <div className="brand-name">SpLegalMart</div>
            <small>Legal | Compliance | Growth</small>
          </div>
        </div>

        <nav className="nav-links">
          <a href="#services">Services</a>
          <a href="#pricing">Pricing</a>
          <a href="#booking">Book</a>
          <Link to="/admin">Admin</Link>
        </nav>
      </header>

      <main>
        <section className="hero">
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="hero-copy">
            <p className="eyebrow">PAN India legal + para-legal support</p>
            <h1>Legal clarity for businesses, founders, and families.</h1>
            <p className="lead">From company registration to contract support, property due diligence, disputes, and brand protection — SpLegalMart keeps your legal foundations strong.</p>
            <div className="cta-row">
              <a href="#booking" className="primary-btn">Book a consultation</a>
              <a href="#pricing" className="secondary-btn">Explore pricing</a>
            </div>
            <div className="stats-row">
              <div><strong>24-hour</strong><span>delivery promise</span></div>
              <div><strong>100%</strong><span>refund guarantee</span></div>
              <div><strong>₹199</strong><span>Pan India consult</span></div>
            </div>
          </motion.div>

          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="hero-visual">
            <div className="seal-card">
              <div className="seal-ring">SP</div>
            </div>
          </motion.div>
        </section>

        <section className="marquee-block">
          <div className="marquee-track">
            <span>Company formation</span>
            <span>Trademark filing</span>
            <span>GST registration</span>
            <span>Legal notices</span>
            <span>Rent agreements</span>
            <span>Founder advisory</span>
            <span>Consumer complaints</span>
            <span>Contract drafting</span>
            <span>Property due diligence</span>
            <span>Legal audit</span>
          </div>
        </section>

        <section id="services" className="section-block">
          <div className="section-head">
            <p className="eyebrow">What we do</p>
            <h2>Core offerings</h2>
          </div>

          <div className="category-grid">
            {serviceCategories.map((category) => (
              <div className="category-item" key={category}>{category}</div>
            ))}
          </div>

          <div className="service-list">
            {services.slice(0, 10).map((service) => (
              <div className="service-card" key={service.id}>
                <div>
                  <span className="service-category">{service.category}</span>
                  <h3>{service.name}</h3>
                </div>
                <div className="service-meta">
                  <strong>{formatMoney(service.fee)}</strong>
                  <small>{service.unit}</small>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section id="pricing" className="section-block pricing-block">
          <div className="section-head">
            <p className="eyebrow">Transparent pricing</p>
            <h2>Simple, fair, and clear</h2>
          </div>

          <div className="pricing-grid">
            {services.slice(0, 8).map((service) => (
              <div className="pricing-card" key={service.id}>
                <span>{service.category}</span>
                <h3>{service.name}</h3>
                <div className="price">{formatMoney(service.fee)}</div>
                <small>{service.unit}</small>
              </div>
            ))}
          </div>
        </section>

        <section id="booking" className="section-block booking-wrap">
          <div className="booking-form-card">
            <div className="section-head left">
              <p className="eyebrow">Consultation</p>
              <h2>Book a legal consult</h2>
            </div>

            <form onSubmit={handleSubmit} className="booking-form">
              <div className="field-grid">
                <input name="name" value={booking.name} onChange={handleChange} placeholder="Full name" required />
                <input name="email" type="email" value={booking.email} onChange={handleChange} placeholder="Email" required />
                <input name="phone" value={booking.phone} onChange={handleChange} placeholder="Phone" required />
                <input name="city" value={booking.city} onChange={handleChange} placeholder="City" required />
                <select name="service" value={booking.service} onChange={handleChange}>
                  {services.map((s) => (
                    <option key={s.id} value={s.name}>{s.name}</option>
                  ))}
                </select>
                <select name="consultation_type" value={booking.consultation_type} onChange={handleChange}>
                  <option value="Video Call">Video call</option>
                  <option value="Office Visit">Office visit</option>
                  <option value="Door-to-door">Door-to-door</option>
                </select>
                <select name="budget" value={booking.budget} onChange={handleChange}>
                  <option>₹1,000 - ₹5,000</option>
                  <option>₹5,000 - ₹20,000</option>
                  <option>₹20,000 - ₹50,000</option>
                  <option>₹50,000+</option>
                </select>
                <select name="urgency" value={booking.urgency} onChange={handleChange}>
                  <option>This week</option>
                  <option>Within 2 weeks</option>
                  <option>Flexible</option>
                </select>
              </div>
              <textarea name="message" value={booking.message} onChange={handleChange} placeholder="Tell us about your matter" rows="5" />
              <button type="submit" className="primary-btn">Submit request</button>
              {success ? <p className="success-note">{success}</p> : null}
            </form>
          </div>

          <aside className="payment-card">
            <p className="eyebrow">UPI payment</p>
            <h3>Pay securely via UPI</h3>
            <div className="qr-box">QR</div>
            <div className="upi-id">7992461191@ybl</div>
            <button className="secondary-btn copy-btn" onClick={() => navigator.clipboard.writeText('7992461191@ybl')}>Copy UPI ID</button>
          </aside>
        </section>
      </main>
    </div>
  );
}

function AdminPage() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [token, setToken] = useState(localStorage.getItem('splegalmart-token') || '');
  const [email, setEmail] = useState('admin@splegalmart.com');
  const [password, setPassword] = useState('admin123');
  const [bookings, setBookings] = useState([]);
  const [services, setServices] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (token) {
      setLoggedIn(true);
      loadData();
    }
  }, [token]);

  async function loadData() {
    if (!token) return;
    try {
      const [bookingsRes, servicesRes] = await Promise.all([
        axios.get(`${API}/api/admin/bookings`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/api/admin/services`, { headers: { Authorization: `Bearer ${token}` } }),
      ]);
      setBookings(bookingsRes.data || []);
      setServices(servicesRes.data.items || []);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const res = await axios.post(`${API}/api/auth/login`, { email, password });
      localStorage.setItem('splegalmart-token', res.data.access_token);
      setToken(res.data.access_token);
      setLoggedIn(true);
      navigate('/admin');
    } catch (err) {
      alert('Invalid credentials');
    }
  }

  function logout() {
    localStorage.removeItem('splegalmart-token');
    setToken('');
    setLoggedIn(false);
  }

  async function updateStatus(id, status) {
    await axios.put(`${API}/api/admin/bookings/${id}/status?status=${status}`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    loadData();
  }

  async function deleteBooking(id) {
    await axios.delete(`${API}/api/admin/bookings/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    loadData();
  }

  if (!loggedIn) {
    return (
      <div className="admin-shell">
        <div className="login-card">
          <h2>SpLegalMart admin</h2>
          <form onSubmit={handleLogin} className="login-form">
            <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
            <button type="submit" className="primary-btn">Login</button>
          </form>
          <Link to="/">Back to landing page</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-shell">
      <div className="admin-topbar">
        <h2>Admin dashboard</h2>
        <button onClick={logout} className="secondary-btn">Logout</button>
      </div>

      <div className="admin-panels">
        <div className="panel">
          <h3>Bookings</h3>
          {bookings.map((booking) => (
            <div key={booking.id} className="booking-row">
              <div>
                <strong>{booking.name}</strong>
                <small>{booking.service}</small>
              </div>
              <select value={booking.status} onChange={(e) => updateStatus(booking.id, e.target.value)}>
                <option>New</option>
                <option>In Review</option>
                <option>Confirmed</option>
                <option>Completed</option>
                <option>Cancelled</option>
              </select>
              <button onClick={() => deleteBooking(booking.id)} className="secondary-btn danger">Delete</button>
            </div>
          ))}
        </div>

        <div className="panel">
          <h3>Services</h3>
          <ul className="service-admin-list">
            {services.map((s) => (
              <li key={s.id}>{s.name} — {formatMoney(s.fee)}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/admin" element={<AdminPage />} />
    </Routes>
  );
}
